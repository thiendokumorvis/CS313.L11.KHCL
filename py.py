import pandas as pd
import argparse
import math

# Find most frequent element in a list
def most_frequent(List): 
  counter = 0
  num = List[0]
  for i in List:
    curr_frequency = List.count(i)
    if(curr_frequency > counter):
      counter = curr_frequency
      num = i
  return num

# Get features' types of the dataframe
def get_features_type(self):
  features_type = []
  # Fill features' types
  for i in range(self.shape[1]):
    for j in range(self.shape[0]):
      if self.iloc[j, i] != '?':
        try:
          float(self.iloc[j, i])
          features_type.append("numeric")
          break
        except:
          features_type.append("nominal")
          break
  return features_type

# Return processed data and log, hand-coded, may be changed later
def fill_data(self):
  data = self.copy()
  index = []
  sum = 0
  log = ''
  features_type = get_features_type(data)
  # Fill data
  for i in range(data.shape[1]):
    missing_count = 0
    if features_type[i] == "nominal":
      mfr = most_frequent(list(data.iloc[:,i]))
      for j in range(data.shape[0]):
        if data.iloc[j, i] == '?':
          data.iloc[j, i] = mfr
          missing_count += 1
      if missing_count > 0:
        log = log + str(data.columns[i]) + '\t' + str(missing_count) + '\t' + mfr + '\n'
    else:
      sum = 0
      index = []
      for j in range(data.shape[0]):
        if data.iloc[j, i] != '?':
          sum += float(data.iloc[j, i])
        else:
          missing_count += 1
          index.append(j)
        avg = sum / data.shape[0]
        for k in range(len(index)):
          data.iloc[index[k], i] = avg
      if missing_count > 0:
        log = log + str(data.columns[i]) + '\t' + str(missing_count) + '\t' + str(avg) + '\n'
  return log, data

# Functions

# Summary
def summarize_data(self, log_path):
  types = get_features_type(self)
  log = str(self.shape[0]) + '\n' + str(self.shape[1]) + '\n'
  for i in range(self.shape[1]):
    log = log + str(self.columns[i]) + '\t' + types[i] + '\n'
  log_file = open(log_path, "w+")
  log_file.write(log)
  log_file.close()

# Replace
def replace_data(self, output_path, log_path):
  log, data = fill_data(self)
  log_file = open(log_path, "w+")
  log_file.write(log)
  log_file.close()
  data.to_csv(output_path, index = False)

# Normalize
def normalize_z_score(self):
  data = self.copy()
  N = data.shape[0]
  log = ''
  features_type = get_features_type(data)
  for i in range(data.shape[1]):
    if features_type[i] == 'numeric':
      sum = 0
      for j in range(N):
        sum += float(data.iloc[j, i])
      avg = sum / N
      variance = 0
      for j in range(N):
        variance += (float(data.iloc[j, i]) - avg)**2
      variance = math.sqrt(variance / N)
      for j in range(N):
        data.iloc[j, i] = ((data.iloc[j, i]) - avg) / variance
      log = log + str(data.columns[i]) + '\t' + str(min(list(data.iloc[:, i].values))) + '\t' + str(max(list(data.iloc[:, i].values))) + '\n'
  # return log, dataframe
  return log, data

def normalize_minmax(self):
  data = self.copy()
  log = ''
  features_type = get_features_type(data)
  for i in range(data.shape[1]):
    if features_type[i] == 'numeric':
      minA = min(list(data.iloc[:, i].values))
      maxA = max(list(data.iloc[:, i].values))
      for j in range(data.shape[0]):
        data.iloc[j, i] = (data.iloc[j, i] - minA) / (maxA - minA)
      log = log + str(data.columns[i]) + '\t' + str(min(list(data.iloc[:, i].values))) + '\t' + str(max(list(data.iloc[:, i].values))) + '\n'
  # return log, dataframe
  return log, data

def normalize_data_w_z_score(self, output_path, log_path):
  log, data = normalize_z_score(self)
  log_file = open(log_path, "w+")
  log_file.write(log)
  log_file.close()
  data.to_csv(output_path, index = False)

def normalize_data_w_minmax(self, output_path, log_path):
  log, data = normalize_minmax(self)
  log_file = open(log_path, "w+")
  log_file.write(log)
  log_file.close()
  data.to_csv(output_path, index = False)

def binning_width(df,column,numcol,number): # cột cần làm chuẩn để chia theo (column), số thứ tự của cột (numcol) , số giỏ (number)
  log = 'properties:'
  data = df.values.tolist()
  lst = df[column]
  log = log + column + ','
  distance = (max(lst)+min(lst))/number
  temp = distance
  for k in range(number):
    for i in range(len(df[column])):
      if data[i][numcol]>temp:
        for j in range(i,len(df[column])):
          if data[j][numcol]<=temp:
            data[i],data[j] = data[j],data[i]
    temp += distance
  temp2 = distance 
  temp3 = 0
  for k in range(number): 
    count = 0
    for i in range(len(lst)):
      if data[i][numcol]<=temp2 and data[i][numcol]>temp3:
        data[i][numcol] = temp2
        count+=1
    log = log + str(temp2) + ':' +str(count) + ','
    temp2 += distance
    temp3 +=distance
  return pd.DataFrame(data),log

def output(data,log):
  data.to_csv(r'/content/drive/My Drive/CS313/clear.csv', index = False)
  text_file = open('/content/drive/My Drive/CS313/clear.txt', "w")
  n = text_file.write(log)
  text_file.close()

# Save normalized dataframe: pd.read_csv('output_path')
parser = argparse.ArgumentParser(description="Bai TH 1")
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-s", "--summary", action="store_true")
group.add_argument("-r", "--replace", action="store_true")
group.add_argument("-d", "--discretize", action="store_true")
group.add_argument("-n", "--normalize", action="store_true")

parser.add_argument("input", type=str, help="input file dir")
parser.add_argument("output", type=str, help="output file dir")
parser.add_argument("log", type=str, help="log file dir")
args = parser.parse_args()

if args.verbose:
    print("input file name: {} \noutput file name: {} \nlog file name: {}".format(args.input, args.output, args.log))
    
elif args.summary:
    df = pd.read_csv(args.input)
    summarize_data(df, args.log)
    print('Done \nresult in: ' + args.log)

elif args.replace:
    df = pd.read_csv(args.input)
    df.iloc[:, 0]
    replace_data(df, args.output, args.log)
    print('Done \nresult in: ' + args.output + '\nto see changed, go to: ' + args.log)

elif args.discretize:
    df = pd.read_csv(args.input)
    print('Choose method: \n1: Binning width \n2: Binning depth')
    method = input().strip()
    print('input number of bin: ')
    binning = input().strip()
    #if method == '1':
      # temp = normalize_data_w_z_score(df, args.output, args.log)
    #elif method == '2':
      # temp = normalize_data_w_minmax(df, args.output, args.log)
    # data,log = binning_width(df,'zone',2,4)
    output(data,log)
    print('Done \nresult in: ' + args.output + '\nto see changed, go to: ' + args.log)

elif args.normalize:
    df = pd.read_csv(args.input)
    print('Choose method: \n1: Z-score \n2: Min-max')
    choice = input().strip()
    if choice == '1':
      temp = normalize_data_w_z_score(df, args.output, args.log)
    elif choice == '2':
      temp = normalize_data_w_minmax(df, args.output, args.log)
    print('Done \nresult in: ' + args.output + '\nto see changed, go to: ' + args.log)


