import sys
from collections import defaultdict

def convert(csv):
    with open(csv, 'r') as rfp:
        fp1 = open('dataset/directed.txt', 'w+')
        fp2 = open('dataset/bi-directed.txt', 'w+')
        dic = defaultdict(int)
        idx = 1
        for line in rfp:
            lst = line.rstrip('\n').split(',')
            for i in range(len(lst)):
                for j in range(i+1, len(lst)):
                    a, b = lst[i], lst[j]
                    if dic[a] == 0:
                        dic[a] = idx
                        idx += 1
                    if dic[b] == 0:
                        dic[b] = idx
                        idx += 1

                    fp1.write("{},{}\n".format(dic[a], dic[b]))
                    fp2.write("{},{}\n".format(dic[a], dic[b]))
                    fp2.write("{},{}\n".format(dic[b], dic[a]))

        print(len(dic))
            
    
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("[Error] python IBM_data_converter.py IBM.csv")
        sys.exit(1)

    print(sys.argv)
    csv = sys.argv[1]
    convert(csv)