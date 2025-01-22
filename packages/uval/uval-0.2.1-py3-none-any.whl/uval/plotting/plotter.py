from os import path
from typing import NamedTuple, Union

import matplotlib.pyplot as plt  # type: ignore

from uval.metrics.metrics import Metrics3D
from uval.utils.log import logger

# if self.subclass_plot:
#    self.generate_report_subclass(metrics_output)


class PlotVectors(NamedTuple):
    xdata: Union[float, list]
    ydata: Union[float, list]
    label: Union[str, None]
    marker: Union[str, None]
    markersize: Union[int, None]
    markerfacecolor: Union[str, None]


class Plotter:
    def __init__(self, output_path, file_name, xlabel, ylabel, title, xlim=None, ylim=None) -> None:
        self.output_path = output_path
        self.file_name = file_name
        self.data: list[PlotVectors] = []
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title
        self.xlim = xlim or [0.0, 0.2]
        self.xlim = ylim or [0.0, 1.0]

    def add_data(self, data: PlotVectors):
        self.data.append(data)

    def generate_plots(self):
        plt.close()
        for data in self.data:
            plt.plot(
                data.xdata,
                data.ydata,
                label=data.label,
                marker=data.marker,
                markersize=data.markersize,
                markerfacecolor=data.markerfacecolor,
            )
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.title(self.title)
        plt.legend(shadow=True)
        plt.grid()
        plt.xlim([0.0, 0.2])
        plt.ylim([0.0, 1.0])
        plt.savefig(path.join(self.output_path, self.file_name))
        plt.close()


class PlotOrganizer:
    def __init__(self, config, metrics_calculator: Metrics3D) -> None:
        self.plots = []
        self.metrics_calculator = metrics_calculator
        self.output_path = config.OUTPUT.PATH

    def add_plot(self, plot: Plotter):
        self.plots.append(plot)

    def run(self):
        metrics_available = self.metrics_calculator.run()
        if metrics_available:
            self.plan_plots(self.metrics_calculator.metrics)
            self.generate_plots()
            return True
        else:
            logger.info("No Metrics Available")
        return False

    def generate_plots(self):
        for plot in self.plots:
            plot.generate_plots()


class BasicPlotter(PlotOrganizer):
    def __init__(self, config, metrics_calculator) -> None:
        super().__init__(config, metrics_calculator)

    def plan_plots(self):
        for result in self.metrics["single_threshold"]:

            plotter_roc = Plotter(
                self.output_path,
                f"{result['Class']}_roc.png",
                "FP Rate",
                "TP Rate",
                f"ROC curve \nClass: {result['Class']}",
            )
            plotter_roc.add_data(
                PlotVectors(
                    result["FPr"], result["recall"], f"ROC for IOU:{self.metrics['iou_threshold']}", None, None, None
                )
            )
            plotter_roc.add_data(PlotVectors(result["Single FPr"], result["Single Recall"], None, "o", 5, "red"))
            plotter_pr = Plotter(
                self.output_path,
                f"{result['Class']}_precision_recall.png",
                "Recall",
                "Precision",
                f"Precision x Recall curve \nClass: {result['Class']}, AP: {result['AP']}",
                [0.0, 1.0],
                [0.0, 1.0],
            )
            plotter_pr.add_data(
                PlotVectors(
                    result["recall"],
                    result["precision"],
                    f"Precision for IOU:{self.metrics['iou_threshold']}",
                    None,
                    None,
                    None,
                )
            )
            plotter_pr.add_data(PlotVectors(result["Single Recall"], result["Single Precision"], None, "o", 5, "red"))
            self.add_plot(plotter_roc)
            self.add_plot(plotter_pr)


class RangePlotter(PlotOrganizer):
    def __init__(self) -> None:
        super().__init__()

    def plan_plots(self):
        for result in self.metrics["single_threshold"]:

            plotter_recall_iou = Plotter(
                self.output_path,
                f"{result['Class']}_roc.png",
                "FP Rate",
                "TP Rate",
                f"ROC curve \nClass: {result['Class']}",
            )
            plotter_recall_iou.add_data(
                PlotVectors(
                    result["FPr"], result["recall"], f"ROC for IOU:{self.metrics['iou_threshold']}", None, None, None
                )
            )
            plotter_recall_iou.add_data(PlotVectors(result["Single FPr"], result["Single Recall"], None, "o", 5, "red"))
            self.add_plot(plotter_recall_iou)


class SubclassBasicPlotter(PlotOrganizer):
    def __init__(self, metrics, output_path) -> None:
        super().__init__(metrics, output_path)

    def plan_plots(self):
        for result in self.metrics["single_threshold"]:
            for sub_class, sub_rec in result["recall subclass"].items():

                plotter_roc_class = Plotter(
                    self.output_path,
                    f"{sub_class} _roc.png",
                    "FP Rate",
                    "TP Rate",
                    f"ROC curve \nClass: {result['Class']} \nSublass: {sub_class}",
                )
                plotter_roc_class.add_data(
                    PlotVectors(result["FPr"], result["recall"], result["Class"], None, None, None)
                )
                plotter_roc_class.add_data(PlotVectors(result["FPr"], sub_rec, sub_class, None, None, None))
                plotter_roc_class.add_data(
                    PlotVectors(result["Single FPr"], result["Single Recall Subclass"][sub_class], None, "o", 5, "red")
                )
                plotter_roc_class.add_data(
                    PlotVectors(result["Single FPr"], result["Single Recall"], None, "o", 5, "red")
                )

                self.add_plot(plotter_roc_class)


class DiffPlotter(PlotOrganizer):  # TODO
    def __init__(self) -> None:
        super().__init__()

    def plan_plots(self):
        pass
