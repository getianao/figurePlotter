import matplotlib
import os
if os.environ.get('DISPLAY', '') == '':
  matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns


def bar(apps, configs, values, ylabel: str, 
        filename=None, groups=True, title=None, plotSize=(16, 4),
        palette=sns.color_palette("mako", 20),
        edgecolor=None, showXAxis=True, legendPosition='best'):
   maxHeight = float('-inf')
   minHeight = float('inf')
   opacity = 0.75
   fig, ax = plt.subplots(figsize=plotSize)
   apps_index = np.arange(len(apps))

   if groups:
      width = 1.0/(len(apps)+1.0)
   else:
      width = 0.5

   for configId in range(len(configs)):
      ys = values[configId]
      maxHeight = max(maxHeight, max(ys))
      minHeight = min(minHeight, min(ys))
      plt.bar(apps_index+configId*width, ys, width,
              alpha=opacity, color=palette[configId],
              edgecolor=(edgecolor if edgecolor else palette[configId]),
              label=configs[configId])
#          if plotAverage:
#             plt.bar([len(entries)], [summary(ys)], width*1.25,
#                  alpha=min(opacity*1.20, 1.0),
#                     color=palette[idx], edgecolor=(edgecolor if edgecolor else palette[idx]))
#             height = summary(ys)

#             avg = np.round(summary(ys), decimals=decimals)
#             if decimals == 0:
#                avg = int(avg)
#             label = str(avg)
#             if labelAverage:
#                plt.text(len(entries), height, label, fontsize=12,
#                         ha='center', va='bottom', rotation=90)

#          if plotAverage:
#             plt.axvline((len(entries)-1) + width, color='grey',
#                         linestyle='dashed', linewidth=1)




   box = ax.get_position()
   ax.set_position([box.x0, box.y0*1.5, box.width, box.height])
   ax.yaxis.grid(True)  # horizontal grid
   ax.xaxis.grid(False)  # horizontal grid
   if minHeight >= 0:
      plt.ylim(0, maxHeight*1.1)
   else:
      plt.ylim(minHeight*1.1, maxHeight*1.1)
#    #plt.ylim(0, 10.5)
#    #plt.ylim(-1, 6.25)

   plt.ylabel(ylabel, fontsize=14)

#    if plotAverage:
#       entries.append('Mean')
#       apps_index = np.arange(len(entries), dtype=float)
#       #apps_index[len(entries)-1] += width*len(groups)*0.5

   
   if groups:
      if showXAxis:
         plt.xticks(apps_index + (len(configs)-1)*width*0.5,
                    apps, rotation=90, ha='center', fontsize=12)
      else:
         plt.xticks([], [])
         #plt.xticks(apps_index + (len(groups)-1)*width*0.5, entries, rotation=30, ha='right')
      #plt.legend(loc='lower right',fontsize=14)
      #plt.legend(loc='upper left',fontsize=14)
      #plt.legend(loc=legendPosition,fontsize=14, ncol=3)
      # plt.legend(loc=legendPosition, fontsize=14)
      # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=14)
      plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.25),
                 ncol=7, fontsize=12)
      #plt.legend(loc='best',fontsize=10)
   else:
      if showXAxis:
         plt.xticks(apps_index, entries, rotation=30, ha='right')
      else:
         plt.xticks([], [])

#    #plt.yticks([-20,-15,-10,-5,0,5,10,15,20])
#    #plt.yticks([-10,-5,0,5,10,15,20,25,30,35,40,45,50,55,60,65,70])
#    #plt.yticks([-1,0,1,2,3,4,5,6])

   
   if title:
      plt.title(title)

   #plt.tight_layout()
   if filename:
      plt.savefig(filename, format="pdf", bbox_inches="tight")
   else:
      plt.show()
   plt.clf()
   plt.close('all')
