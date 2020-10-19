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
def replace_data(self, log_path, output_path):
  log, data = fill_data(self)
  log_file = open(log_path, "w+")
  log_file.write(log)
  log_file.close()
  data.to_csv(output_path, index = False)
# Normalize
def normalize_z_score(self):
  data = self.copy()
  N = data.shape[0]
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
  # return dataframe
  return data

def normalize_minmax(self):
  data = self.copy()
  features_type = get_features_type(data)
  for i in range(data.shape[1]):
    if features_type[i] == 'numeric':
      minA = min(list(data.iloc[:, i].values))
      maxA = max(list(data.iloc[:, i].values))
      for j in range(data.shape[0]):
        data.iloc[j, i] = (data.iloc[j, i] - minA) / (maxA - minA)
  # return dataframe
  return data

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
    print(0)
elif args.replace:
    df = pd.read_csv(args.input)
    df.iloc[:, 0]
    replace_data(df, args.log, args.output)
elif args.discretize:
    print(0)
elif args.normalize:
    print(0)

