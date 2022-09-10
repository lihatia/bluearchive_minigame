import csv
import pickle

data = []
with open("sp_action.csv", "r", encoding='utf8', newline='') as f:
    reader=csv.reader(f)

    for row in reader:
        str_data=row
        left=int(str_data[0])
        right=int(str_data[1])
        if left+right!=0:
            data.append([left,right])


with open("sp_beatmap_fix.pkl", "wb") as f:
    pickle.dump(data, f)
