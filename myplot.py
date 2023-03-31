import matplotlib
import os
if os.environ.get('DISPLAY', '') == '':
  matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns


def bar(apps, configs, values, ylabel: str, 
        filename=None, groups=True, groupsInterval = 0.10, title=None, plotSize=(16, 4), 
        plotAverage=True, labelAverage=True, averageXlabel = "Mean", averageFunc=np.mean, decimals=1, fontSize = 14,
        yscale = None, ylim = None, 
        colorPalette=sns.color_palette("mako", 25),  colorHatch=None, 
        edgecolor="black", showXAxis=True, legendPosition='best', plotConfig = None):
   averageHeightDict = {}
   maxHeight = float('-inf')
   minHeight = float('inf')
   opacity = 0.75
   
   fig, ax = plt.subplots(figsize=plotSize)
   
   apps_index = np.arange(len(apps))
   # print(apps_index)

   if groups:
      width = (1.0 - groupsInterval)/(len(configs))
   else:
      width = 0.5

   for configId in range(len(configs)):
      ys = values[:, configId].astype('float')
      maxHeight = max(maxHeight, max(ys))
      minHeight = min(minHeight, min(ys))
      
      if colorHatch is not None:
         hatch = colorHatch[configId]
      else:
         hatch = None
      plt.bar(apps_index+configId*width, ys, width,
              alpha=opacity, color=colorPalette[configId],
              edgecolor=(edgecolor if edgecolor else colorPalette[configId]),
              linewidth=1, label=configs[configId], hatch = hatch)
      if plotAverage:
         print(np.array([len(apps)])+configId*width)
         plt.bar(np.array([len(apps)])+configId*width, [averageFunc(ys)], width,
                 alpha=min(opacity*1.20, 1.0), color=colorPalette[configId],
                 edgecolor=(edgecolor if edgecolor else colorPalette[configId]),
                 linewidth=1, hatch = hatch)
         height = averageFunc(ys) + 0.2
         if ylim is not None and height > ylim[1]:
            height = ylim[1]+0.1 
         label = format(np.round(averageFunc(
             ys), decimals=decimals), "."+str(decimals)+"f")
         averageHeightDict[configs[configId]] = label
         if labelAverage:
            plt.text(np.array([len(apps)])+configId*width, height, label, fontsize=fontSize - 2, ha='center', va='bottom', rotation=90)
   if plotAverage:
      plt.axvline((2*len(apps)-1+(len(configs)-1)*width)/2, color='grey',
                  linestyle='dashed', linewidth=1)


   box = ax.get_position()
   ax.set_position([box.x0, box.y0*1.5, box.width, box.height])
   ax.yaxis.grid(True)  # horizontal grid
   ax.xaxis.grid(False)  # horizontal grid
   
   if yscale == "log":
      ax.set_yscale('log', base=2)
      ax.set_yticks([0.25, 0.5, 1, 2, 4, 8, 16, 32, 64, 128], minor=False)
      formatter = matplotlib.ticker.LogFormatter(base=2, labelOnlyBase=False)
      ax.yaxis.set_major_formatter(formatter)
   else:
      if ylim is not None:
         plt.ylim(ylim[0], ylim[1])
         # plt.ylim(0, 10.5)
         # plt.ylim(-1, 6.25)
      else:
         if minHeight >= 0:
            plt.ylim(0, maxHeight*1.1)
         else:
            plt.ylim(minHeight*1.1, maxHeight*1.1)

   plt.ylabel(ylabel, fontsize=fontSize)

   # ticks
   if groups:
      plt.yticks(fontsize=fontSize)
      if showXAxis:
         if plotAverage:
            apps.append(averageXlabel)
            apps_index = np.arange(len(apps))
         plt.xticks(apps_index + (len(configs)-1)*width*0.5,
                    apps, rotation=60, ha='center', fontsize=fontSize)
      else:
         plt.xticks([], [])
   else:
      if showXAxis:
         plt.xticks(apps_index, entries, rotation=30, ha='right')
      else:
         plt.xticks([], [])
         
   plt.margins(x=0.01)


   # legend
   # plt.legend(loc='lower right',fontsize=14)
   # plt.legend(loc='upper left',fontsize=14)
   # plt.legend(loc=legendPosition,fontsize=14, ncol=3)
   # plt.legend(loc=legendPosition, fontsize=14)
   # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=14)
   plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1.2),
               ncol=7, fontsize=fontSize)
   # plt.legend(loc='best',fontsize=12)
   
   if title:
      plt.title(title)

   #plt.tight_layout()
   if filename:
      plt.savefig(filename, format="pdf", bbox_inches="tight")
   else:
      plt.show()
   plt.clf()
   plt.close('all')
   
   print("maxHeight", "%.2f" % maxHeight)
   print("minHeight", "%.2f" % minHeight)
   print("averageHeightDict", averageHeightDict)
