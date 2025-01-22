import os
from datetime import datetime
from os import path

import randomname  # type: ignore
from fvcore.common.config import CfgNode as CN  # type: ignore

# -----------------------------------------------------------------------------
# Config definition
# -----------------------------------------------------------------------------
CPUS = os.cpu_count() or 1
UVAL_DIR = path.abspath(path.join(path.dirname(__file__), "..", "..", ".."))
_C = CN()

_C.ENV = CN()
_C.ENV.CACHE_FOLDER = UVAL_DIR

_C.DATA = CN()
_C.DATA.PATH = path.join(UVAL_DIR, "data", "hdf5")
_C.DATA.IGNORE_MISSING_FILES = True
_C.DATA.MAX_THREADS = CPUS
_C.DATA.CLASS_MAPPINGS = ({},)
_C.DATA.MINIMUM_SCORE = 0.0
_C.DATA.SCORE_NAME = None


_C.DATA_SPLIT = CN()
_C.DATA_SPLIT.YAML = path.join(UVAL_DIR, "data", "datasplit", "uval_ds.yaml")
_C.DATA_SPLIT.SUBSET = ["train", "test"]

_C.METRICS = CN()
# f-{factor] score
_C.METRICS.FACTOR = 1
_C.METRICS.IOU_THRESHOLD = 0.3
_C.METRICS.IOU_RANGE = (0,)
_C.METRICS.SCAN_LEVEL_2D = False
_C.METRICS.MAX_PROCESSES = CPUS
_C.METRICS.CONFIDENCE_THRESHOLD = 0.6
_C.METRICS.AP_METHOD = "EveryPointInterpolation"
_C.METRICS.CLASS_SPECIFIC_CONFIDENCE_THRESHOLD = ({},)
_C.METRICS.BLADE_LENGTH_ANALYSIS_CLASSES = []
_C.METRICS.BLADE_LENGTH_BINS = [35, 40, 50, 60, 70, 80, 85, 90, 100, 120]
tt = datetime.now()

_C.OUTPUT = CN()
_C.OUTPUT.PATH = path.abspath(path.join(UVAL_DIR, "output", tt.strftime("%Y%m%d%H%M%S")))
_C.OUTPUT.TITLE = randomname.get_name()
_C.OUTPUT.TEMPLATES_PATH = path.abspath(path.join(UVAL_DIR, "src", "uval", "templates"))
_C.OUTPUT.TEMPLATES_FILE = "template.html"
_C.OUTPUT.TEMPLATES_FILE_RANGE = "template_range.html"
_C.OUTPUT.TEMPLATES_FILE_DIFF = "template_diff.html"
_C.OUTPUT.TEMPLATES_FILE_RANGE_DIFF = "template_range_diff.html"
_C.OUTPUT.TEMPLATES_FILE_SUBCLASS = "template_subclass.html"
_C.OUTPUT.TEMPLATES_FILE_RANGE_SUBCLASS = "template_range_subclass.html"
_C.OUTPUT.TEMPLATES_FILE_SUBCLASS_DIFF = "template_diff_subclass.html"
_C.OUTPUT.TEMPLATES_FILE_RANGE_SUBCLASS_DIFF = "template_range_diff_subclass.html"
_C.OUTPUT.CONFIG_FILE = "config.yaml"
_C.OUTPUT.SUBCLASS_PLOT = True
_C.OUTPUT.REPORT_FILE = "report.html"
_C.OUTPUT.REPORT_FILE_DIFF = "report_diff.html"
_C.OUTPUT.REPORT_FILE_SUBCLASS = "report_subclass.html"
_C.OUTPUT.REPORT_FILE_SUBCLASS_DIFF = "report_subclass_diff.html"
_C.OUTPUT.METRICS_FILE = "metrics.pickle"
_C.OUTPUT.CACHE_FILE = "data_cache.pickle"
_C.OUTPUT.DATASET_OVERVIEW_FILE = "dataset_overview.csv"
