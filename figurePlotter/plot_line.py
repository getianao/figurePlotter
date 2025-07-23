import matplotlib
import os

if os.environ.get("DISPLAY", "") == "":
    matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import pandas as pd
import numpy as np
import seaborn as sns
from adjustText import adjust_text


def line(
    apps,
    configs,
    values,
    ylabel: str,
    xlabel: str,
    only_average=False,
    only_average_label=None,
    filename=None,
    groups=True,
    groupsInterval=0.10,
    title=None,
    plotSize=(16, 4),
    plotAverage=True,
    labelAverage=True,
    averageXlabel="Mean",
    averageFunc=np.mean,
    decimals=1,
    fontSize=14,
    yscale=None,
    ylim=None,
    legendPosition="best",
    legendCol=10,
    legendConfig={
        "legend.columnspacing": 1,
        "legend.handlelength": 2,
        "legend.handletextpad": 0.8,
    },
    legendPositionOffset=(0.45, 1),
    yMultipleLocator=None,
    colorPalette=[
        "#f6c143",
        "#7eaa55",
        "#4d73be",
        "#ae8dca",
        "#2bdddd",
        "#df8244",
    ],
    colorHatch=None,
    edgecolor="black",
    showXAxis=True,
    markerPalette=["o-", "s-", "^-", "v-", "+-", "x-", "*-"],
    labelAllY =False,
):
    averageHeightDict = {}
    maxHeight = float("-inf")
    minHeight = float("inf")
    opacity = 1

    fig, ax = plt.subplots(figsize=plotSize)

    apps_index = np.arange(len(apps))
    # print(apps_index)

    if groups:
        width = (1.0 - groupsInterval) / (len(configs))
    else:
        width = 0.5

    if only_average:
        y_list = []
        for configId in range(len(configs)):
            ys = values[:, configId].astype("float")
            maxHeight = max(maxHeight, averageFunc(ys))
            minHeight = min(minHeight, averageFunc(ys))
            y_list.append(averageFunc(ys))
        assert len(configs) == len(y_list)
        plt.plot(configs, y_list, "o-", color="g", label=only_average_label)
    else:
        for configId in range(len(configs)):
            ys = values[:, configId].astype("float")
            maxHeight = max(maxHeight, max(ys))
            minHeight = min(minHeight, min(ys))

            if colorHatch is not None:
                hatch = colorHatch[configId]
            else:
                hatch = None

            valueMask = np.isfinite(ys)
            plt.plot(
                (apps_index + 1)[valueMask],
                ys[valueMask],
                markerPalette[configId],
                linewidth=2,
                markersize=8,
                color=colorPalette[configId],
                label=configs[configId],
            )
            if labelAllY:
                for i in range(len(ys)):
                    plt.text(
                        apps_index[i] + 1,
                        ys[i] + (ylim[1] if ylim else maxHeight) * 0.03,
                        format(np.round(ys[i], decimals=decimals), "." + str(decimals) + "f"),
                        fontsize=fontSize,
                        ha="center",
                        va="bottom",
                        rotation=0,
                        weight="bold",
                    )
            

            # plt.bar(apps_index+configId*width, ys, width,
            #    alpha=opacity, color=colorPalette[configId],
            #    edgecolor=(edgecolor if edgecolor else colorPalette[configId]),
            #    linewidth=1, label=configs[configId], hatch = hatch)

    box = ax.get_position()
    ax.set_position([box.x0, box.y0 * 1.5, box.width, box.height])
    ax.yaxis.grid(True, linestyle="--", linewidth=0.5)  # horizontal grid
    ax.xaxis.grid(False)  # horizontal grid

    if yscale == "log":
        ax.set_yscale('log', base=2)
        # ax.set_yticks([1, 100, 10000], minor=False)
        # formatter = matplotlib.ticker.LogFormatter(base=base, labelOnlyBase=False)
        # ax.set_yscale("log", base=2)
        # ax.set_yticks([1, 8, 64, 512, 4096, 32768], minor=False)
        # formatter = matplotlib.ticker.LogFormatter(base=2, labelOnlyBase=False)
        
        # ax.yaxis.set_major_formatter(formatter)
    else:
        if ylim is not None:
            plt.ylim(ylim[0], ylim[1])
            # plt.ylim(0, 10.5)
            # plt.ylim(-1, 6.25)
        else:
            if minHeight >= 0:
                plt.ylim(0, maxHeight * 1.1)
            else:
                plt.ylim(minHeight * 1.1, maxHeight * 1.1)
    if yMultipleLocator:
        ax.yaxis.set_major_locator(MultipleLocator(yMultipleLocator))
    plt.yticks(fontsize=fontSize - 2, weight="bold")
    ax.yaxis.get_ticklocs(minor=True)
    ax.yaxis.set_tick_params(which="minor", bottom=False)
    ax.minorticks_on()
    # plt.xticks(range(0, 6), fontsize=fontSize - 2, weight="bold")
    plt.xticks(
        apps_index + 1,
        apps,
        rotation=0,
        ha="center",
        fontsize=fontSize,
        weight="bold",
    )

    plt.ylabel(ylabel, fontsize=fontSize, weight="bold")
    plt.xlabel(xlabel, fontsize=fontSize - 2, weight="bold")
    plt.margins(x=0.15)
    # plt.margins(x=0)
    

    # legend
    if legendConfig is not None:
        plt.rcParams["legend.columnspacing"] = legendConfig["legend.columnspacing"]
        plt.rcParams["legend.handlelength"] = legendConfig["legend.handlelength"]
        plt.rcParams["legend.handletextpad"] = legendConfig["legend.handletextpad"]

    # legendConfig = {'legend.columnspacing': 0.1,
    #                 'legend.handlelength': 1, 'legend.handletextpad': 0.5}

    # plt.legend(loc='lower right',fontsize=14)
    # plt.legend(loc='upper left',fontsize=14)
    # plt.legend(loc=legendPosition,fontsize=14, ncol=3)
    # plt.legend(loc=legendPosition, fontsize=14)
    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=14)
    plt.legend(
        loc="lower center",
        bbox_to_anchor=legendPositionOffset,
        ncol=legendCol,
        fontsize=fontSize,
        frameon=False,
        prop={"weight": "bold"},
    )
    # plt.legend(loc='best',fontsize=12)

    ax.spines["top"].set_linewidth(1.5)
    ax.spines["bottom"].set_linewidth(1.5)
    ax.spines["left"].set_linewidth(1.5)
    ax.spines["right"].set_linewidth(1.5)

    if title:
        plt.title(title)

    # plt.tight_layout()
    if filename:
        plt.savefig(filename, format="pdf", bbox_inches="tight")
        print(f"Saved to {filename}")
    else:
        plt.show()
    plt.clf()
    plt.close("all")

    print("maxHeight", "%.2f" % maxHeight)
    print("minHeight", "%.2f" % minHeight)
    print("averageHeightDict", averageHeightDict)
