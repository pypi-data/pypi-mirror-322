# -*- coding: utf-8 -*-
"""This module provides stages that can compute metrics like overlaps between
groundtruth and detections, or simply count detections per bag.
"""
import copy
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

from uval.stages.stage import uval_stage  # type: ignore
from uval.stages.stage_data import SupportedDatasetSpecificationData
from uval.utils.average_precision import calculate_average_precision, eleven_point_interpolated_ap
from uval.utils.iou import iou as iou_func
from uval.utils.log import logger
from uval.utils.metric_utils import bin_placement, counter_cumsum, counter_sum_norm

matplotlib.use("Agg")


class Metrics:
    """This class implements all the evaluation metrics."""

    def __init__(self, dataset, metrics_settings, output_settings, class_mappings):
        self.dataset = dataset
        dataset.load_dataset()

        self.data = None
        self.blade_length_classes = metrics_settings.BLADE_LENGTH_ANALYSIS_CLASSES
        self.blade_length_bins = metrics_settings.BLADE_LENGTH_BINS
        self.iou_threshold = metrics_settings.IOU_THRESHOLD
        self.class_mappings = class_mappings
        self.subclass_plot = output_settings.SUBCLASS_PLOT
        self.blade_length_dataset = dataset.dataset.create_blade_length_dataset(
            self.blade_length_bins, self.blade_length_classes
        )
        # class mappings need to be set before this feature:
        self.class_specific_confidence_threshold = metrics_settings.CLASS_SPECIFIC_CONFIDENCE_THRESHOLD
        self.template_file = output_settings.TEMPLATES_FILE
        self.template_file_subclass = output_settings.TEMPLATES_FILE_SUBCLASS
        if len(metrics_settings.IOU_RANGE) == 3:
            a, b, c = metrics_settings.IOU_RANGE
            self.iou_range = np.linspace(a, b, int(np.round((b - a) / c)) + 1, endpoint=True).tolist()
            self.iou_range = [round(iou, 2) for iou in self.iou_range]
            self.template_file = output_settings.TEMPLATES_FILE_RANGE
            self.template_file_subclass = output_settings.TEMPLATES_FILE_RANGE_SUBCLASS
        else:
            self.iou_range = None
        self.confidence_threshold = metrics_settings.CONFIDENCE_THRESHOLD
        self.output_path = output_settings.PATH

        self.title = output_settings.TITLE or self.output_path.split("/")[-1]

        self.report_file = output_settings.REPORT_FILE
        self.report_file_subclass = output_settings.REPORT_FILE_SUBCLASS

        self.metrics_file = output_settings.METRICS_FILE
        self.max_workers = metrics_settings.MAX_PROCESSES
        self.templates_path = output_settings.TEMPLATES_PATH
        if not os.path.exists(self.templates_path):
            message = f"The given template directory does not exist, {self.templates_path}"
            logger.error(message)
            raise IOError(message)
        self.ap_method = metrics_settings.AP_METHOD
        self.factor = metrics_settings.FACTOR

        self.ignored_classes = set()

    def evaluate(self):
        hallucination_log, basics = self.basic_metric()
        if self.blade_length_classes:
            self.blade_length_analysis(basics)
        single_recall = {basic["Class"]: basic["Single Recall"] for basic in basics}
        single_recall_subclass = {basic["Class"]: basic["Single Recall Subclass"] for basic in basics}
        confidence_for_all_classes = {basic["Class"]: basic["Conf Thresh"] for basic in basics}
        ap_metrics = self.get_average_precision(basics, method=self.ap_method)
        fscore_metrics = self.get_fscore(ap_metrics)

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
        self.plot_roc_curves(fscore_metrics)
        self.plot_precision_recall_curve(fscore_metrics)
        self.generate_report(metrics_output)
        if self.subclass_plot:
            self.generate_report_subclass(metrics_output)
        return metrics_output

    def worker(self, iou_threshold):
        _, basics = self.basic_metric(iou_threshold=iou_threshold)

        rs = [result["Single Recall"] for result in basics]
        rs_subclass = [result["Single Recall Subclass"] for result in basics]
        output_metrics = self.get_average_precision(basics)
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
        ars = self.get_average_recall(rs, iou_range)
        self.plot_recall_iou_curve(
            single_recall, single_recall_subclass, rs, rs_subclass, iou_range, classes, confidence_for_all_classes
        )

        mar = sum(ars) / len(ars)
        return aps, rs, ars, map, mar, rs_subclass

    @property
    def templates_path(self):
        return self._templates_path

    @templates_path.setter
    def templates_path(self, path):
        # os.makedirs(os.path.abspath(path), exist_ok=True)
        self._templates_path = os.path.abspath(path)

    @property
    def class_specific_confidence_threshold(self):
        return self._class_specific_confidence_threshold

    @class_specific_confidence_threshold.setter
    def class_specific_confidence_threshold(self, confidence_thresholds):
        c = {(self.class_mappings.get(k) or k): v for part in confidence_thresholds for k, v in part.items()}
        self._class_specific_confidence_threshold = c

    @property
    def output_path(self):
        return self._output_path

    @output_path.setter
    def output_path(self, path):
        os.makedirs(os.path.abspath(path), exist_ok=True)
        self._output_path = os.path.abspath(path)

    @property
    def iou_threshold(self):
        return self._iou_threshold

    @iou_threshold.setter
    def iou_threshold(self, value):
        if value < 0 or value > 1:
            raise ValueError
        self._iou_threshold = value

    @property
    def confidence_threshold(self):
        return self._confidence_threshold

    @confidence_threshold.setter
    def confidence_threshold(self, value):
        if value < 0 or value > 1:
            raise ValueError
        self._confidence_threshold = value

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

    def get_pascal_voc2012_metric(self, confidence_threshold=None) -> list:
        basics = self.basic_metric(iou_threshold=0.5, confidence_threshold=confidence_threshold)
        return self.get_average_precision(basics, method="EveryPointInterpolation")

    def get_pascal_voc2007_metric(self, confidence_threshold=None) -> list:
        basics = self.basic_metric(iou_threshold=0.5, confidence_threshold=confidence_threshold)
        return self.get_average_precision(basics, method="ElevenPointInterpolation")

    @uval_stage
    def get_average_recall(self, recalls: Dict[float, list], iou_range: List) -> List:
        class_num = len(recalls[iou_range[0]])
        average_recalls = [0] * class_num
        for c in range(class_num):
            area = 0
            for idx in range(len(iou_range) - 1):
                iou_step = iou_range[idx + 1] - iou_range[idx]
                area += iou_step * (
                    recalls[iou_range[idx]][c] + 0.5 * (recalls[iou_range[idx]][c] - recalls[iou_range[idx + 1]][c])
                )
            average_recalls[c] = area
        return average_recalls

    @uval_stage
    def get_average_precision(self, basic_metrics: List[dict], method: str = None) -> List[dict]:
        """Get the average precision. This will be used in multiple other metrics such as
        COCO or pascal voc.

        Args:
            basic_metrics (List[dict]): [description]
            method (str, optional): choice between precise (EveryPointInterpolation or None)
            or estimation (ElevenPointInterpolation). Defaults to None.

        Returns:
            List[dict]: adds ap to the each class of the output dictionaries.
        """

        if method is None:
            method = self.ap_method
        ret = []
        for err in basic_metrics:
            # Depending on the method, call the right implementation
            if method == "EveryPointInterpolation":
                [ap, mpre, mrec] = calculate_average_precision(err["recall"], err["precision"])
            else:
                [ap, mpre, mrec] = eleven_point_interpolated_ap(err["recall"], err["precision"])
            # add class result in the dictionary to be returned
            r = dict(err.items())
            r["AP"] = ap
            r["interpolated precision"] = mpre
            r["interpolated recall"] = mrec

            ret.append(r)
        return ret

    @uval_stage
    def get_fscore(self, basic_metrics: List[dict]) -> List[dict]:
        """Get the f score metrics.

        Args:
            basic_metrics (List[dict]): output of basic_metric method.
            needs to be called before this method.

        Returns:
            List[dict]: adds dict['F score'] and dict['F score soft'] to the inputs.
        """

        ret = []
        for err in basic_metrics:
            fp = err["Total FP"]
            fn = err["Total FN"]
            tp = err["Total TP"]
            f_score = (1 + self.factor**2) * tp / ((1 + self.factor**2) * tp + (self.factor**2) * fn + fp)

            fp_soft = err["Total FP soft"]
            fn_soft = err["Total FN soft"]
            tp_soft = err["Total TP soft"]
            f_score_soft = (
                (1 + self.factor**2)
                * tp_soft
                / ((1 + self.factor**2) * tp_soft + (self.factor**2) * fn_soft + fp_soft)
            )
            # add class result in the dictionary to be returned
            r = dict(err.items())
            r["F score"] = f_score
            r["F score soft"] = f_score_soft
            ret.append(r)
        return ret

    @uval_stage
    def generate_report(self, results_cluttered: dict) -> None:
        # Sample DataFrame
        range_results = copy.deepcopy(results_cluttered)
        single_results = range_results.pop("single_threshold")

        def func(row):

            highlight = "background-color: darkorange;"
            default = ""

            return [default] * (len(row) - 1) + [highlight]

        classes = []
        for res in single_results:
            res.pop("precision")
            res.pop("recall")
            res.pop("conf level")
            res.pop("FPr")
            res.pop("TP Volume")
            res.pop("FP Volume")
            res.pop("FP Image Volume")
            res.pop("FP Image Confidence")
            res.pop("interpolated precision")
            res.pop("interpolated recall")
            res.pop("failed volumes")
            res.pop("recall subclass")
            res.pop("TP Label")
            res.pop("Single Recall Bladelength")
            res.pop("recall bladelength")
            classes.append(res["Class"])
            res.pop("Class")
            res["Single Recall Subclass"] = {k:"{:.3f}".format(v) for k,v in res["Single Recall Subclass"].items()}
        # for key, value in kwargs.items():
        high_level = dict()
        range_results.pop("ap", None)
        rs = range_results.pop("rs", None)
        range_results.pop("ars", None)
        range_results.pop("iou_range", None)
        range_results.pop("rs_subclass", None)
        high_level["mar"] = range_results.pop("mar", None)

        cell_hover = {  # for row hover use <tr> instead of <td>
            "selector": "td:hover",
            "props": [("background-color", "#ffffb3")],
        }
        row_hover = {  # for row hover use <tr> instead of <td>
            "selector": "tr:hover",
            "props": [("background-color", "#ffffb3")],
        }
        sorted_idx = [i[0] for i in sorted(enumerate(classes), key=lambda x: x[1])]
        single_results_sorted = [single_results[i] for i in sorted_idx]
        df = pd.DataFrame(single_results_sorted, index=pd.Index(sorted(classes)))

        styler = (
            df.style.set_caption(f"Calculated metrics for iou:{self.iou_threshold}")
            # .set_precision(2)
            .format(precision=3).set_table_styles([row_hover])
        )
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=self.templates_path))
        template = env.get_template(self.template_file)
        total_images = []

        for cls in sorted(classes):
            img_names = []
            img_names.append("." + "/" + cls + "_roc.png")
            img_names.append("." + "/" + cls + "_precision_recall.png")
            if self.iou_range:
                img_names.append("." + "/" + cls + "_recall_iou.png")
            total_images.append(img_names)

        if self.iou_range:
            high_level["map"] = sum(range_results["map"].values()) / len(range_results["map"])
            range_results["map"]["Total"] = high_level["map"]
            df2 = pd.DataFrame(
                [range_results["map"].values()],
                index=pd.Index(["map"]),
                columns=[str(k) for k in range_results["map"].keys()],
            )
            rs_sorted = {str(key): [val[i] for i in sorted_idx] for key, val in rs.items()}
            df_rs = pd.DataFrame(rs_sorted, index=pd.Index(sorted(classes)))
            styler_rs = (
                df_rs.style.set_caption("Recall values for all classes and all IOU thresholds")
                .format(precision=2)
                .set_table_styles([row_hover])
            )

            styler2 = (
                df2.style.set_caption("Mean average precision for various IOU levels.")
                .format(precision=2)
                .set_table_styles([cell_hover])
                .apply(func, subset=["Total"], axis=1)
            )

            # Template handling

            html = template.render(
                range_table=styler2.to_html(),
                single_table=styler.to_html(),
                rs_table=styler_rs.to_html(),
                total_images=total_images,
                mar=round(high_level["mar"], 2),
                mean_ap=round(high_level["map"], 2),
                title=self.title,
            )
        else:
            html = template.render(single_table=styler.to_html(), total_images=total_images, title=self.title)
            # Template handling

        # Write the HTML file
        with open(os.path.join(self.output_path, self.report_file), "w") as f:
            f.write(html)
        logger.info(f"Report saved to {os.path.join(self.output_path, self.report_file)}.")

    @uval_stage
    def generate_report_subclass(self, results_cluttered: dict) -> None:
        # Sample DataFrame

        single_results = [res["Single Recall Subclass"] for res in results_cluttered["single_threshold"]]

        def func(row):

            highlight = "background-color: darkorange;"
            default = ""

            return [default] * (len(row) - 1) + [highlight]

        classes = [res["Class"] for res in results_cluttered["single_threshold"]]
        row_hover = {  # for row hover use <tr> instead of <td>
            "selector": "tr:hover",
            "props": [("background-color", "#ffffb3")],
        }
        sorted_idx = [i[0] for i in sorted(enumerate(classes), key=lambda x: x[1])]
        single_results_sorted = [single_results[i] for i in sorted_idx]
        chained_results = ChainMap(*single_results_sorted)
        df = pd.DataFrame(
            dict(chained_results), index=pd.Index(["single recall"])
        )  # , columns=pd.Index(list(chained_results.keys())))

        styler = (
            df.style.set_caption(f"Calculated metrics for iou:{self.iou_threshold}")
            .format(precision=3)
            .set_table_styles([row_hover])
        )
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=self.templates_path))
        template = env.get_template(self.template_file_subclass)
        total_images = []

        for sorted_result in single_results_sorted:
            for subclass in sorted_result.keys():

                img_names = []
                img_names.append("." + "/" + subclass + "_roc.png")
                if self.iou_range:
                    img_names.append("." + "/" + subclass + "_recall_iou.png")
                total_images.append(img_names)

        if self.iou_range:
            rs_sorted = {
                str(key): [val[i] for i in sorted_idx] for key, val in results_cluttered["rs_subclass"].items()
            }
            df_rs = pd.DataFrame(
                {k: ChainMap(*v).values() for k, v in rs_sorted.items()},
                index=pd.Index(ChainMap(*rs_sorted[list(rs_sorted.keys())[0]]).keys()),
            )
            styler_rs = (
                df_rs.style.set_caption("Recall values for all subclasses and all IOU thresholds")
                .format(precision=2)
                .set_table_styles([row_hover])
            )

            # Template handling

            html = template.render(
                single_table=styler.to_html(),
                rs_table=styler_rs.to_html(),
                total_images=total_images,
                title=self.title,
            )
        else:
            html = template.render(single_table=styler.to_html(), total_images=total_images, title=self.title)
            # Template handling

        # Write the HTML file
        with open(os.path.join(self.output_path, self.report_file_subclass), "w") as f:
            f.write(html)
        logger.info(f"Report saved to {os.path.join(self.output_path, self.report_file_subclass)}.")

    @uval_stage
    def plot_roc_curves(self, roc_metrics: List[dict], show_graphic: bool = False) -> None:
        """Plot the ROC curve for every class.

        Args:
            roc_metrics (List[dict]): Output of some basic_metric. needs to be
            called before this method.
            show_graphic (bool, optional): if True, the plot will be shown. Defaults to False.

        Raises:
            IOError: [description]
        """

        result = None
        # Each resut represents a class
        for result in roc_metrics:
            if result is None:
                raise IOError("Error:No data for this class could be found.")

            class_id = result["Class"]
            single_recall = result["Single Recall"]
            single_recall_subclass = result["Single Recall Subclass"]
            single_fpr = result["Single FPr"]
            recall = result["recall"]
            fpr = result["FPr"]
            # confidence = result["Conf Thresh"]
            plt.close()
            plt.plot(fpr, recall, label=f"ROC for IOU:{self.iou_threshold}")
            plt.xlabel("FP Rate")
            plt.ylabel("TP Rate")
            plt.title("ROC curve \nClass: %s" % str(class_id))
            plt.legend(shadow=True)
            plt.grid()
            plt.xlim([0.0, 0.2])
            plt.ylim([0.0, 1.0])
            plt.plot(single_fpr, single_recall, marker="o", markersize=5, markerfacecolor="red")
            if self.output_path is not None:
                plt.savefig(os.path.join(self.output_path, class_id + "_roc.png"))
            if show_graphic:
                plt.show(block=False)
                plt.pause(0.05)
            if self.subclass_plot:
                for sub_class, sub_rec in result["recall subclass"].items():
                    plt.close()
                    plt.plot(fpr, recall, label=class_id)
                    plt.plot(fpr, sub_rec, label=sub_class)
                    plt.xlabel("FP Rate")
                    plt.ylabel("TP Rate")
                    plt.title(f"ROC curve, Class: {str(class_id)} \nSublass: {sub_class}")
                    plt.legend(shadow=True)
                    plt.grid()
                    plt.xlim([-0.01, 0.4])
                    plt.ylim([-0.01, 1.01])
                    plt.plot(
                        single_fpr, single_recall_subclass[sub_class], marker="o", markersize=5, markerfacecolor="red"
                    )
                    plt.plot(single_fpr, single_recall, marker="o", markersize=5, markerfacecolor="red")
                    if self.output_path is not None:
                        plt.savefig(os.path.join(self.output_path, sub_class + "_roc.png"))
            plt.close()

    @uval_stage
    def plot_precision_recall_curve(
        self,
        pascal_voc_metrics: List[dict],
        show_ap: bool = True,
        show_interpolated_precision: bool = True,
        show_graphic: bool = False,
    ) -> None:
        """Plot the Precision x Recall curve for a given class.

        Args:
            pascal_voc_metrics (List[dict]): Output of some pascal voc metric. needs to be
            called before this method.
            show_ap (bool, optional): if True, the average precision value will be shown
            in the title of the graph. Defaults to False.
            show_interpolated_precision (bool, optional): if True, it will show in the plot
            the interpolated precision. Defaults to False.
            show_graphic (bool, optional): if True, the plot will be shown. Defaults to False.

        Raises:
            IOError: [description]
        """

        result = None
        # Each result represents a class
        for result in pascal_voc_metrics:
            if result is None:
                raise IOError("Error: No data for a class was found.")

            class_id = result["Class"]
            precision = result["precision"]
            single_recall = result["Single Recall"]
            single_prec = result["Single Precision"]
            recall = result["recall"]
            average_precision = result["AP"]
            mpre = result["interpolated precision"]
            mrec = result["interpolated recall"]

            plt.close()
            if show_interpolated_precision:
                if self.ap_method == "EveryPointInterpolation":
                    plt.plot(mrec, mpre, "--r", label="Interpolated precision (every point)")
                elif self.ap_method == "ElevenPointInterpolation":
                    # Uncomment the line below if you want to plot the area
                    # plt.plot(mrec, mpre, 'or', label='11-point interpolated precision')
                    # Remove duplicates, getting only the highest precision of
                    # each recall value
                    nrec = []
                    nprec = []
                    for idx in range(len(mrec)):
                        r = mrec[idx]
                        if r not in nrec:
                            idx_eq = np.argwhere(mrec == r)
                            nrec.append(r)
                            nprec.append(max(mpre[int(idx)] for idx in idx_eq))
                    plt.plot(nrec, nprec, "or", label="11-point interpolated precision")
                else:
                    raise NotImplementedError(
                        "plot_precision_recall_curve() without show_interpolated_precision is not implemented yet!"
                    )
            plt.plot(recall, precision, label=f"Precision for IOU:{self.iou_threshold}")
            plt.plot(single_recall, single_prec, marker="o", markersize=5, markerfacecolor="red")

            plt.xlabel("recall")
            plt.ylabel("precision")
            if show_ap:
                ap_str = "{0:.2f}%".format(average_precision * 100)
                plt.title("Precision x Recall curve \nClass: %s, AP: %s" % (str(class_id), ap_str))
            else:
                plt.title("Precision x Recall curve \nClass: %s" % str(class_id))
            plt.legend(shadow=True)
            plt.grid()

            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.0])
            if self.output_path is not None:
                plt.savefig(os.path.join(self.output_path, class_id + "_precision_recall.png"))

            if show_graphic:
                plt.show(block=False)
                plt.pause(0.05)
        plt.close()

    @uval_stage
    def plot_recall_iou_curve(
        self,
        single_recall: float,
        single_recall_subclass,
        recalls: Dict[float, List[float]],
        recalls_subclass,
        iou_thresholds: List[float],
        classes: List[str],
        confidence_for_all_classes: Dict[str, float],
        show_ar: bool = True,
    ) -> None:
        """Plot the Recall x IOU curve for a given class.

        Args:
            recalls (Dict[float:list]): keys are iou thresholds. value is a list of recall for each class.
            iou_thresholds: list of iou thresholds.
            classes: list containing names of all classes.
        """
        # Each result represents a class
        for index, class_id in enumerate(classes):
            recall_vector = [recalls[iou][index] for iou in iou_thresholds]

            plt.close()

            plt.plot(iou_thresholds, recall_vector, label=f"Confidence:{confidence_for_all_classes[class_id]}")
            plt.plot(self.iou_threshold, single_recall[class_id], marker="o", markersize=5, markerfacecolor="red")

            plt.xlabel("IOU")
            plt.ylabel("Recall")
            if show_ar:

                ap_str = "{0:.2f}%".format(sum(recall_vector) / len(recall_vector) * 100)
                plt.title("Recall x IOU curve \nClass: %s, AR: %s" % (str(class_id), ap_str))
            else:
                plt.title("Recall x IOU curve \nClass: %s" % str(class_id))
            plt.legend(shadow=True)
            plt.grid()
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.0])
            plt.savefig(os.path.join(self.output_path, class_id + "_recall_iou.png"))
            plt.close()
            if self.subclass_plot:
                for sub_class, sub_rec in single_recall_subclass[class_id].items():
                    recall_vector_subclass = [recalls_subclass[iou][index][sub_class] for iou in iou_thresholds]

                    plt.close()

                    plt.plot(iou_thresholds, recall_vector, label=class_id)
                    plt.plot(iou_thresholds, recall_vector_subclass, label=sub_class)

                    plt.plot(
                        self.iou_threshold, single_recall[class_id], marker="o", markersize=5, markerfacecolor="red"
                    )
                    plt.plot(self.iou_threshold, sub_rec, marker="o", markersize=5, markerfacecolor="red")

                    plt.xlabel("IOU")
                    plt.ylabel("Recall")
                    plt.title(f"Recall x IOU curve Class:{str(class_id)} \n Subclass: {sub_class}")
                    plt.legend(shadow=True)
                    plt.grid()
                    plt.xlim([0.0, 1.0])
                    plt.ylim([0.0, 1.0])
                    plt.savefig(os.path.join(self.output_path, sub_class + "_recall_iou.png"))
                    plt.close()

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
