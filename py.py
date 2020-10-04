import pandas as pd
import argparse


#df = pd.read_csv('dataset/flag_with_attributes.data')
# df = pd.read_csv(args._input_)
# df.iloc[:,0]

def most_frequent(List):
    counter = 0
    num = List[0]
    for i in List:
        curr_frequency = List.count(i)
        if curr_frequency > counter:
            counter = curr_frequency
            num = i
    return num


# wrong
def fill_data(df):
    index = []
    sum = 0
    attribute_type = []
    # fill attribute type
    for i in range(df.shape[1]):
        for j in range(df.shape[0]):
            if df.iloc[j, i] != '?':
                try:
                    int(df.iloc[j, i])
                    attribute_type.append("numberic")
                    break
                except:
                    attribute_type.append("nominal")
                    break
    # fill data
    for i in range(df.shape[1]):
        if attribute_type[i] == "nominal":
            mfr = most_frequent(list(df.iloc[:, i]))
            for j in range(df.shape[0]):
                if df.iloc[j, i] == '?':
                    df.iloc[j, i] = mfr
        else:
            sum = 0
            index = []
            for j in range(df.shape[0]):
                if df.iloc[j, i] != '?':
                    sum += float(df.iloc[j, i])
                else:
                    index.append(j)
                avg = sum / df.shape[0]
                for k in range(len(index)):
                    df.iloc[k, i] = avg
    print(attribute_type)
    return df


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
    print(fill_data(df))
elif args.discretize:
    print(0)
elif args.normalize:
    print(0)

