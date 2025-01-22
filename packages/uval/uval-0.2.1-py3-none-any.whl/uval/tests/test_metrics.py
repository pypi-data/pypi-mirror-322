import unittest
from os import path

import pytest

from uval.config import get_cfg
from uval.stages.combine_files import support_dataset_with_file_paths
from uval.stages.dataset_specification import load_datasplit
from uval.stages.hdf5 import load_evaulation_files
from uval.stages.metrics import Metrics
from uval.utils.iou import boxes_intersect, get_area, get_intersection_area, get_union_areas, iou

DATA_PATH = "./data"
datasplit_subset = ["train", "test"]


@pytest.fixture
def setup():
    """
    Create configs and perform basic setups.
    """
    # parser = default_argument_parser()
    # args = parser.parse_args()
    cfg = get_cfg()
    # if args.config_file:
    #    cfg.merge_from_file(args.config_file)
    # cfg.merge_from_list(args.opts)
    cfg.freeze()
    return cfg


@pytest.fixture
def load_test_data(setup):
    class_mappings = {w: k for mapping in setup.DATA.CLASS_MAPPINGS for k, v in mapping.items() for w in v}
    dataset = load_datasplit(
        path.join(DATA_PATH, "datasplit/uval_ds.yaml"), datasplit_subset, class_mappings=class_mappings
    )
    hdf5_groundtruth, hdf5_detections, soc_data = load_evaulation_files(
        path.join(DATA_PATH, "hdf5"),
        recursive=True,
        dataset=dataset,
        ignore_missing_files=setup.DATA.IGNORE_MISSING_FILES,
    )
    print(soc_data)
    supported_dataset = support_dataset_with_file_paths(hdf5_groundtruth, hdf5_detections, soc_data)
    return Metrics(supported_dataset, setup.METRICS, setup.OUTPUT, setup.DATA.CLASS_MAPPINGS)


def test_basic_metric(load_test_data):
    print("iou th is:", load_test_data.iou_threshold)
    print("conf th is:", load_test_data.confidence_threshold)
    print("is there dataset?:", load_test_data.dataset)
    basic_metric = load_test_data.basic_metric()
    assert basic_metric is not None
    all_classes = {metric["Class"] for metric in basic_metric}
    assert len(basic_metric) == len(all_classes)
    for metric in basic_metric:
        assert (min(metric["precision"]) >= 0) & (max(metric["precision"]) <= 1)
        assert (min(metric["recall"]) >= 0) & (max(metric["recall"]) <= 1)
        assert len(metric["precision"]) == len(metric["recall"])
        assert metric["Total Positives"] > 0
        assert metric["Total Negatives"] > 0
        assert metric["Total TP"] <= metric["Total Positives"]
        assert metric["Total FP"] <= metric["Total Negatives"]
        assert metric["Total FN"] <= metric["Total Positives"]
        assert metric["Total TP soft"] <= metric["Total TP"]
        assert metric["Total FP soft"] <= metric["Total FP"]
        assert metric["Total FN soft"] >= metric["Total FN"]


def test_get_pascal_voc2012_metric(load_test_data):
    voc_007 = load_test_data.get_pascal_voc2007_metric()
    voc_012 = load_test_data.get_pascal_voc2012_metric()
    for metric7, metric12 in zip(voc_007, voc_012):
        assert metric7["AP"] > 0 and metric7["AP"] < 1
        assert metric12["AP"] > 0 and metric12["AP"] < 1
        assert metric7["AP"] == pytest.approx(metric12["AP"], 0.25)


def test_get_fscore(load_test_data):
    basic_metrics11 = load_test_data.basic_metric(iou_threshold=0.1, confidence_threshold=0.1)
    fscore_metric11 = load_test_data.get_fscore(basic_metrics11)
    for metric in fscore_metric11:
        assert metric["F score"] >= 0 and metric["F score"] <= 1
        assert metric["F score soft"] >= 0 and metric["F score soft"] <= 1

    basic_metrics91 = load_test_data.basic_metric(iou_threshold=0.9, confidence_threshold=0.1)
    for metric11, metric91 in zip(basic_metrics11, basic_metrics91):
        assert metric11["Total TP"] >= metric91["Total TP"]

    basic_metrics15 = load_test_data.basic_metric(iou_threshold=0.1, confidence_threshold=0.9)
    for metric11, metric15 in zip(basic_metrics11, basic_metrics15):
        assert metric11["Total TP"] > metric15["Total TP"]


def test_generate_report(load_test_data):
    load_test_data.evaluate()
    assert path.isfile(path.join(load_test_data.output_path, load_test_data.report_file))


class TestIOU(unittest.TestCase):
    def test_area(self):
        assert get_area([1, 2, 3]) == 6

    def test_intersection_area(self):
        assert get_intersection_area([0, 0, 0], [2, 3, 4], [1, 1, 1], [3, 2, 1]) == 2

    def test_union_area(self):
        assert get_union_areas([0, 0, 0], [2, 3, 4], [1, 1, 1], [3, 2, 1]) == 28

    def test_intersect(self):
        assert boxes_intersect([0, 0, 0], [1, 1, 1], [1, 1, 1], [1, 1, 1]) is True
        assert boxes_intersect([0, 0, 0], [1, 1, 1], [2, 1, 1], [1, 1, 1]) is False
        assert boxes_intersect([0, 0, 0], [1, 1, 1], [1, 2, 1], [1, 1, 1]) is False
        assert boxes_intersect([0, 0, 0], [1, 1, 1], [1, 1, 2], [1, 1, 1]) is False
        assert boxes_intersect([3, 0, 0], [1, 1, 1], [1, 1, 1], [1, 1, 1]) is False
        assert boxes_intersect([0, 3, 0], [1, 1, 1], [1, 1, 1], [1, 1, 1]) is False
        assert boxes_intersect([0, 0, 3], [1, 1, 1], [1, 1, 1], [1, 1, 1]) is False

    def test_iou(self):
        assert iou([-1, 0, 0], [2, 3, 4], [1, 1, 1], [3, 2, 1]) == 0
        assert iou([3, 0, 0], [1, 1, 1], [1, 1, 1], [1, 1, 1]) == 0
        assert iou([1, 1, 1], [2, 3, 4], [2, 2, 2], [3, 2, 1]) == (2.0 / (30.0 - 2.0))
