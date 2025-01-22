"""This module is run after standalone test and reads the pickle file and generates a differential reportz"""
import os

# from collections import defaultdict
from itertools import cycle
from typing import Dict, List, cast

import jinja2
import matplotlib.colors as mcolors
import pandas as pd  # type: ignore
from matplotlib import pyplot as plt  # type: ignore

from uval.stages.stage import uval_stage  # type: ignore
from uval.utils.log import logger


class DiffReporter:
    """This class implements a comparison for atleast two methods.
    The basic UVal analysis should have been performed beforehand.
    """

    def __init__(self, models: List[Dict], cfgs) -> None:
        """init func

        Args:
            models (List[Dict]): metrics from pickle.
        """

        pallette = cycle(
            [
                "tab:blue",
                "tab:orange",
                "tab:green",
                "tab:red",
                "tab:purple",
                "tab:brown",
                "tab:pink",
                "tab:gray",
                "tab:olive",
                "tab:cyan",
            ]
        )
        self.colors = tuple(mcolors.to_rgb(next(pallette)) for _ in range(len(models)))
        self.models = models
        if all("iou_range" in model.keys() for model in models):
            self.report_type = "RANGE"
        else:
            self.report_type = "SINGLE"
        name = " vs. ".join([str(result.get("title")) for result in models])

        self.output_path = os.path.join(".", name)
        os.makedirs(os.path.join(".", name), exist_ok=True)
        threshold = {model.get("iou_threshold") for model in models}
        assert len(threshold) == 1
        self.iou_threshold = threshold.pop()
        self.models_single: List[list] = [cast(list, model.get("single_threshold")) for model in models]

        self.classes = sorted(list({result["Class"] for model in self.models_single for result in model}))
        self.subclass_plot = any(cfg.OUTPUT.SUBCLASS_PLOT for cfg in cfgs)

        self.template_file = (
            cfgs[0].OUTPUT.TEMPLATES_FILE_RANGE_DIFF
            if self.report_type == "RANGE"
            else cfgs[0].OUTPUT.TEMPLATES_FILE_DIFF
        )
        self.template_file_subclass = (
            cfgs[0].OUTPUT.TEMPLATES_FILE_RANGE_SUBCLASS_DIFF
            if self.report_type == "RANGE"
            else cfgs[0].OUTPUT.TEMPLATES_FILE_SUBCLASS_DIFF
        )
        self.templates_path = cfgs[0].OUTPUT.TEMPLATES_PATH
        self.report_file = cfgs[0].OUTPUT.REPORT_FILE_DIFF

    def run(self):
        """This function performs the comparison. plots and generates the report."""
        self.plot_roc_curves()
        self.plot_precision_recall_curve()
        if self.report_type == "RANGE":
            self.plot_recall_iou_curve()
        self.generate_report()
        # self.generate_report_subclass()

    @uval_stage
    def plot_roc_curves(self) -> None:
        """Plot the ROC curve for every class."""

        result = None
        # Each result represents a class
        for class_id in self.classes:
            plt.close()
            # subclass_data = defaultdict(dict)
            for model_single, model, color in zip(self.models_single, self.models, self.colors):
                contestant = model.get("title")

                try:
                    result = next(filter(lambda x: x["Class"] == class_id, model_single))
                    # for sub_class, sub_rec in result["recall subclass"].items():
                    # subclass_data[sub_class][contestant] = (
                    #    result["FPr"],
                    #    sub_rec,
                    #    result["Single FPr"],
                    #    result["Single Recall Subclass"][sub_class],
                    # )
                    # subclass_data[]list(result["recall subclass"].items()))
                    recall = result["recall"]
                    fpr = result["FPr"]
                    plt.plot(fpr, recall, label=f"ROC for IOU:{self.iou_threshold}, model:{contestant}", color=color)
                    plt.plot(
                        result["Single FPr"], result["Single Recall"], marker="o", markersize=5, markerfacecolor="red"
                    )
                except NameError:
                    logger.debug(f"There is no {class_id} among the classes of {contestant}.")

            plt.xlabel("FP Rate")
            plt.ylabel("TP Rate")
            plt.title("ROC curve \nClass: %s" % str(class_id))
            plt.legend(shadow=True)
            plt.grid()
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.0])

            if self.output_path is not None:
                plt.savefig(os.path.join(self.output_path, class_id + "_roc.png"))
        """
        if self.subclass_plot:
            for sub_class, plottables in subclass_data.items():
                plt.close()

                for plottable_contestant, plottable_vec, color in zip(
                    plottables.keys(), plottables.values(), self.colors
                ):
                    plt.plot(plottable_vec[0], plottable_vec[1], label=plottable_contestant)
                    plt.plot(
                        plottable_vec[2], plottable_vec[3], marker="o", markersize=5, markerfacecolor="red",
                    )
                plt.xlabel("FP Rate")
                plt.ylabel("TP Rate")
                plt.title(f"ROC curve, Class: {str(class_id)} \nSublass: {sub_class}")
                plt.legend(shadow=True)
                plt.grid()
                plt.xlim([-0.01, 0.4])
                plt.ylim([-0.01, 1.01])

                if self.output_path is not None:
                    plt.savefig(os.path.join(self.output_path, sub_class + "_roc.png"))
        """
        plt.close()

    @uval_stage
    def plot_precision_recall_curve(self) -> None:
        """Plot the Precision x Recall curve for a given class."""

        # Each result represents a class
        for class_id in self.classes:
            plt.close()
            for model, model_single, color in zip(self.models, self.models_single, self.colors):
                contestant = model["title"]
                try:
                    result = next(filter(lambda x: x["Class"] == class_id, model_single))
                    average_precision = result["AP"]
                    plt.plot(
                        result["recall"],
                        result["precision"],
                        label=f"Precision for IOU:{self.iou_threshold}, Model:{contestant}, AP={average_precision:5.3}",
                        color=color,
                    )

                    plt.plot(
                        result["Single Recall"],
                        result["Single Precision"],
                        marker="o",
                        markersize=5,
                        markerfacecolor="red",
                    )
                except NameError:
                    logger.debug(f"There is no {class_id} among the classes of {contestant}.")

            plt.xlabel("recall")
            plt.ylabel("precision")

            plt.title("Precision x Recall curve \nClass:" + class_id)
            plt.legend(shadow=True)
            plt.grid()

            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.0])
            plt.savefig(os.path.join(self.output_path, class_id + "_precision_recall.png"))

            plt.close()

    @uval_stage
    def plot_recall_iou_curve(self) -> None:
        """Plot the Recall x IOU curve for a given class."""
        # Each result represents a class
        for class_id in self.classes:

            plt.close()
            for model_single, model, color in zip(self.models_single, self.models, self.colors):
                try:
                    result = next(filter(lambda x: x["Class"] == class_id, model_single))
                    contestant = model["title"]
                    idx = [c["Class"] for c in model["single_threshold"]].index(class_id)

                    iou_thresholds = model["iou_range"]
                    recall_vector = [model.get("rs").get(iou)[idx] for iou in iou_thresholds]  # type:ignore
                    ap_str = "{0:.2f}%".format(sum(recall_vector) / len(recall_vector) * 100)

                    plt.plot(
                        iou_thresholds,
                        recall_vector,
                        label=f"Confidence:{model.get('confidence_threshold')}, Model: {contestant}, AP: {ap_str}",
                        color=color,
                    )
                    plt.plot(
                        self.iou_threshold, result["Single Recall"], marker="o", markersize=5, markerfacecolor="red"
                    )
                except NameError:
                    logger.debug(f"There is no {class_id} among the classes of {contestant}.")

            plt.xlabel("IOU")
            plt.ylabel("Recall")

            plt.title(f"Recall x IOU curve \nClass: {class_id}")

            plt.legend(shadow=True)
            plt.grid()
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.0])
            plt.savefig(os.path.join(self.output_path, class_id + "_recall_iou.png"))
            plt.close()

    @uval_stage
    def generate_report(self) -> None:
        """the report html is generated."""
        # Sample DataFrame
        color_dict = {model.get("title"): color for model, color in zip(self.models, self.colors)}
        range_results = [dict(model) for model in self.models]
        single_results = [result.pop("single_threshold") for result in range_results]
        contestants = [str(result.get("title")) for result in range_results]

        def func(row, custom_color_dict):
            style_out = []
            for item in row:
                col_int = tuple(int(256 * c) for c in custom_color_dict.get(item))
                highlight = f"color: rgb{col_int}"
                style_out.append(highlight)
                # default = ""

            return style_out

        classes = self.classes
        to_remove = [
            "precision",
            "recall",
            "FPr",
            "interpolated precision",
            "interpolated recall",
            "failed volumes",
            "conf level",
            "recall subclass",
        ]
        [r.pop(field) for field in to_remove for res in single_results for r in res]
        # [r.pop("Class") for r in res]
        # for key, value in kwargs.items():
        high_level = dict()
        to_remove = ["ap", "ars", "iou_range"]
        [r.pop(field, None) for field in to_remove for r in range_results]
        recalls = [r.pop("rs", None) for r in range_results]
        high_level["mar"] = [r.pop("mar", None) for r in range_results]

        cell_hover = {  # for row hover use <tr> instead of <td>
            "selector": "td:hover",
            "props": [("background-color", "#ffffb3")],
        }
        row_hover = {  # for row hover use <tr> instead of <td>
            "selector": "tr:hover",
            "props": [("background-color", "#ffffb3")],
        }

        sorted_idx = []
        single_results_sorted = []
        for model in single_results:
            m_cls = [m.get("Class") for m in model]
            s_idx = [i[0] for i in sorted(enumerate(m_cls), key=lambda x: x[1])]
            single_results_sorted.append([model[i] for i in s_idx])
            sorted_idx.append(s_idx)

        pd_index = [val for val in contestants for _ in range(len(classes))]
        columns = list(single_results_sorted[0][0].keys())

        df = pd.DataFrame(
            [r.values() for result in single_results_sorted for r in result], index=pd.Index(pd_index), columns=columns
        )
        df.rename_axis("Models").sort_values(by=["Class", "Models"], inplace=True)
        styler = (
            df.style.set_caption(f"Calculated metrics for iou:{self.iou_threshold}")
            # .set_precision(2)
            .format(precision=2)
            .set_table_styles([row_hover])
            .apply_index(func, custom_color_dict=color_dict, axis=0)
        )
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=self.templates_path))
        template = env.get_template(self.template_file)
        total_images = []

        for cls in classes:
            img_names = []
            img_names.append("." + "/" + cls + "_roc.png")
            img_names.append("." + "/" + cls + "_precision_recall.png")
            if self.report_type == "RANGE":
                img_names.append("." + "/" + cls + "_recall_iou.png")
            total_images.append(img_names)

        if self.report_type == "RANGE":
            for result in range_results:
                result["map"]["Total"] = sum(result["map"].values()) / len(result["map"])
            columns = list(range_results[0]["map"].keys())
            df2 = pd.DataFrame(
                [result["map"].values() for result in range_results],
                index=pd.Index(contestants),
                columns=[str(round(c, 2)) if isinstance(c, float) else c for c in columns],
            )
            rs_sorted = []
            for k in range(len(sorted_idx)):
                rs_sorted.append({key: [val[i] for i in sorted_idx[k]] for key, val in recalls[k].items()})

            pd_index = [val for val in contestants for _ in range(len(classes))]
            pd_lines = []

            for result in rs_sorted:
                for c in range(len(classes)):
                    pd_lines.append([classes[c]] + [v[c] for v in result.values()])
            df_rs = pd.DataFrame(
                pd_lines, index=pd.Index(pd_index), columns=["Class"] + [str(e) for e in list(rs_sorted[0].keys())]
            )
            df_rs.rename_axis("Models").sort_values(by=["Class", "Models"], inplace=True)

            styler_rs = (
                df_rs.style.set_caption("Recall values for all classes and all IOU thresholds")
                .format(precision=2)
                .set_table_styles([row_hover])
                .apply_index(func, custom_color_dict=color_dict, axis=0)
            )

            styler2 = (
                df2.style.set_caption("Mean average precision for various IOU levels.")
                .format(precision=2)
                .set_table_styles([cell_hover])
                .apply_index(func, custom_color_dict=color_dict, axis=0)
            )

            # Template handling

            html = template.render(
                range_table=styler2.to_html(),
                single_table=styler.to_html(),
                rs_table=styler_rs.to_html(),
                total_images=total_images,
                # mar=round(high_level["mar"][0], 2),
                mar=" vs. ".join(
                    [contestants[r] + ":" + str(round(high_level["mar"][r], 2)) for r in range(len(range_results))]
                ),
                mean_ap=" vs. ".join(
                    [
                        contestants[r] + ":" + str(round(range_results[r]["map"]["Total"], 2))
                        for r in range(len(range_results))
                    ]
                ),
                # mean_ap=round(high_level["mean_ap"][0], 2),
                title=" x ".join(contestants),
            )
        else:
            html = template.render(
                single_table=styler.to_html(), total_images=total_images, title=" x ".join(contestants)
            )
            # Template handling

        # Write the HTML file
        with open(os.path.join(self.output_path, self.report_file), "w") as f:
            f.write(html)
        logger.info(f"Report saved to {os.path.join(self.output_path, self.report_file)}.")

    @uval_stage
    def generate_report_subclass(self) -> None:
        """the report html is generated."""
        # Sample DataFrame
        color_dict = {model.get("title"): color for model, color in zip(self.models, self.colors)}
        range_results = [dict(model) for model in self.models]
        single_results = [result.pop("single_threshold") for result in range_results]
        contestants = [str(result.get("title")) for result in range_results]

        def func(row, custom_color_dict):
            style_out = []
            for item in row:
                col_int = tuple(int(256 * c) for c in custom_color_dict.get(item))
                highlight = f"color: rgb{col_int}"
                style_out.append(highlight)
                # default = ""

            return style_out

        classes = self.classes
        to_remove = [
            "precision",
            "recall",
            "FPr",
            "interpolated precision",
            "interpolated recall",
            "failed volumes",
            "conf level",
        ]
        [r.pop(field) for field in to_remove for res in single_results for r in res]
        # [r.pop("Class") for r in res]
        # for key, value in kwargs.items():
        high_level = dict()
        to_remove = ["ap", "ars", "iou_range"]
        [r.pop(field, None) for field in to_remove for r in range_results]
        recalls = [r.pop("rs", None) for r in range_results]
        high_level["mar"] = [r.pop("mar", None) for r in range_results]

        cell_hover = {  # for row hover use <tr> instead of <td>
            "selector": "td:hover",
            "props": [("background-color", "#ffffb3")],
        }
        row_hover = {  # for row hover use <tr> instead of <td>
            "selector": "tr:hover",
            "props": [("background-color", "#ffffb3")],
        }

        sorted_idx = []
        single_results_sorted = []
        for model in single_results:
            m_cls = [m.get("Class") for m in model]
            s_idx = [i[0] for i in sorted(enumerate(m_cls), key=lambda x: x[1])]
            single_results_sorted.append([model[i] for i in s_idx])
            sorted_idx.append(s_idx)

        pd_index = [val for val in contestants for _ in range(len(classes))]
        columns = list(single_results_sorted[0][0].keys())

        df = pd.DataFrame(
            [r.values() for result in single_results_sorted for r in result], index=pd.Index(pd_index), columns=columns
        )
        df.rename_axis("Models").sort_values(by=["Class", "Models"], inplace=True)
        styler = (
            df.style.set_caption(f"Calculated metrics for iou:{self.iou_threshold}")
            # .set_precision(2)
            .format(precision=2)
            .set_table_styles([row_hover])
            .apply_index(func, custom_color_dict=color_dict, axis=0)
        )
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=self.templates_path))
        template = env.get_template(self.template_file)
        total_images = []

        for cls in classes:
            img_names = []
            img_names.append("." + "/" + cls + "_roc.png")
            img_names.append("." + "/" + cls + "_precision_recall.png")
            if self.report_type == "RANGE":
                img_names.append("." + "/" + cls + "_recall_iou.png")
            total_images.append(img_names)

        if self.report_type == "RANGE":
            for result in range_results:
                result["map"]["Total"] = sum(result["map"].values()) / len(result["map"])
            columns = list(range_results[0]["map"].keys())
            df2 = pd.DataFrame(
                [result["map"].values() for result in range_results],
                index=pd.Index(contestants),
                columns=[str(round(c, 2)) if isinstance(c, float) else c for c in columns],
            )
            rs_sorted = []
            for k in range(len(sorted_idx)):
                rs_sorted.append({key: [val[i] for i in sorted_idx[k]] for key, val in recalls[k].items()})

            pd_index = [val for val in contestants for _ in range(len(classes))]
            pd_lines = []

            for result in rs_sorted:
                for c in range(len(classes)):
                    pd_lines.append([classes[c]] + [v[c] for v in result.values()])
            df_rs = pd.DataFrame(
                pd_lines, index=pd.Index(pd_index), columns=["Class"] + [str(e) for e in list(rs_sorted[0].keys())]
            )
            df_rs.rename_axis("Models").sort_values(by=["Class", "Models"], inplace=True)

            styler_rs = (
                df_rs.style.set_caption("Recall values for all classes and all IOU thresholds")
                .format(precision=2)
                .set_table_styles([row_hover])
                .apply_index(func, custom_color_dict=color_dict, axis=0)
            )

            styler2 = (
                df2.style.set_caption("Mean average precision for various IOU levels.")
                .format(precision=2)
                .set_table_styles([cell_hover])
                .apply_index(func, custom_color_dict=color_dict, axis=0)
            )

            # Template handling

            html = template.render(
                range_table=styler2.to_html(),
                single_table=styler.to_html(),
                rs_table=styler_rs.to_html(),
                total_images=total_images,
                # mar=round(high_level["mar"][0], 2),
                mar=" vs. ".join(
                    [contestants[r] + ":" + str(round(high_level["mar"][r], 2)) for r in range(len(range_results))]
                ),
                mean_ap=" vs. ".join(
                    [
                        contestants[r] + ":" + str(round(range_results[r]["map"]["Total"], 2))
                        for r in range(len(range_results))
                    ]
                ),
                # mean_ap=round(high_level["mean_ap"][0], 2),
                title=" x ".join(contestants),
            )
        else:
            html = template.render(
                single_table=styler.to_html(), total_images=total_images, title=" x ".join(contestants)
            )
            # Template handling

        # Write the HTML file
        with open(os.path.join(self.output_path, self.report_file), "w") as f:
            f.write(html)
        logger.info(f"Report saved to {os.path.join(self.output_path, self.report_file)}.")
