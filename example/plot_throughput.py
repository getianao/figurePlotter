import sys
import os
import pandas as pd
sys.path.append("..") 
import myplot


def plot_throughput(dataPath, figurePath):
  exclude_apps = []
  path = sys.path[0]
  dataPath = path+'/'+dataPath
  figurePath = path+'/'+figurePath
  print("Open data file: ", dataPath)
  df = pd.read_csv(dataPath)
  apps = df.keys().values.tolist()[1:]
  apps = sorted(apps)
  print(apps)
  configs = df['config'].values.tolist()
  print(configs)
  values = df.loc[:, df.columns != 'config'].values
  values = values / 1000000
  print(values)
  myplot.bar(apps, configs, values, "Throughput (MB/s)", filename=figurePath)
  


if __name__ == "__main__":
    plot_throughput("./abs_throughput.csv", "./figures/abs_throughput.pdf")