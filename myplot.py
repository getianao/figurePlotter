import matplotlib
import os
if os.environ.get('DISPLAY', '') == '':
  matplotlib.use('Agg')
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import pandas as pd
import numpy as np
import seaborn as sns
from adjustText import adjust_text


def bar(apps, configs, values, ylabel: str, 
        filename=None, groups=True, groupsInterval = 0.10, title=None, plotSize=(16, 4), 
        plotAverage=True, labelAverage=True, averageXlabel = "Mean", labelExceedYlim = False,
        averageFunc=np.mean, decimals=1, fontSize = 12,
        only_average=False,
        yscale = None, ylim = None, yMultipleLocator=None,
        colorPalette=sns.color_palette("mako", 25),  colorHatch=None, 
        edgecolor="black", showXAxis=True, 
        legendPosition='best', legendCol=10, legendConfig = {'legend.columnspacing': 1,
                                                      'legend.handlelength': 2, 'legend.handletextpad': 0.8}, legendPositionOffset = (0.45, 1),
        stack = False, values2 =None, colorPalette2=None, stack_labels = None,
        ticksFrontsize = 14, ticksRotation = 30,
        plotHline = True):
   averageHeightDict = {}
   maxHeight = float('-inf')
   minHeight = float('inf')
   opacity = 1
   adjust_tests = []
   
   
   fig, ax = plt.subplots(figsize=plotSize)
   
   if groups:
      width = (1.0 - groupsInterval)/(len(configs))
   else:
      width = 0.5
            
   apps_index = np.arange(len(apps))
   # print(apps_index)
   if stack:
      if only_average:
         print("use stacks")
         width = 0.75
         stack_ys_bottom = []
         stack_ys_top = []
         for configId in range(len(configs)):
            ys = values[:, configId].astype('float')
            maxHeight = max(maxHeight, max(ys))
            minHeight = min(minHeight, min(ys))
            ys2 = values2[:, configId].astype('float')
            maxHeight = max(maxHeight, max(ys2))
            minHeight = min(minHeight, min(ys2))
            if colorHatch is not None:
               hatch = colorHatch[0]
            else:
               hatch = None
            avg_stack_bottom = averageFunc(ys)
            avg_stack_top = averageFunc(ys2+ys) - averageFunc(ys)
            stack_ys_bottom.append(avg_stack_bottom)
            stack_ys_top.append(avg_stack_top)

            height = averageFunc(ys+ys2) + ylim[1]*0.03
            if ylim is not None and height > ylim[1]:
               height = ylim[1]+0.1
            label = format(np.round(averageFunc(ys+ys2),
                           decimals=decimals), "."+str(decimals)+"f")
            averageHeightDict[configs[configId]] = label
            if labelAverage:
               plt.text(configId, height, label, fontsize=fontSize, ha='center', va='bottom', rotation=0,  weight='bold')
         # print(stack_ys_bottom, stack_ys_top)
         plt.bar(np.arange(len(configs)), stack_ys_bottom, width,
                 alpha=opacity, color=colorPalette[0],
                 edgecolor=(edgecolor if edgecolor else colorPalette[0]),
                 linewidth=1, label=stack_labels[0], hatch=hatch)
         plt.bar(np.arange(len(configs)), stack_ys_top, width,
                 alpha=opacity, color=colorPalette2[0],
                 edgecolor=(edgecolor if edgecolor else colorPalette[0]),
                 linewidth=1, label=stack_labels[1], hatch=hatch, bottom=stack_ys_bottom)
   else:
      if only_average:
         width = 0.75
         for configId in range(len(configs)):
            ys = values[:, configId].astype('float')
            maxHeight = max(maxHeight, max(ys))
            minHeight = min(minHeight, min(ys))
            if colorHatch is not None:
               hatch = colorHatch[0]
            else:
               hatch = None
            plt.bar(configId, averageFunc(ys), width,
                     alpha=min(opacity*1.20, 1.0), color=colorPalette[0],
                     edgecolor=(
                  edgecolor if edgecolor else colorPalette[0]),
                  linewidth=1, hatch=hatch)
            height = averageFunc(ys) + ylim[1]*0.03
            if ylim is not None and height > ylim[1]:
               height = ylim[1]+0.1
            label = format(np.round(averageFunc(
                  ys), decimals=decimals), "."+str(decimals)+"f")
            averageHeightDict[configs[configId]] = label
            if labelAverage:
               plt.text(configId, height, label, fontsize=fontSize, ha='center', va='bottom', rotation=0,  weight='bold')
      else:
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
            
            if labelExceedYlim:
               mask_list = [1 if x > ylim[1] else 0 for x in ys]    
               yss = np.multiply(mask_list, ys)
               xss = np.multiply(mask_list, apps_index+configId*width)
               
               for mask_bit_id in range(len(mask_list)):
                  maks_bit = mask_list[mask_bit_id]
                  if maks_bit == 1:
                     yss_label = format(np.round(yss[mask_bit_id], decimals=decimals), "."+str(decimals)+"f")
                     adjust_tests.append(plt.text(xss[mask_bit_id], ylim[1] + 0.1 , yss_label, fontsize=fontSize - 4, ha='center', va='bottom', rotation=0,  bbox=dict(facecolor='white', edgecolor='black', boxstyle='round', pad=0.08)))
                     
               
            if plotAverage:
               print(np.array([len(apps)])+configId*width)
               plt.bar(np.array([len(apps) + width])+configId*width, [averageFunc(ys)], width,
                     alpha=min(opacity*1.20, 1.0), color=colorPalette[configId],
                     edgecolor=(edgecolor if edgecolor else colorPalette[configId]),
                     linewidth=1, hatch = hatch)
               height = averageFunc(ys)+ ylim[1]*0.1
               if ylim is not None and height > ylim[1]:
                  height = ylim[1]+0.1
               label = format(np.round(averageFunc(ys), decimals=decimals), "."+str(decimals)+"f")
               averageHeightDict[configs[configId]] = label
               if labelAverage:
                  plt.text(np.array([len(apps) + width])+configId*width, height, label,
                           fontsize=fontSize - 5, ha='center', va='bottom', rotation=90, weight='bold')
         if plotAverage:
            plt.axvline((2*len(apps)-1+(len(configs)-1)*width + width)/2, color='grey',
                        linestyle='dashed', linewidth=1)

   if plotHline:
      plt.axhline(1, color='red',
                           linestyle='dashed', linewidth=1)
   box = ax.get_position()
   ax.set_position([box.x0, box.y0*1.5, box.width, box.height])
   ax.yaxis.grid(True, linestyle = '--', linewidth = 0.5)  # horizontal grid
   ax.xaxis.grid(False)  # horizontal grid
   
   if yscale == "log":
      ax.set_yscale('log', base=2)
      ax.set_yticks([0.25, 0.5, 1, 2, 4, 8, 16, 32, 64, 128], minor=False)
      formatter = matplotlib.ticker.LogFormatter(base=2, labelOnlyBase=False)
      ax.yaxis.set_major_formatter(formatter)
   else:
      if ylim is not None:
         plt.ylim(ylim[0], ylim[1])
      else:
         if minHeight >= 0:
            plt.ylim(0, maxHeight*1.1)
         else:
            plt.ylim(minHeight*1.1, maxHeight*1.1)
      if yMultipleLocator:
         ax.yaxis.set_major_locator(MultipleLocator(yMultipleLocator))

   plt.ylabel(ylabel, fontsize=fontSize, weight='bold')

   # ticks
   plt.yticks(fontsize=fontSize, weight='bold')
   if only_average:
       plt.xticks(np.arange(len(configs)),
                  configs, rotation=ticksRotation, ha='center', fontsize=fontSize, weight='bold')
   else:
      if groups:
         if showXAxis:
            apps_index = np.arange(len(apps))
            if plotAverage:
               apps.append(averageXlabel)
               apps_index = np.append(apps_index, len(apps_index)+width)
            print(apps_index + (len(configs)-1)*width*0.5)
            plt.xticks(apps_index + (len(configs)-1)*width*0.5,
                     apps, rotation=ticksRotation, ha='center', fontsize=fontSize, weight='bold')
         else:
            plt.xticks([], [])
      else:
         if showXAxis:
            plt.xticks(apps_index, entries, rotation=ticksRotation, ha='right')
         else:
            plt.xticks([], [])
            
      # plt.margins(x=0.01)
      plt.margins(x=0.01, tight=True)


   # legend
   if legendConfig is not None:
      plt.rcParams['legend.columnspacing'] = legendConfig['legend.columnspacing']
      plt.rcParams['legend.handlelength'] = legendConfig['legend.handlelength']
      plt.rcParams['legend.handletextpad'] = legendConfig['legend.handletextpad']
   
   # legendConfig = {'legend.columnspacing': 0.1,
   #                 'legend.handlelength': 1, 'legend.handletextpad': 0.5}
   
   
   # plt.legend(loc='lower right',fontsize=14)
   # plt.legend(loc='upper left',fontsize=14)
   # plt.legend(loc=legendPosition,fontsize=14, ncol=3)
   # plt.legend(loc=legendPosition, fontsize=14)
   # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=14)
   plt.legend(loc='lower center', bbox_to_anchor=legendPositionOffset,
               ncol=legendCol, fontsize=fontSize, frameon=False, prop={'weight':'bold'})
   # plt.legend(loc='best',fontsize=12)
   
   
   if title:
      plt.title(title, weight='bold')
   adjust_text(adjust_tests, ensure_inside_axes=False,
            arrowprops=dict(arrowstyle='->', color='black'),
            # expand = (1.1, 0.5),
            only_move={'explode': 'xy', 'pull': 'xy', 'static': 'xy', 'text': 'xy' })

   ax.spines['top'].set_linewidth(1.5)
   ax.spines['bottom'].set_linewidth(1.5)
   ax.spines['left'].set_linewidth(1.5)
   ax.spines['right'].set_linewidth(1.5)



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
   
def line(apps, configs, values, ylabel: str, only_average=False,  only_average_label = None,
        filename=None, groups=True, groupsInterval = 0.10, title=None, plotSize=(16, 4), 
        plotAverage=True, labelAverage=True, averageXlabel = "Mean", averageFunc=np.mean, decimals=1, fontSize = 14,
        yscale = None, ylim = None, 
        legendPosition='best', legendCol=10, legendConfig = {'legend.columnspacing': 1,
                                                      'legend.handlelength': 2, 'legend.handletextpad': 0.8}, legendPositionOffset = (0.45, 1),
        yMultipleLocator =None,
        colorPalette=sns.color_palette("mako", 25),  colorHatch=None, 
        edgecolor="black", showXAxis=True,
        markerPalette = ['o-','s-','^-','v-','+-', 'x-', '*-'],
        ):
   averageHeightDict = {}
   maxHeight = float('-inf')
   minHeight = float('inf')
   opacity = 1
   
   fig, ax = plt.subplots(figsize=plotSize)
   
   apps_index = np.arange(len(apps))
   # print(apps_index)

   if groups:
      width = (1.0 - groupsInterval)/(len(configs))
   else:
      width = 0.5

   if only_average:
      y_list = []
      for configId in range(len(configs)):
         ys = values[:, configId].astype('float')
         maxHeight = max(maxHeight, averageFunc(ys))
         minHeight = min(minHeight, averageFunc(ys))
         y_list.append(averageFunc(ys))
      assert(len(configs) == len(y_list))
      plt.plot(configs, y_list, 'o-', color = 'g', label=only_average_label)
   else:
      for configId in range(len(configs)):
         ys = values[:, configId].astype('float')
         maxHeight = max(maxHeight, max(ys))
         minHeight = min(minHeight, min(ys))
         
         if colorHatch is not None:
            hatch = colorHatch[configId]
         else:
            hatch = None
         
         valueMask = np.isfinite(ys)
         plt.plot((apps_index + 1)[valueMask], ys[valueMask], markerPalette[configId], linewidth=1, markersize=4, color = colorPalette[configId], label=configs[configId])
         
         # plt.bar(apps_index+configId*width, ys, width,
         #    alpha=opacity, color=colorPalette[configId],
         #    edgecolor=(edgecolor if edgecolor else colorPalette[configId]),
         #    linewidth=1, label=configs[configId], hatch = hatch)
         
         
   box = ax.get_position()
   ax.set_position([box.x0, box.y0*1.5, box.width, box.height])
   ax.yaxis.grid(True, linestyle = '--', linewidth = 0.5)  # horizontal grid
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
   if yMultipleLocator:
         ax.yaxis.set_major_locator(MultipleLocator(yMultipleLocator))
   plt.yticks(fontsize=fontSize-2, weight='bold')
   ax.yaxis.get_ticklocs(minor=True)
   ax.yaxis.set_tick_params(which='minor', bottom=False)
   ax.minorticks_on()
   plt.xticks(range(0, 21, 5),fontsize=fontSize-2, weight='bold')

   plt.ylabel(ylabel, fontsize=fontSize, weight='bold')    
   plt.xlabel("Application Idx", fontsize=fontSize-2, weight='bold')  
   # plt.margins(x=0.01)
   # plt.margins(x=0)

# legend
   if legendConfig is not None:
      plt.rcParams['legend.columnspacing'] = legendConfig['legend.columnspacing']
      plt.rcParams['legend.handlelength'] = legendConfig['legend.handlelength']
      plt.rcParams['legend.handletextpad'] = legendConfig['legend.handletextpad']
   
   # legendConfig = {'legend.columnspacing': 0.1,
   #                 'legend.handlelength': 1, 'legend.handletextpad': 0.5}
   
   
   # plt.legend(loc='lower right',fontsize=14)
   # plt.legend(loc='upper left',fontsize=14)
   # plt.legend(loc=legendPosition,fontsize=14, ncol=3)
   # plt.legend(loc=legendPosition, fontsize=14)
   # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=14)
   plt.legend(loc='lower center', bbox_to_anchor=legendPositionOffset,
               ncol=legendCol, fontsize=fontSize, frameon=False, prop={'weight':'bold'})
   # plt.legend(loc='best',fontsize=12)

   ax.spines['top'].set_linewidth(1.5)
   ax.spines['bottom'].set_linewidth(1.5)
   ax.spines['left'].set_linewidth(1.5)
   ax.spines['right'].set_linewidth(1.5)
   
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
      
      
def stack(apps, configs, values, ylabel: str, 
        filename=None, groups=True, groupsInterval = 0.10, title=None, plotSize=(16, 4), 
        plotAverage=True, labelAverage=True, averageXlabel = "Mean", labelExceedYlim = False,
        averageFunc=np.mean, decimals=1, fontSize = 14,
        only_average=False,
        yscale = None, ylim = None, yMultipleLocator=None,
        colorPalette=sns.color_palette("mako", 25),  colorHatch=None, 
        edgecolor="black", showXAxis=True, 
        legendPosition='best', legendCol=10, legendConfig = None, legendPositionOffset = (0.45, 1),
        stack = False, values2 =None, colorPalette2=None, stack_labels = None,
        ticksFrontsize = 14, ticksRotation = 0):
   averageHeightDict = {}
   maxHeight = float('-inf')
   minHeight = float('inf')
   opacity = 1
   adjust_tests = []
   
   
   fig, ax = plt.subplots(figsize=plotSize)
   
   if groups:
      width = (1.0 - groupsInterval)/(len(configs))
   else:
      width = 0.5
            
   apps_index = np.arange(len(apps))
   # print(apps_index)
   if stack:
      if only_average:
         print("use stacks")
         width = 0.75
         stack_ys_bottom = []
         stack_ys_top = []
         for configId in range(len(configs)):
            ys = values[:, configId].astype('float')
            maxHeight = max(maxHeight, max(ys))
            minHeight = min(minHeight, min(ys))
            ys2 = values2[:, configId].astype('float')
            maxHeight = max(maxHeight, max(ys2))
            minHeight = min(minHeight, min(ys2))
            if colorHatch is not None:
               hatch = colorHatch[0]
            else:
               hatch = None
            avg_stack_bottom = averageFunc(ys)
            avg_stack_top = averageFunc(ys2+ys) - averageFunc(ys)
            stack_ys_bottom.append(avg_stack_bottom)
            stack_ys_top.append(avg_stack_top)

            height = averageFunc(ys+ys2) + ylim[1]*0.03
            if ylim is not None and height > ylim[1]:
               height = ylim[1]+0.1
            label = format(np.round(averageFunc(ys+ys2),
                           decimals=decimals), "."+str(decimals)+"f")
            averageHeightDict[configs[configId]] = label
            if labelAverage:
               plt.text(configId, height, label, fontsize=fontSize -
                           4, ha='center', va='bottom', rotation=90)
         # print(stack_ys_bottom, stack_ys_top)
         plt.bar(np.arange(len(configs)), stack_ys_bottom, width,
                 alpha=opacity, color=colorPalette[0],
                 edgecolor=(edgecolor if edgecolor else colorPalette[0]),
                 linewidth=1, label=stack_labels[0], hatch=hatch)
         plt.bar(np.arange(len(configs)), stack_ys_top, width,
                 alpha=opacity, color=colorPalette2[0],
                 edgecolor=(edgecolor if edgecolor else colorPalette[0]),
                 linewidth=1, label=stack_labels[1], hatch=hatch, bottom=stack_ys_bottom)
   else:
      if only_average:
            
         for configId in range(len(configs)):
            ys = values[:, configId].astype('float')
            maxHeight = max(maxHeight, max(ys))
            minHeight = min(minHeight, min(ys))
            if colorHatch is not None:
               hatch = colorHatch[0]
            else:
               hatch = None
            plt.bar(configId, averageFunc(ys), width,
                     alpha=min(opacity*1.20, 1.0), color=colorPalette[0],
                     edgecolor=(
                  edgecolor if edgecolor else colorPalette[0]),
                  linewidth=1, hatch=hatch)
            height = averageFunc(ys) + ylim[1]*0.03
            if ylim is not None and height > ylim[1]:
               height = ylim[1]+0.1
            label = format(np.round(averageFunc(
                  ys), decimals=decimals), "."+str(decimals)+"f")
            averageHeightDict[configs[configId]] = label
            if labelAverage:
               plt.text(configId, height, label, fontsize=fontSize -
                        4, ha='center', va='bottom', rotation=90)
      else:
         last_ys = None
         last_ys_avg = None
         for configId in range(len(configs)):
            ys = values[:, configId].astype('float')
            maxHeight = max(maxHeight, max(ys))
            minHeight = min(minHeight, min(ys))
            
            if colorHatch is not None:
               hatch = colorHatch[configId]
            else:
               hatch = None
            
            if last_ys is None:
               plt.bar(apps_index+(len(configs)-1)*width/2,  ys, width*len(configs),
               alpha=opacity, color=colorPalette[configId],
               edgecolor=(edgecolor if edgecolor else colorPalette[configId]),
               linewidth=1, label=configs[configId], hatch = hatch)
            else:
               plt.bar(apps_index+(len(configs)-1)*width/2, ys- last_ys, width*len(configs),
                  alpha=opacity, color=colorPalette[configId],
                  edgecolor=(edgecolor if edgecolor else colorPalette[configId]),
                  linewidth=1, label=configs[configId], hatch = hatch, bottom=last_ys)
            last_ys = ys
            
            if labelExceedYlim:
               mask_list = [1 if x > ylim[1] else 0 for x in ys]    
               yss = np.multiply(mask_list, ys)
               xss = np.multiply(mask_list, apps_index+configId*width)
               
               for mask_bit_id in range(len(mask_list)):
                  maks_bit = mask_list[mask_bit_id]
                  if maks_bit == 1:
                     yss_label = format(np.round(yss[mask_bit_id], decimals=decimals), "."+str(decimals)+"f")
                     adjust_tests.append(plt.text(xss[mask_bit_id], ylim[1] + 0.1 , yss_label, fontsize=fontSize - 4, ha='center', va='bottom', rotation=0,  bbox=dict(facecolor='white', edgecolor='black', boxstyle='round', pad=0.08)))
                     
               
            if plotAverage:
               print(np.array([len(apps)])+configId*width)
               if last_ys_avg is None:
                  plt.bar(np.array([len(apps) + width])+(len(configs)-1)*width/2, [averageFunc(ys)], width*len(configs),
                        alpha=min(opacity*1.20, 1.0), color=colorPalette[configId],
                        edgecolor=(edgecolor if edgecolor else colorPalette[configId]),
                        linewidth=1, hatch = hatch)
               else:
                  plt.bar(np.array([len(apps) + width])+(len(configs)-1)*width/2, [averageFunc(ys) - last_ys_avg] , width*len(configs),
                        alpha=min(opacity*1.20, 1.0), color=colorPalette[configId],
                        edgecolor=(edgecolor if edgecolor else colorPalette[configId]),
                        linewidth=1, hatch = hatch, bottom=last_ys_avg)
               last_ys_avg = averageFunc(ys)
               height = averageFunc(ys) #+ ylim[1]*0.03
               # if ylim is not None and height > ylim[1]:
               #    height = ylim[1]+0.1 
               label = format(np.round(averageFunc(ys), decimals=decimals), "."+str(decimals)+"f")
               averageHeightDict[configs[configId]] = label
               if labelAverage:
                  adjust_tests.append(plt.text(np.array([len(apps)+ width])+(len(configs)-1)*width + 7.5*width, height, label, fontsize=fontSize - 4, ha='center', va='bottom', rotation=0, weight='bold'))
         if plotAverage:
            plt.axvline((2*len(apps)-1+(len(configs)-1)*width + width)/2, color='grey',
                        linestyle='dashed', linewidth=1)


   box = ax.get_position()
   ax.set_position([box.x0, box.y0*1.5, box.width, box.height])
   ax.yaxis.grid(True, linestyle = '--', linewidth = 0.5)  # horizontal grid
   ax.xaxis.grid(False)  # horizontal grid
   
   if yscale == "log":
      ax.set_yscale('log', base=2)
      ax.set_yticks([0.25, 0.5, 1, 2, 4, 8, 16, 32, 64, 128], minor=False)
      formatter = matplotlib.ticker.LogFormatter(base=2, labelOnlyBase=False)
      ax.yaxis.set_major_formatter(formatter)
   else:
      if ylim is not None:
         plt.ylim(ylim[0], ylim[1])
      else:
         if minHeight >= 0:
            plt.ylim(0, maxHeight*1.1)
         else:
            plt.ylim(minHeight*1.1, maxHeight*1.1)
      if yMultipleLocator:
         ax.yaxis.set_major_locator(MultipleLocator(yMultipleLocator))
   plt.ylabel(ylabel, fontsize=fontSize, weight='bold')

   # ticks
   plt.yticks(fontsize=fontSize, weight='bold')
   if only_average:
       plt.xticks(np.arange(len(configs)),
                  configs, rotation=ticksRotation, ha='center', fontsize=fontSize)
   else:
      if groups:
         if showXAxis:
            apps_index = np.arange(len(apps))
            if plotAverage:
               apps.append(averageXlabel)
               apps_index = np.append(apps_index, len(apps_index)+width)
            plt.xticks(apps_index + (len(configs)-1)*width*0.5,
                     apps, rotation=ticksRotation, ha='center', fontsize=fontSize, weight='bold')
         else:
            plt.xticks([], [])
      else:
         if showXAxis:
            plt.xticks(apps_index, entries, rotation=ticksRotation, ha='right')
         else:
            plt.xticks([], [])
            
      # plt.margins(x=0.01)
      plt.margins(x=0.01, tight=True)


   # legend
   if legendConfig is not None:
      plt.rcParams['legend.columnspacing'] = legendConfig['legend.columnspacing']
      plt.rcParams['legend.handlelength'] = legendConfig['legend.handlelength']
      plt.rcParams['legend.handletextpad'] = legendConfig['legend.handletextpad']
   
   # plt.legend(loc='lower right',fontsize=14)
   # plt.legend(loc='upper left',fontsize=14)
   # plt.legend(loc=legendPosition,fontsize=14, ncol=3)
   # plt.legend(loc=legendPosition, fontsize=14)
   # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=14)
   plt.legend(loc='lower center', bbox_to_anchor=legendPositionOffset,
               ncol=legendCol, fontsize=fontSize, frameon=False, prop={'weight':'bold'})
   # plt.legend(loc='best',fontsize=12)
   
   
   if title:
      plt.title(title)
   adjust_text(adjust_tests, ensure_inside_axes=False,
            arrowprops=dict(arrowstyle='->', color='red'),
            expand = (1.1, 1.2),
            only_move={'explode': 'xy', 'pull': 'xy', 'static': 'y', 'text': 'y' })

   ax.spines['top'].set_linewidth(1.5)
   ax.spines['bottom'].set_linewidth(1.5)
   ax.spines['left'].set_linewidth(1.5)
   ax.spines['right'].set_linewidth(1.5)
   
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