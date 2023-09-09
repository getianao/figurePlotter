import os
import matplotlib

if os.environ.get("DISPLAY", "") == "":
    matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import numpy as np
import seaborn as sns
from adjustText import adjust_text


def bar(
    apps,  # xaixs
    configs,  # yaxis
    values,  # data
    filename=None,
    plotSize=(16, 4),
    groups=True,
    groupsInterval=0.10,
    title=None,
    xyConfig={
        "xylabel": ["", ""],
        "xlim": [None, None],
        "ylim": [None, None],
        "labelExceedYlim": False,
        "xyscale": [None, None],
        "showxyTicksLabel": [True, True],
        "xyticksRotation": [30, 0],
        "xyticksMajorLocator": [None, None],
    },
    averageConfig={
        "plotAverage": True,
        "onlyAverage": False,
        "labelAverage": True,
        "xlabel": "Mean",
        "averageFunc": np.mean,
    },
    plotNormalizedLine=True,
    legendConfig={
        "position": "best",
        "positionOffset": (0.45, 1),
        "col": 10,
        "legend.columnspacing": 1,
        "legend.handlelength": 2,
        "legend.handletextpad": 0.8,
    },
    decimals=1,
    fontSize=12,
    colorPalette=sns.color_palette("mako", 25),
    colorHatch=None,
    edgecolor="black",
):
    averageHeightDict = {}
    maxHeight = float("-inf")
    minHeight = float("inf")
    opacity = 1
    adjust_tests = []

    fig, ax = plt.subplots(figsize=plotSize)

    if groups:
        width = (1.0 - groupsInterval) / (len(configs))
    else:
        width = 0.5

    # bar
    apps_index = np.arange(len(apps))
    if averageConfig["onlyAverage"]:
        width = 0.75
        for configId in range(len(configs)):
            ys = values[:, configId].astype("float")
            maxHeight = max(maxHeight, max(ys))
            minHeight = min(minHeight, min(ys))
            if colorHatch is not None:
                hatch = colorHatch[0]
            else:
                hatch = None
            plt.bar(
                configId,
                averageConfig["averageFunc"](ys),
                width,
                alpha=min(opacity * 1.20, 1.0),
                color=colorPalette[0],
                edgecolor=(edgecolor if edgecolor else colorPalette[0]),
                linewidth=1,
                hatch=hatch,
            )
            height = averageConfig["averageFunc"](ys) + xyConfig["ylim"][1] * 0.03
            if xyConfig["ylim"][1] is not None and height > xyConfig["ylim"][1]:
                height = xyConfig["ylim"][1] + 0.1
            label = format(
                np.round(averageConfig["averageFunc"](ys), decimals=decimals),
                "." + str(decimals) + "f",
            )
            averageHeightDict[configs[configId]] = label
            if averageConfig["labelAverage"]:
                plt.text(
                    configId,
                    height,
                    label,
                    fontsize=fontSize,
                    ha="center",
                    va="bottom",
                    rotation=0,
                    weight="bold",
                )
    else:
        for configId in range(len(configs)):
            ys = values[:, configId].astype("float")
            maxHeight = max(maxHeight, max(ys))
            minHeight = min(minHeight, min(ys))
            if colorHatch is not None:
                hatch = colorHatch[configId]
            else:
                hatch = None
            plt.bar(
                apps_index + configId * width,
                ys,
                width,
                alpha=opacity,
                color=colorPalette[configId],
                edgecolor=(edgecolor if edgecolor else colorPalette[configId]),
                linewidth=1,
                label=configs[configId],
                hatch=hatch,
            )
            # For the bar higer than ylim[1], put the label on the top of the bar.
            if xyConfig["labelExceedYlim"]:
                mask_list = [1 if x > xyConfig["ylim"][1] else 0 for x in ys]
                yss = np.multiply(mask_list, ys)
                xss = np.multiply(mask_list, apps_index + configId * width)
                for mask_bit_id in range(len(mask_list)):
                    maks_bit = mask_list[mask_bit_id]
                    if maks_bit == 1:
                        yss_label = format(
                            np.round(yss[mask_bit_id], decimals=decimals),
                            "." + str(decimals) + "f",
                        )
                        adjust_tests.append(
                            plt.text(
                                xss[mask_bit_id],
                                xyConfig["ylim"][1] + 0.1,
                                yss_label,
                                fontsize=fontSize - 4,
                                ha="center",
                                va="bottom",
                                rotation=0,
                                bbox=dict(
                                    facecolor="white",
                                    edgecolor="black",
                                    boxstyle="round",
                                    pad=0.08,
                                ),
                            )
                        )
            # average bar
            if averageConfig["plotAverage"]:
                plt.bar(
                    np.array([len(apps) + width]) + configId * width,
                    [averageConfig["averageFunc"](ys)],
                    width,
                    alpha=min(opacity * 1.20, 1.0),
                    color=colorPalette[configId],
                    edgecolor=(edgecolor if edgecolor else colorPalette[configId]),
                    linewidth=1,
                    hatch=hatch,
                )
                averageTextHeight = averageConfig["averageFunc"](ys) + 0.2
                if (
                    xyConfig["ylim"][1] is not None
                    and averageTextHeight > xyConfig["ylim"][1]
                ):
                    height = xyConfig["ylim"][1] + 0.2
                averageText = format(
                    np.round(averageConfig["averageFunc"](ys), decimals=decimals),
                    "." + str(decimals) + "f",
                )
                averageHeightDict[configs[configId]] = averageText
                if averageConfig["labelAverage"]:
                    plt.text(
                        np.array([len(apps) + width]) + configId * width,
                        averageTextHeight,
                        averageText,
                        fontsize=fontSize - 5,
                        ha="center",
                        va="bottom",
                        rotation=90,
                        weight="bold",
                    )
        if averageConfig["plotAverage"]:
            plt.axvline(
                (2 * len(apps) - 1 + (len(configs) - 1) * width + width) / 2,
                color="grey",
                linestyle="dashed",
                linewidth=1,
            )
    if plotNormalizedLine:
        plt.axhline(1, color="red", linestyle="dashed", linewidth=1)

    # if yscale == "log":
    #     ax.set_yscale("log", base=2)
    #     ax.set_yticks([0.25, 0.5, 1, 2, 4, 8, 16, 32, 64, 128], minor=False)
    #     formatter = matplotlib.ticker.LogFormatter(base=2, labelOnlyBase=False)
    #     ax.yaxis.set_major_formatter(formatter)
    # else:

    # ylim
    if xyConfig["ylim"][0] is not None and xyConfig["ylim"][1] is not None:
        plt.ylim(xyConfig["ylim"][0], xyConfig["ylim"][1])
    else:
        if minHeight >= 0:
            plt.ylim(0, maxHeight * 1.1)
        else:
            plt.ylim(minHeight * 1.1, maxHeight * 1.1)

    # xy label
    if xyConfig["xylabel"][0]:
        plt.xlabel(xyConfig["xylabel"][0], fontsize=fontSize, weight="bold")
    if xyConfig["xylabel"][1]:
        plt.ylabel(xyConfig["xylabel"][1], fontsize=fontSize, weight="bold")

    # xy ticks
    plt.yticks(fontsize=fontSize, weight="bold")
    if xyConfig["xyticksMajorLocator"][1]:
        ax.yaxis.set_major_locator(MultipleLocator(xyConfig["xyticksMajorLocator"][1]))
    if averageConfig["onlyAverage"]:
        plt.xticks(
            np.arange(len(configs)),
            configs,
            rotation=xyConfig["xyticksRotation"][0],
            ha="center",
            fontsize=fontSize,
            weight="bold",
        )
    else:
        if groups:
            if xyConfig["showxyTicksLabel"][0]:
                apps_index = np.arange(len(apps))
                if averageConfig["plotAverage"]:
                    apps.append(averageConfig["xlabel"])
                    apps_index = np.append(apps_index, len(apps_index) + width)
                # print(apps_index + (len(configs) - 1) * width * 0.5)
                plt.xticks(
                    apps_index + (len(configs) - 1) * width * 0.5,
                    apps,
                    rotation=xyConfig["xyticksRotation"][0],
                    ha="center",
                    fontsize=fontSize,
                    weight="bold",
                )
            else:
                plt.xticks([], [])
        else:
            if xyConfig["showxyTicksLabel"][0]:
                plt.xticks(
                    apps_index,
                    entries,
                    rotation=xyConfig["xyticksRotation"][0],
                    ha="right",
                )
            else:
                plt.xticks([], [])

        # plt.margins(x=0.01)

    # legend
    plt.rcParams["legend.columnspacing"] = legendConfig["legend.columnspacing"]
    plt.rcParams["legend.handlelength"] = legendConfig["legend.handlelength"]
    plt.rcParams["legend.handletextpad"] = legendConfig["legend.handletextpad"]
    plt.legend(
        loc=legendConfig["position"],
        bbox_to_anchor=legendConfig["positionOffset"],
        ncol=legendConfig["col"],
        fontsize=fontSize,
        frameon=False,
        prop={"weight": "bold"},
    )

    adjust_text(
        adjust_tests,
        ensure_inside_axes=False,
        arrowprops=dict(arrowstyle="->", color="black"),
        # expand = (1.1, 0.5),
        only_move={"explode": "xy", "pull": "xy", "static": "xy", "text": "xy"},
    )

    if title:
        plt.title(title, weight="bold")

    # border
    ax.spines["top"].set_linewidth(1.5)
    ax.spines["bottom"].set_linewidth(1.5)
    ax.spines["left"].set_linewidth(1.5)
    ax.spines["right"].set_linewidth(1.5)

    # grid
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 * 1.5, box.width, box.height])
    ax.yaxis.grid(True, linestyle="--", linewidth=0.5)  # horizontal grid
    ax.xaxis.grid(False)  # horizontal grid

    plt.margins(x=0.01, tight=True)
    # plt.tight_layout()
    if filename:
        plt.savefig(filename, format="pdf", bbox_inches="tight")
    else:
        plt.show()
    plt.clf()
    plt.close("all")

    print("maxHeight", "%.2f" % maxHeight)
    print("minHeight", "%.2f" % minHeight)
    print("averageHeight", averageHeightDict)
