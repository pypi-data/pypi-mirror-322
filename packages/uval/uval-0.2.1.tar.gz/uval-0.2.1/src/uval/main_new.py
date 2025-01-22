"""This module performs testing in UVAL style"""
import hashlib
import logging
import pickle
import shutil
import time
from os import path
from typing import Any

from rich.console import Console
from rich.traceback import install

from uval import (
    Metrics,
    default_argument_parser,
    get_context,
    load_datasplit,
    load_evaulation_files,
    setup_from_args,
    support_dataset_with_file_paths,
)
from uval.data.dataset import UVALDATASET
from uval.metrics.metrics import Metrics3D
from uval.plotting.plotter import BasicPlotter, RangePlotter
from uval.reporting.reporter import Reporter
from uval.stages.diff_reporter import DiffReporter
from uval.utils.log import logger

console = Console(record=True)
install()


def main() -> None:
    """This function is the core of Uval. Everything starts here"""
    parser = default_argument_parser()
    args = parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    logger.info("Command Line Args: %s", args)

    cfgs = setup_from_args(args)
    for cfg in cfgs:
        single(cfg)

    if len(cfgs) > 1:
        logger.info("initiating the generation of a differential report...")
        # the contents of the dataset and the splits should match
        # otherwise comparison is meaningless
        # the metrics should also match
        md5_hash = {hashlib.md5(bytes(str(dict(cfg.METRICS).pop("MAX_PROCESSES")), "UTF-8")).digest() for cfg in cfgs}

        results = []
        if len(set(md5_hash)) != 1:
            logger.error("UVAL proudly refuses to compare apples and oranges!")
            return 1

        for cfg in cfgs:
            filename = path.join(cfg.OUTPUT.PATH, cfg.OUTPUT.METRICS_FILE)
            with open(filename, "rb") as pickle_file:
                results.append(pickle.load(pickle_file))
        logger.info("loaded")
        reporter = DiffReporter(results, cfgs)
        reporter.run()
        try:
            shutil.copyfile("log-file.log", f"{cfg.OUTPUT.PATH}/log-file.log")
        except Exception:
            print("no log-file.log found")
            logger.warning(Exception)
    return 0


def single(cfg: Any) -> None:
    """Perform uval analysis on a single configuration/standalone testing.

    Args:
        cfg (Any): config file
    """
    if path.isfile(path.join(cfg.OUTPUT.PATH, cfg.OUTPUT.METRICS_FILE)):
        logger.info("metrics pickle already exists. skipping the evaluation...")
        return
    logger.debug(cfg)
    ctx = get_context(cfg.DATA.MAX_THREADS)
    ctx.set_cache_folder(cfg.ENV.CACHE_FOLDER)

    with ctx.cached():
        t0 = time.perf_counter()
        dataset = UVALDATASET(cfg)
        metrics_calculator = Metrics3D(cfg, dataset=dataset)
        plotter = BasicPlotter(cfg, metrics_calculator=metrics_calculator)
        reporter = Reporter(cfg, plotter=plotter)
        reporter.run()
        logger.info(f"Elapsed time in seconds:{time.perf_counter() - t0}")


if __name__ == "__main__":
    quit(main())
