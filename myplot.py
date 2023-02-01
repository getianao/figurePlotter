import matplotlib
import os
if os.environ.get('DISPLAY', '') == '':
  matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns


def bar(apps, configs, values, ylabel: str, 
        filename=None, groups=True, title=None, plotSize=(16, 4), ylim = None, 
        plotAverage=True, labelAverage=True, averageXlabel = "Mean", averageFunc=np.mean, decimals=1,
        colorPalette=sns.color_palette("mako", 25), 
        edgecolor="black", showXAxis=True, legendPosition='best'):
   maxHeight = float('-inf')
   minHeight = float('inf')
   opacity = 0.75
   
   fig, ax = plt.subplots(figsize=plotSize)
   
   apps_index = np.arange(len(apps))
   # print(apps_index)

   if groups:
      width = 1.0/(len(apps)+1.0)
   else:
      width = 0.5

   for configId in range(len(configs)):
      ys = values[configId]
      maxHeight = max(maxHeight, max(ys))
      minHeight = min(minHeight, min(ys))
      plt.bar(apps_index+configId*width, ys, width,
              alpha=opacity, color=colorPalette[configId],
              edgecolor=(edgecolor if edgecolor else colorPalette[configId]),
              linewidth=0.01,
              label=configs[configId])
      if plotAverage:
         plt.bar(np.array([len(apps)])+configId*width, [averageFunc(ys)], width*1.25,
                 alpha=min(opacity*1.20, 1.0), color=colorPalette[configId],
                 edgecolor=(edgecolor if edgecolor else colorPalette[configId]))
         plt.axvline((len(apps)) - width/2.0, color='grey',  linestyle='dashed', linewidth=1)
         
         height = averageFunc(ys) + 0.1
         # print(ys)
         if ylim is not None and height > ylim[1]:
            height = ylim[1]+0.1
         avg = np.round(averageFunc(ys), decimals=decimals)
         label = format(avg, "."+str(decimals)+"f")
         # print(ys, averageFunc(ys))
         if labelAverage:
            plt.text(np.array([len(apps)])+configId*width, height, label, fontsize=5,
                     ha='center', va='bottom', rotation=90)

   box = ax.get_position()
   ax.set_position([box.x0, box.y0*1.5, box.width, box.height])
   ax.yaxis.grid(True)  # horizontal grid
   ax.xaxis.grid(False)  # horizontal grid
   
   ax.set_yscale('log', base=2)
   ax.set_yticks([0.2, 1, 2, 4, 8, 16, 32, 64, 128], minor=False)
   if ylim is not None:
      plt.ylim(ylim[0], ylim[1])
      # plt.ylim(0, 10.5)
      # plt.ylim(-1, 6.25)
   else:
      if minHeight >= 0:
         plt.ylim(0, maxHeight*1.1)
      else:
         plt.ylim(minHeight*1.1, maxHeight*1.1)

   plt.ylabel(ylabel, fontsize=14)

   # ticks
   if groups:
      if showXAxis:
         if plotAverage:
            apps.append(averageXlabel)
            apps_index = np.arange(len(apps))
         plt.xticks(apps_index + (len(configs)-1)*width*0.5,
                    apps, rotation=60, ha='center', fontsize=12)
      else:
         plt.xticks([], [])
         #plt.xticks(apps_index + (len(groups)-1)*width*0.5, entries, rotation=30, ha='right')
   else:
      if showXAxis:
         plt.xticks(apps_index, entries, rotation=30, ha='right')
      else:
         plt.xticks([], [])


   # legend
   # plt.legend(loc='lower right',fontsize=14)
   # plt.legend(loc='upper left',fontsize=14)
   # plt.legend(loc=legendPosition,fontsize=14, ncol=3)
   # plt.legend(loc=legendPosition, fontsize=14)
   # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=14)
   plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.3),
               ncol=7, fontsize=12)
   #plt.legend(loc='best',fontsize=10)
   
   if title:
      plt.title(title)

   #plt.tight_layout()
   if filename:
      plt.savefig(filename, format="pdf", bbox_inches="tight")
   else:
      plt.show()
   plt.clf()
   plt.close('all')
