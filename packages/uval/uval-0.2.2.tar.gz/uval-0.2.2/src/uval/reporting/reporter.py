import os
from collections import ChainMap

import jinja2  # type: ignore
import pandas as pd

from uval.plotting.plotter import PlotOrganizer
from uval.utils.log import logger


class Reporter:
    def __init__(self, config, plotter: PlotOrganizer):
        self.iou_range = config.METRICS.IOU_RANGE
        self.templates_path = config.OUTPUT.TEMPLATES_PATH
        self.template_file = config.OUTPUT.TEMPLATES_PATH
        self.template_file_subclass = config.OUTPUT.TEMPLATES_FILE_SUBCLASS
        self.plotter = plotter
        if not os.path.exists(self.templates_path):
            message = f"The given template directory does not exist, {self.templates_path}"
            logger.error(message)
            raise IOError(message)

    @property
    def metrics(self):
        return self._metrics

    @metrics.setter
    def metrics(self, value):
        self._metrics = value

    def run(self) -> bool:
        plots_available = self.plotter.run()
        if plots_available:
            self.generate_report()
            return True
        else:
            logger.debug("plotter failed")
            return False

    def generate_report(self) -> None:
        single_columns = [
            "Conf Thresh",
            "Single FPr",
            "Single Recall",
            "Single Precision",
            "Total Positives",
            "Total Negatives",
            "Total TP",
            "Total FP",
            "Total FN",
            "Total TP soft",
            "Total FP soft",
            "Total FN soft",
            "AP",
            "F score",
            "F score soft",
        ]

        def func(row):

            highlight = "background-color: darkorange;"
            default = ""

            return [default] * (len(row) - 1) + [highlight]

        classes = []
        single_results = []
        for res in self._metrics["single_threshold"]:
            single_results.append({col: res[col] for col in single_columns})

            classes.append(res["Class"])
        # for key, value in kwargs.items():
        high_level = dict()
        rs = self._metrics["rs"]

        high_level["mar"] = self._metrics["mar"]

        cell_hover = {  # for row hover use <tr> instead of <td>
            "selector": "td:hover",
            "props": [("background-color", "#ffffb3")],
        }
        row_hover = {  # for row hover use <tr> instead of <td>
            "selector": "tr:hover",
            "props": [("background-color", "#ffffb3")],
        }
        sorted_idx = [i[0] for i in sorted(enumerate(classes), key=lambda x: x[1])]
        single_results_sorted = [single_results[i] for i in sorted_idx]
        df = pd.DataFrame(single_results_sorted, index=pd.Index(sorted(classes)))

        styler = (
            df.style.set_caption(f"Calculated metrics for iou:{self._metrics['iou_threshold']}")
            # .set_precision(2)
            .format(precision=3).set_table_styles([row_hover])
        )
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=self.templates_path))
        template = env.get_template(self.template_file)
        total_images = []

        for cls in sorted(classes):
            img_names = []
            img_names.append("." + "/" + cls + "_roc.png")
            img_names.append("." + "/" + cls + "_precision_recall.png")
            if self.iou_range:
                img_names.append("." + "/" + cls + "_recall_iou.png")
            total_images.append(img_names)

        if self.iou_range:
            high_level["map"] = sum(self._metrics["map"].values()) / len(self._metrics["map"])
            map = self._metrics["map"]
            map["Total"] = high_level["map"]
            df2 = pd.DataFrame(
                [map.values()],
                index=pd.Index(["map"]),
                columns=[str(k) for k in map.keys()],
            )
            rs_sorted = {str(key): [val[i] for i in sorted_idx] for key, val in rs.items()}
            df_rs = pd.DataFrame(rs_sorted, index=pd.Index(sorted(classes)))
            styler_rs = (
                df_rs.style.set_caption("Recall values for all classes and all IOU thresholds")
                .format(precision=2)
                .set_table_styles([row_hover])
            )

            styler2 = (
                df2.style.set_caption("Mean average precision for various IOU levels.")
                .format(precision=2)
                .set_table_styles([cell_hover])
                .apply(func, subset=["Total"], axis=1)
            )

            # Template handling

            html = template.render(
                range_table=styler2.to_html(),
                single_table=styler.to_html(),
                rs_table=styler_rs.to_html(),
                total_images=total_images,
                mar=round(high_level["mar"], 2),
                mean_ap=round(high_level["map"], 2),
                title=self.title,
            )
        else:
            html = template.render(single_table=styler.to_html(), total_images=total_images, title=self.title)
            # Template handling

        # Write the HTML file
        with open(os.path.join(self.output_path, self.report_file), "w") as f:
            f.write(html)
        logger.info(f"Report saved to {os.path.join(self.output_path, self.report_file)}.")

    def generate_report_subclass(self) -> None:
        # Sample DataFrame

        single_results = [res["Single Recall Subclass"] for res in self._metrics["single_threshold"]]

        def func(row):

            highlight = "background-color: darkorange;"
            default = ""

            return [default] * (len(row) - 1) + [highlight]

        classes = [res["Class"] for res in self._metrics["single_threshold"]]
        row_hover = {  # for row hover use <tr> instead of <td>
            "selector": "tr:hover",
            "props": [("background-color", "#ffffb3")],
        }
        sorted_idx = [i[0] for i in sorted(enumerate(classes), key=lambda x: x[1])]
        single_results_sorted = [single_results[i] for i in sorted_idx]
        chained_results = ChainMap(*single_results_sorted)
        df = pd.DataFrame(
            dict(chained_results), index=pd.Index(["single recall"])
        )  # , columns=pd.Index(list(chained_results.keys())))

        styler = (
            df.style.set_caption(f"Calculated metrics for iou:{self._metrics['iou_threshold']}")
            .format(precision=3)
            .set_table_styles([row_hover])
        )
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=self.templates_path))
        template = env.get_template(self.template_file_subclass)
        total_images = []

        for sorted_result in single_results_sorted:
            for subclass in sorted_result.keys():

                img_names = []
                img_names.append("." + "/" + subclass + "_roc.png")
                if self.iou_range:
                    img_names.append("." + "/" + subclass + "_recall_iou.png")
                total_images.append(img_names)

        if self.iou_range:
            rs_sorted = {str(key): [val[i] for i in sorted_idx] for key, val in self._metrics["rs_subclass"].items()}
            df_rs = pd.DataFrame(
                {k: ChainMap(*v).values() for k, v in rs_sorted.items()},
                index=pd.Index(ChainMap(*rs_sorted[list(rs_sorted.keys())[0]]).keys()),
            )
            styler_rs = (
                df_rs.style.set_caption("Recall values for all subclasses and all IOU thresholds")
                .format(precision=2)
                .set_table_styles([row_hover])
            )

            # Template handling

            html = template.render(
                single_table=styler.to_html(),
                rs_table=styler_rs.to_html(),
                total_images=total_images,
                title=self.title,
            )
        else:
            html = template.render(single_table=styler.to_html(), total_images=total_images, title=self.title)
            # Template handling

        # Write the HTML file
        with open(os.path.join(self.output_path, self.report_file_subclass), "w") as f:
            f.write(html)
        logger.info(f"Report saved to {os.path.join(self.output_path, self.report_file_subclass)}.")
