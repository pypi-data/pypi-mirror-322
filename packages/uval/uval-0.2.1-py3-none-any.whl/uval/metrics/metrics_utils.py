from typing import Dict, List

from uval.utils.average_precision import calculate_average_precision, eleven_point_interpolated_ap


def get_average_recall(recalls: Dict[float, list], iou_range: List) -> List:
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


def get_average_precision(basic_metrics: List[dict], method: str = "EveryPointInterpolation") -> List[dict]:
    """Get the average precision. This will be used in multiple other metrics such as
    COCO or pascal voc.

    Args:
        basic_metrics (List[dict]): [description]
        method (str, optional): choice between precise (EveryPointInterpolation or None)
        or estimation (ElevenPointInterpolation). Defaults to None.

    Returns:
        List[dict]: adds ap to the each class of the output dictionaries.
    """

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


def get_fscore(basic_metrics: List[dict], factor=1) -> List[dict]:
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
        f_score = (1 + factor**2) * tp / ((1 + factor**2) * tp + (factor**2) * fn + fp)

        fp_soft = err["Total FP soft"]
        fn_soft = err["Total FN soft"]
        tp_soft = err["Total TP soft"]
        f_score_soft = (1 + factor**2) * tp_soft / ((1 + factor**2) * tp_soft + (factor**2) * fn_soft + fp_soft)
        # add class result in the dictionary to be returned
        r = dict(err.items())
        r["F score"] = f_score
        r["F score soft"] = f_score_soft
        ret.append(r)
    return ret
