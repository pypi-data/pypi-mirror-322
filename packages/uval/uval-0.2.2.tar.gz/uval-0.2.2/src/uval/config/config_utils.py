import argparse
import os
from os import path

from uval.utils.log import logger


def default_argument_parser(epilog=None):
    """
    Create a parser with some common arguments used by uval users.
    Args:
        epilog (str): epilog passed to ArgumentParser describing the usage.
    Returns:
        argparse.ArgumentParser:
    """
    parser = argparse.ArgumentParser(
        epilog=epilog or """ Examples: None existent at the moment.""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--config-file", default="", metavar="FILE", help="path to config file or files, comma separated"
    )
    parser.add_argument("-v", "--verbose", action="store_true", default=False, help="show debug level logs")

    parser.add_argument(
        "opts",
        help="""
            Modify config options at the end of the command. For Yacs configs, use
            space-separated "PATH.KEY VALUE" pairs.
            For python-based LazyConfig, use "path.key=value".
        """.strip(),
        default=None,
        nargs=argparse.REMAINDER,
    )
    return parser


def get_cfg():
    """
    Get a copy of the default config.
    Returns:
        a Uval CfgNode instance.
    """
    from .defaults import _C

    return _C.clone()


def setup_from_args(args):
    """
    Create configs and perform basic setups.
    """
    cfgs = []
    config_files = args.config_file.split(",")
    # TODO: we are not covering the case where one empty and one real config are passed

    if not args.config_file:
        # if no config file provided the default settings are used.
        cfg = get_cfg()
        cfg_process(cfg)
        cfgs.append(cfg)
    else:
        # checking config files to exist.
        for cf in config_files:
            if not path.exists(cf):
                logger.error("No config file found at %s:", cf)
                raise (IOError)

    for config_file in config_files:
        if config_file:
            stem_path = path.abspath(path.join(config_file, ".."))
            cfg = get_cfg()
            if path.isfile(config_file):
                cfg.merge_from_file(config_file)
            cfg_process(cfg, stem_path, args.opts)
            cfgs.append(cfg)
    return cfgs


def cfg_process(cfg, stem_path=None, opts=None):
    if opts:
        cfg.merge_from_list(opts)
    if stem_path:
        if not path.isabs(cfg.DATA.PATH):
            cfg.DATA.PATH = path.join(stem_path, cfg.DATA.PATH)
        if not path.isabs(cfg.DATA_SPLIT.YAML):
            cfg.DATA_SPLIT.YAML = path.join(stem_path, cfg.DATA_SPLIT.YAML)
    cfg.freeze()
    os.makedirs(cfg.OUTPUT.PATH, exist_ok=True)
    cfg_str = cfg.dump()
    with open(os.path.join(cfg.OUTPUT.PATH, cfg.OUTPUT.CONFIG_FILE), "w") as f:
        f.write(cfg_str)
    logger.info(f"config file saved to {os.path.join(cfg.OUTPUT.PATH, cfg.OUTPUT.CONFIG_FILE)}.")
