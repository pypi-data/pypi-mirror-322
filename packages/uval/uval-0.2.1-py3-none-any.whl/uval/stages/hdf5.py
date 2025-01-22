# -*- coding: utf-8 -*-
"""This module include stages that are used to find and load HDF5 files from disk.
The result will be returned as a dictionary object
"""

from glob import glob  # type: ignore
from os import path  # type: ignore
from typing import Dict, List, Tuple  # type: ignore

from uval.stages.stage import uval_stage  # type: ignore
from uval.utils.log import logger  # type: ignore


def compare_list_to_dict(list_of_files, folder_path, file_filter, ignore_missing_files=False, recursive=True):
    if not list_of_files:
        return []
    if recursive:
        file_list_pre = glob(path.join(folder_path, "**", file_filter), recursive=True)
    else:
        file_list_pre = glob(path.join(folder_path, file_filter), recursive=False)
    what_is = {f.split("/")[-1] for f in file_list_pre}
    what_shouldve_been = {f.split("/")[-1] for f in list_of_files}
    if len(what_shouldve_been - what_is):
        logger.debug(f"These files were never found:{what_shouldve_been - what_is}")
    what_is_left = what_shouldve_been - (what_shouldve_been - what_is)
    file_dict = {f.split("/")[-1].split(".")[0]: f for f in file_list_pre if f.split("/")[-1] in what_is_left}
    if not ignore_missing_files and len(what_shouldve_been - what_is):
        raise IOError(f"HDF5 file does not exist: {what_shouldve_been - what_is}")
    # Find all HDF5 files that could be relevant
    logger.debug(file_dict)
    return file_dict


@uval_stage
def load_gt(folder_path: str, recursive: bool = False, dataset=None, ignore_missing_files: bool = False):
    """Ground truth in non negative images are loaded based on the YAML file.

    Args:
        folder_path (str): path to the data.
        recursive (bool, optional): set to True if subdirectories should also be searched. Defaults to False.
        dataset ([DatasetSpecificationData], optional): The dataset that was loaded from YAML files. Defaults to None.
        ignore_missing_files: If a HDF5 file is missing, no error is raised

    Raises:
        Exception: if a file includes in the dataset but not in the directory (sanity check).

    Returns:
        gt_files: Ground truths in positive images.
    """

    list_of_files = []
    list_of_labels = []
    if dataset:
        list_of_files = [v["volume_id"] for v in dataset.values() if not v["is_negative"]]
        list_of_labels = [v["label_id"] for v in dataset.values() if not v["is_negative"]]
        list_of_classnames = [v["class_name"] for v in dataset.values() if not v["is_negative"]]

    gt_labels: Dict[str, List[Tuple]] = {}
    single_label = []
    for f, l, c in zip(list_of_files, list_of_labels, list_of_classnames):
        single_label = gt_labels.get(f, [])
        single_label.append((l, c))
        gt_labels[f] = single_label

    file_list_full = [path.join(folder_path, f"{file}.gt.h5") for file in list_of_files]

    files_gt = compare_list_to_dict(
        list_of_files=file_list_full,
        folder_path=folder_path,
        file_filter="*.gt.h5",
        ignore_missing_files=ignore_missing_files,
        recursive=recursive,
    )
    return files_gt, gt_labels


@uval_stage
def load_detections(folder_path: str, recursive: bool = False, dataset=None, ignore_missing_files=False) -> Dict:
    """Detections in non negative images are loaded based on the YAML file.

    Args:
        folder_path (str): path to the data.
        recursive (bool, optional): set to True if subdirectories should also be searched. Defaults to False.
        dataset ([DatasetSpecificationData], optional): The dataset that was loaded from YAML files. Defaults to None.
        ignore_missing_files: If a HDF5 file is missing, no error is raised

    Raises:
        Exception: if a file includes in the dataset but not in the directory (sanity check).

    Returns:
        files_det: Detections in positive images.
    """
    list_of_files = []
    if dataset:
        list_of_files = [v["volume_id"] for v in dataset.values() if not v["is_negative"]]

    file_list_full = [path.join(folder_path, f"{file}.det.h5") for file in list_of_files]

    return compare_list_to_dict(
        list_of_files=file_list_full,
        folder_path=folder_path,
        file_filter="*.det.h5",
        ignore_missing_files=ignore_missing_files,
        recursive=recursive,
    )


@uval_stage
def load_negatives(
    folder_path: str, recursive: bool = False, dataset: Dict = None, ignore_missing_files: bool = False
) -> Dict:
    """Detections in negative images are loaded based on the YAML file.

    Args:
        folder_path (str): path to the data.
        recursive (bool, optional): set to True if subdirectories should also be searched. Defaults to False.
        dataset ([DatasetSpecificationData], optional): The dataset that was loaded from YAML files. Defaults to None.
        ignore_missing_files: If a HDF5 file is missing, no error is raised

    Raises:
        Exception: if a file includes in the dataset but not in the directory (sanity check).

    Returns:
        files_soc: Detections in Negative images.
    """
    list_of_files = []
    if dataset:
        list_of_files = [v["volume_id"] for v in dataset.values() if v["is_negative"]]
    file_list_full = [path.join(folder_path, f"{file}.det.h5") for file in list_of_files]

    return compare_list_to_dict(
        list_of_files=file_list_full,
        folder_path=folder_path,
        file_filter="*.det.h5",
        ignore_missing_files=ignore_missing_files,
        recursive=recursive,
    )


@uval_stage
def load_evaulation_files(
    folder_path: str, recursive=False, dataset=None, ignore_missing_files=False
) -> Tuple[Tuple, Dict, Dict]:
    """This is a wrapper that calls underlying functions and loads positive
    detections, GTs and negative detections.

    Args:
        folder_path (str): path to the data folder.
        recursive (bool, optional): set to True if subdirectories should also be searched. Defaults to False.
        dataset ([DatasetSpecificationData], optional): The input dataset
        loaded from YAML file. Defaults to None.
        ignore_missing_files: If a HDF5 file is missing, no error is raised

    Returns:
        (detections, groundtruths, negatives): Tuple including all three parts of the dataset.
    """
    neg = {v["volume_id"] for v in dataset.values() if v["is_negative"]}
    pos = {v["volume_id"] for v in dataset.values() if not v["is_negative"]}
    if len(neg & pos) > 0:
        raise ValueError("The positive and negative subsets have overlap.")

    files_det = load_detections(
        # path.join(folder_path, "detections"), recursive, dataset, ignore_missing_files, max_workers=max_workers
        folder_path,
        recursive,
        dataset,
        ignore_missing_files,
    )

    files_gt, labels_gt = load_gt(
        # path.join(folder_path, "raw"), recursive, dataset, ignore_missing_files, max_workers=max_workers
        folder_path,
        recursive,
        dataset,
        ignore_missing_files,
    )
    files_soc = load_negatives(
        # path.join(folder_path, "detections"), recursive, dataset, ignore_missing_files, max_workers=max_workers
        folder_path,
        recursive,
        dataset,
        ignore_missing_files,
    )
    return (files_gt, labels_gt), files_det, files_soc
