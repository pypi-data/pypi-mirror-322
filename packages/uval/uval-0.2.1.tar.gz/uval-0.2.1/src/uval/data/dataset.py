import pickle
from os import path

from uval.data.combine_files import support_dataset_with_file_paths
from uval.data.dataset_specification import load_data_split
from uval.data.hdf5 import load_evaulation_files
from uval.utils.log import logger


class UVALDATASET:
    def __init__(self, config):
        self.cache = True
        self.data_split_path = config.DATA_SPLIT.YAML
        self.subset = config.DATA_SPLIT.SUBSET
        self.class_mappings = {w: k for mapping in config.DATA.CLASS_MAPPINGS for k, v in mapping.items() for w in v}
        self.data_path = config.DATA.PATH
        self.ignore_missing_files = config.DATA.IGNORE_MISSING_FILES
        self.minimum_score = config.DATA.MINIMUM_SCORE
        self.score_name = config.DATA.SCORE_NAME
        self.output_path = config.OUTPUT.PATH
        self.output = config.OUTPUT
        self.cache_file = config.OUTPUT.CACHE_FILE
        self.prepared_data = None
        self.scan_level_2d = config.METRICS.SCAN_LEVEL_2D

    def load_data_split(self):
        dataset_dict = load_data_split(
            self.data_split_path, self.subset, output=self.output, class_mappings=self.class_mappings
        )
        return dataset_dict

    def load_hdf_files(self, data_split):
        hdf5_groundtruth, hdf5_detections, soc_data = load_evaulation_files(
            self.data_path,
            recursive=True,
            dataset=data_split,
            ignore_missing_files=self.ignore_missing_files,
        )
        return hdf5_groundtruth, hdf5_detections, soc_data

    def support_dataset(self, ground_truths, detections, negatives):
        supported_dataset = support_dataset_with_file_paths(
            ground_truths,
            detections,
            negatives,
            class_mappings=self.class_mappings,
            minimum_score=self.minimum_score,
            score_name=self.score_name,
        )
        with open(path.join(self.output_path, self.cache_file), "wb") as f:
            pickle.dump(supported_dataset, f)

        return supported_dataset

    def load_dataset(self):

        cache_path = path.join(self.output_path, self.cache_file)
        if self.cache and path.isfile(cache_path):
            with open(cache_path, "rb") as cache_pickle:
                self.dataset = pickle.load(cache_pickle)
            logger.info(f"cache pickle already exists in {cache_path}. loading...")
        else:
            data_split = self.load_data_split()
            ground_truths, detections, negatives = self.load_hdf_files(data_split)
            self.dataset = self.support_dataset(ground_truths, detections, negatives)
            with open(cache_path, "wb") as f:
                pickle.dump(self.dataset, f)
            logger.info(f"cache pickle saved in {cache_path}.")

    def data_preparations(self):
        if not self.prepared_data:
            ground_truths = self.dataset.pop_ground_truths()
            detections = self.dataset.pop_detections()
            volumes_soc = self.dataset.pop_negatives()
            classes = self.dataset.subclass_stats()
            hallucinated_classes = [c for c in self.dataset.detected_classes() if c not in classes.keys()]
            # classes = set(ground_truths.keys())
            logger.info(f"detected classes are:{set(detections.keys())}")
            logger.info(f"ground truth classes are:{classes}")
            soc_count = len(volumes_soc)
            hallucination_log = {c: [] for c in hallucinated_classes}
            for hc in hallucinated_classes:
                volumes_negative_current = set(volumes_soc)
                dects = detections.get(hc)
                for dect in iter(dects):
                    if dect.volume_id in volumes_negative_current:
                        pfr = (len(hallucination_log[hc]) + 1) / soc_count
                        hallucination_log[hc].append((dect.score, pfr))
                        volumes_negative_current.remove(dect.volume_id)
            self.prepared_data = (hallucination_log, classes, volumes_soc, ground_truths, detections, soc_count)
        return self.prepared_data
