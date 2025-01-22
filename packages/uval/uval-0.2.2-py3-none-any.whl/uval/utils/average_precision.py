from typing import Any, List, Union

import numpy as np


def calculate_average_precision(rec: List[float], prec: List[float]) -> List[Any]:
    assert len(rec) == len(prec)
    mrec = [0.0] + list(rec) + [1.0]
    mpre = [1.0] + list(prec) + [0.0]
    for i in range(len(mpre) - 1, 0, -1):
        mpre[i - 1] = max(mpre[i - 1], mpre[i])
    ii = [i + 1 for i in range(len(mrec) - 1) if mrec[1 + i] != mrec[i]]
    ap: Union[float, Any] = 0.0
    for i in ii:
        ap = ap + np.sum((mrec[i] - mrec[i - 1]) * mpre[i])
    return [ap, mpre[:-1], mrec[: len(mpre) - 1]]


# 11-point interpolated average precision
def eleven_point_interpolated_ap(rec: List[float], prec: List[float]) -> List[Any]:
    mrec = list(rec)
    mpre = list(prec)
    recall_values_np = np.linspace(0, 1, 11)
    recall_values = list(recall_values_np[::-1])
    rho_interp = []
    recall_valid = []
    # For each recall_values (0, 0.1, 0.2, ... , 1)
    for r in recall_values:
        # Obtain all recall values higher or equal than r
        arg_greater_recalls = np.argwhere(mrec[:] >= r)
        pmax = 0.0
        # If there are recalls above r
        if arg_greater_recalls.size != 0:
            pmax = max(mpre[int(arg_greater_recalls.min()) :])
        recall_valid.append(r)
        rho_interp.append(pmax)
    # By definition ap = sum(max(precision whose recall is above r))/11
    ap = sum(rho_interp) / 11
    # Generating values for the plot
    rvals = [recall_valid[0]] + list(recall_valid) + [0.0]
    pvals = [0.0] + list(rho_interp) + [0.0]
    # rho_interp = rho_interp[::-1]
    cc = []
    for i in range(len(rvals)):
        p = (rvals[i], pvals[i - 1])
        if p not in cc:
            cc.append(p)
        p = (rvals[i], pvals[i])
        if p not in cc:
            cc.append(p)
    recall_values_out = [i[0] for i in cc]
    rho_interp = [i[1] for i in cc]
    return [ap, rho_interp, recall_values_out]
