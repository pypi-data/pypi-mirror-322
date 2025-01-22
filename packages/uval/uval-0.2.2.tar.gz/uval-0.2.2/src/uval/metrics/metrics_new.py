from typing import Any, Dict, Tuple


class Item:
    def __init__(self, class_name: str, params: Dict[str, Any]) -> None:
        self.class_name = class_name
        self.params = params

    def identifier(self):
        pass


class Scheduler:
    def __init__(self) -> None:
        self.pipeline = []

    def push(self, item: Tuple[Item]):
        pass


class Metric:
    def pre_requisits(self):
        pass

    def run(self, data, progress):
        pass


class BasicMetric(Metric):
    def pre_requisits(self):
        return set()

    def run(self, data, progress, iou_threshold: float = None, confidence_threshold: float = None) -> List[dict]:
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
