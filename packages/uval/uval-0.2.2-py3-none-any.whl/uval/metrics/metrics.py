# -*- coding: utf-8 -*-
"""This module provides stages that can compute metrics like overlaps between
groundtruth and detections, or simply count detections per bag.
"""
import os
import pickle
import warnings
from collections import ChainMap
from multiprocessing import Pool
from statistics import fmean
from typing import Any, Dict, List

import jinja2  # type: ignore
import matplotlib  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import numpy as np
import pandas as pd  # type: ignore
from rich.console import Console
from rich.progress import Progress
from rich.table import Table

from uval.data.dataset import UVALDATASET
from uval.metrics.metrics_utils import get_average_precision, get_average_recall, get_fscore
from uval.stages.stage import uval_stage  # type: ignore
from uval.stages.stage_data import SupportedDatasetSpecificationData
from uval.utils.iou import iou as iou_func
from uval.utils.log import logger
from uval.utils.metric_utils import bin_placement, counter_cumsum, counter_sum_norm

matplotlib.use("Agg")


class Metrics:
    def __init__(self):
        pass


class Metrics3D(Metrics):
    """This class implements all the evaluation metrics."""

    def __init__(self, config, dataset: UVALDATASET):
        super().__init__()
        self.dataset = dataset
        self.dataset.load_dataset()
        self.data = None
        self.blade_length_classes = config.METRICS.BLADE_LENGTH_ANALYSIS_CLASSES
        self.blade_length_bins = config.METRICS.BLADE_LENGTH_BINS
        self.iou_threshold = config.METRICS.IOU_THRESHOLD
        self.class_mappings = {w: k for mapping in config.DATA.CLASS_MAPPINGS for k, v in mapping.items() for w in v}
        self.blade_length_dataset = dataset.dataset.create_blade_length_dataset(
            self.blade_length_bins, self.blade_length_classes
        )
        # class mappings need to be set before this feature:
        self.class_specific_confidence_threshold = config.METRICS.CLASS_SPECIFIC_CONFIDENCE_THRESHOLD
        if len(config.METRICS.IOU_RANGE) == 3:
            a, b, c = config.METRICS.IOU_RANGE
            self.iou_range = np.linspace(a, b, int(np.round((b - a) / c)) + 1, endpoint=True).tolist()
            self.iou_range = [round(iou, 2) for iou in self.iou_range]
            self.template_file = config.OUTPUT.TEMPLATES_FILE_RANGE
            self.template_file_subclass = config.OUTPUT.TEMPLATES_FILE_RANGE_SUBCLASS
        else:
            self.iou_range = None
        self.confidence_threshold = config.METRICS.CONFIDENCE_THRESHOLD
        self.output_path = config.OUTPUT.PATH

        self.title = config.OUTPUT.TITLE or self.output_path.split("/")[-1]

        self.metrics_file = config.OUTPUT.METRICS_FILE
        self.max_workers = config.METRICS.MAX_PROCESSES

        self.ap_method = config.METRICS.AP_METHOD
        self.factor = config.METRICS.FACTOR

        self.ignored_classes = set()

    def run(self):
        hallucination_log, basics = self.basic_metric()
        if self.blade_length_classes:
            self.blade_length_analysis(basics)
        single_recall = {basic["Class"]: basic["Single Recall"] for basic in basics}
        single_recall_subclass = {basic["Class"]: basic["Single Recall Subclass"] for basic in basics}
        confidence_for_all_classes = {basic["Class"]: basic["Conf Thresh"] for basic in basics}
        ap_metrics = get_average_precision(basics, method=self.ap_method)
        fscore_metrics = get_fscore(ap_metrics, factor=self.factor)

        metrics_output = {
            "title": self.title,
            "iou_threshold": self.iou_threshold,
            "single_threshold": fscore_metrics,
            "Conf Thresh": self.confidence_threshold,
        }
        metrics_output["Hallucinations"] = hallucination_log

        if self.iou_range:
            aps, rs, ars, map, mar, rs_subclass = self.evaluate_range(
                single_recall,
                single_recall_subclass,
                iou_range=self.iou_range,
                confidence_for_all_classes=confidence_for_all_classes,
            )
            metrics_output["AP"] = aps
            metrics_output["rs"] = rs
            metrics_output["rs_subclass"] = rs_subclass
            metrics_output["ars"] = ars
            metrics_output["map"] = map
            metrics_output["mar"] = mar
            metrics_output["iou_range"] = self.iou_range

            metrics_output["blade_length"] = self.blade_length_dataset
        with open(os.path.join(self.output_path, self.metrics_file), "wb") as f:
            pickle.dump(metrics_output, f)
        logger.info(f"metrics saved to {os.path.join(self.output_path, self.metrics_file)}.")
        return True

    def worker(self, iou_threshold):
        _, basics = self.basic_metric(iou_threshold=iou_threshold)

        rs = [result["Single Recall"] for result in basics]
        rs_subclass = [result["Single Recall Subclass"] for result in basics]
        output_metrics = get_average_precision(basics)
        aps = [result["AP"] for result in output_metrics]
        # mean_ap = sum(aps) / len(aps)
        map = fmean(aps)
        classes = [basic["Class"] for basic in basics]
        return rs, aps, map, classes, rs_subclass

    def evaluate_range(
        self,
        single_recall,
        single_recall_subclass,
        iou_range: List[float],
        confidence_threshold: float = None,
        confidence_for_all_classes: Dict = dict(),
    ):
        # if not iou_range:
        #    iou_range = self.iou_range
        if not confidence_threshold:
            confidence_threshold = self.confidence_threshold

        aps = {}
        rs: Dict[float, List[float]] = {}
        map = {}
        rs_subclass = {}
        result = []
        with Progress() as progress:
            task_id = progress.add_task("[cyan]Completed...", total=len(iou_range))
            with Pool(self.max_workers) as pool:
                res = pool.starmap_async(
                    self.worker, [(r,) for r in iou_range], callback=lambda x: progress.advance(task_id)
                )
                result.extend(res.get())

        # with Pool(self.max_workers) as pool:
        # for iou in iou_range:
        #    res = self.worker(iou)

        #    result = pool.map(self.worker, iou_range)

        for iou, res in zip(iou_range, result):
            rs[iou] = res[0]
            aps[iou] = res[1]
            map[iou] = res[2]
            classes = res[3]
            rs_subclass[iou] = res[4]

        assert len(aps) == len(iou_range)
        ars = get_average_recall(rs, iou_range)

        mar = sum(ars) / len(ars)
        return aps, rs, ars, map, mar, rs_subclass

    @property
    def class_specific_confidence_threshold(self):
        return self._class_specific_confidence_threshold

    @class_specific_confidence_threshold.setter
    def class_specific_confidence_threshold(self, confidence_thresholds):
        c = {(self.class_mappings.get(k) or k): v for part in confidence_thresholds for k, v in part.items()}
        self._class_specific_confidence_threshold = c

    @uval_stage
    def basic_metric(self, iou_threshold: float = None, confidence_threshold: float = None) -> List[dict]:
        """Get the TP, FP, Precision and recall.

        Args:
            iou_threshold (float, optional): Threshold for IOU. Defaults to None.
            confidence_threshold (float, optional): Threshold for confidence. Defaults to None.

        Returns:
            List[dict]: A list of dictionaries. Each dictionary contains information and
            metrics of each class.
        """

        if not self.data:
            self.data = self.dataset.data_preparations()

        hallucination_log, classes, volumes_soc, ground_truths, detections, total_negative = self.data
        if iou_threshold is None:
            iou_threshold = self.iou_threshold
        if confidence_threshold is None:
            confidence_threshold = self.confidence_threshold
        ret = []
        # Loop through by classes
        total_gt_count = sum(len(v) for v in ground_truths.values())

        for c, sub_c in classes.items():
            blade_length_dataset = self.blade_length_dataset[c]
            if c in self.ignored_classes:
                continue
            class_specific_confidence_threshold = (
                self.class_specific_confidence_threshold.get(c) or confidence_threshold
            )
            logger.debug(f"class {c} has confidece value {class_specific_confidence_threshold}")
            volumes_negative_current = {v: 0 for v in volumes_soc}

            # Get only detection of class c
            dects = detections.get(c)
            if not dects:
                self.ignored_classes.add(c)
                logger.warning(f"No detections found for class {c}. Ignoring this class ...")
                continue

            # dects = [d for d in detections if d.class_name == c]
            # Get only ground truths of class c, use filename as key
            gts: Dict[Any, Any] = {}
            gts_single_class = ground_truths.get(c)
            npos = len(gts_single_class)
            blade_length_npos = {bin: len(blade_length_dataset[bin]) for bin in self.blade_length_bins}
            nneg = total_gt_count - npos
            gts = gts_single_class.to_dict()

            # sort detections by decreasing confidence
            total_tp = 0
            total_fp = 0
            fp_image_level = np.zeros(len(dects))
            fp_image_level_volume = [""] * len(dects)
            fp_image_level_confidence = np.zeros(len(dects))
            # tp_subclass_level = {sc:np.zeros(count) for sc, count in sub_c.items()}
            # fp_subclass_level = {sc:np.zeros(len(dects)) for sc in sub_c}
            tp_subclass_level = [0] * len(dects)  # list with subclass of detected or 0 for not matched
            tp_blade_length = [0] * len(dects)
            tp = np.zeros(len(dects))
            fp = np.zeros(len(dects))
            tp_volume = [""] * len(dects)
            tp_label = [""] * len(dects)
            fp_volume = [""] * len(dects)
            conf_level = np.zeros(len(dects))
            tp_soft = 0
            fp_soft = 0
            # create dictionary with amount of gts for each image
            det = {key: np.zeros(len(value)) for key, value in gts.items()}
            sorted_volume_ids = []
            # Loop through detections
            single_recall = 0.0
            single_recall_blade_length = None
            single_fpr = 1.0
            for d, dect in enumerate(iter(dects)):
                conf_level[d] = dect.score
                if dect.score > class_specific_confidence_threshold:
                    single_recall = float(np.sum(tp)) / npos
                    single_recall_subclass = counter_sum_norm(tp_subclass_level, sub_c)

                    if c in self.blade_length_classes:
                        single_recall_blade_length = counter_sum_norm(tp_blade_length, blade_length_npos)

                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        single_prec = np.divide(float(np.sum(tp)), (float(np.sum(fp)) + float(np.sum(tp))))
                    single_fpr = float(np.sum(fp_image_level)) / float(total_negative)
                if dect.volume_id in volumes_negative_current:
                    fp_image_level[d] = 1
                    fp_image_level_volume[d] = dect.volume_id
                    fp_image_level_confidence[d] = dect.score
                    volumes_negative_current.pop(dect.volume_id, None)

                # Find ground truth image
                gt = gts.get(dect.volume_id, [])
                blade_length_quantized, j_subclass, jmax, iou_max = 0, 0, 0, -1.0  # sys.float_info.min
                for j, gtj in enumerate(gt):
                    if det[dect.volume_id][j] == 0:
                        iou = iou_func(dect.roi_start, dect.roi_shape, gtj.roi_start, gtj.roi_shape)
                        if iou > iou_max:
                            iou_max = iou
                            jmax = j
                            j_subclass = gtj.subclass_name
                            j_label = gtj.label_name
                            if c in self.blade_length_classes:
                                blade_length_quantized = bin_placement(gtj.blade_length, self.blade_length_bins)

                # Assign detection as true positive/don't care/false positive
                if iou_max >= iou_threshold:
                    if det[dect.volume_id][jmax] == 0:
                        tp[d] = 1  # count as true positive
                        tp_volume[d] = dect.volume_id
                        tp_label[d] = j_label
                        tp_subclass_level[d] = j_subclass
                        if c in self.blade_length_classes:
                            tp_blade_length[d] = blade_length_quantized
                        if dect.volume_id not in sorted_volume_ids:
                            sorted_volume_ids.append(dect.volume_id)
                        total_tp += 1 if dect.score > class_specific_confidence_threshold else 0
                        tp_soft += dect.score if dect.score > class_specific_confidence_threshold else 0
                        det[dect.volume_id][jmax] = 1  # flag as already 'seen'
                    else:
                        fp[d] = 1  # count as false positive
                        fp_volume[d] = dect.volume_id
                        total_fp += 1 if dect.score > class_specific_confidence_threshold else 0
                        fp_soft += dect.score if dect.score > class_specific_confidence_threshold else 0
                # - A detected "cat" is overlaped with a GT "cat" with IOU >= iou_threshold.
                else:
                    fp[d] = 1  # count as false positive
                    fp_volume[d] = dect.volume_id
                    total_fp += 1 if dect.score > class_specific_confidence_threshold else 0
                    fp_soft += dect.score if dect.score > class_specific_confidence_threshold else 0

            # for vol_id in gts.keys():
            #    if vol_id not in sorted_volume_ids:
            #        sorted_volume_ids.append(vol_id)
            # compute precision, recall and average precision
            acc_fp = np.cumsum(fp)
            acc_tp = np.cumsum(tp)

            acc_tp_subclass_level = counter_cumsum(tp_subclass_level, sub_c)
            acc_tp_blade_length = counter_cumsum(tp_blade_length, blade_length_npos)
            acc_fp_image_level = np.cumsum(fp_image_level)
            fpr = acc_fp_image_level / total_negative
            rec = acc_tp / npos
            rec_subclass_level = {
                k: list(map(lambda x: x / sub_c[k], v)) for k, v in acc_tp_subclass_level.items() if k in sub_c
            }

            if c in self.blade_length_classes:
                rec_blade_length = {
                    k: list(map(lambda x: x / blade_length_npos[k], v))
                    for k, v in acc_tp_blade_length.items()
                    if k in blade_length_npos
                }
            else:
                rec_blade_length = {}

            prec = np.divide(acc_tp, (acc_fp + acc_tp))

            # Depending on the method, call the right implementation
            # add class result in the dictionary to be returned
            # logger.info(f"volumes for class {c} in the order of detection quality are: {sorted_volume_ids}")
            logger.debug(
                f"volumes for class {c}, iou:{iou_threshold}, confidence:{class_specific_confidence_threshold}"
                f"with low quality detections are: {set(gts.keys()) - set(sorted_volume_ids)}"
            )
            r = {
                "Class": c,
                "Conf Thresh": class_specific_confidence_threshold,
                "precision": prec,
                "recall subclass": rec_subclass_level,
                "recall bladelength": rec_blade_length,
                "recall": rec,
                "conf level": conf_level,
                "Single FPr": single_fpr,
                "Single Recall": single_recall,
                "Single Recall Subclass": single_recall_subclass,
                "Single Recall Bladelength": single_recall_blade_length,
                "Single Precision": single_prec,
                "Total Positives": int(npos),
                "Total Negatives": int(nneg),
                "Total TP": int(total_tp),
                "Total FP": int(total_fp),
                "Total FN": int(npos - total_tp),
                "Total TP soft": tp_soft,
                "Total FP soft": fp_soft,
                "Total FN soft": npos - tp_soft,
                "FPr": fpr,
                "failed volumes": set(gts.keys()) - set(sorted_volume_ids),
                "TP Volume": tp_volume,
                "TP Label": tp_label,
                "FP Volume": fp_volume,
                "FP Image Volume": fp_image_level_volume,
                "FP Image Confidence": fp_image_level_confidence,
            }
            ret.append(r)

        return hallucination_log, ret

    @uval_stage
    def blade_length_analysis(self, metrics):
        for c, dict_of_lengths in self.blade_length_dataset.items():
            total = {k: len(v) for k, v in dict_of_lengths.items()}
            for m in metrics:
                if m["Class"] == c:
                    bladelength_tpr_vector = m["recall bladelength"]
                    fpr_vector = m["FPr"]
                    single_fpr = m["Single FPr"]
                    single_bla = m["Single Recall Bladelength"]

                    for leng, single_recall in single_bla.items():
                        plt.close()
                        plt.plot(fpr_vector, bladelength_tpr_vector[leng], label=f"ROC for Blade Length:{leng}")
                        plt.xlabel("FP Rate")
                        plt.ylabel("TP Rate")
                        plt.title("ROC curve \nClass: %s" % str(c))
                        plt.legend(shadow=True)
                        plt.grid()
                        plt.xlim([0.0, 0.2])
                        plt.ylim([0.0, 1.0])
                        plt.plot(single_fpr, single_recall, marker="o", markersize=5, markerfacecolor="red")
                        if self.output_path is not None:
                            plt.savefig(os.path.join(self.output_path, f"{c}_blade_{leng}_roc.png"))

                    table = Table(title=f"Blade Length Analysis {c}")
                    table.add_column("blade Length", justify="left", style="cyan", no_wrap=True)
                    table.add_column("Total", justify="left", style="#3D59AB", no_wrap=True)
                    table.add_column("TPR", justify="left", style="#3D59AB", no_wrap=True)
                    for k, v in single_bla.items():
                        table.add_row(str(k), str(total[k]), "{:.4f}".format(v))

                    console = Console(record=True)
                    console.print(table)
                    console.save_html(self.output_path + f"/blade_length_analysis_{c}.html", inline_styles=True)
