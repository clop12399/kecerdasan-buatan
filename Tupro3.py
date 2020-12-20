import csv

def setData(reader):
    dataInf = []
    for row in reader:
        if row[0] == 'id':
            continue
        struct = {'id' : row[0],
                  'follower' : int(row[1]),
                  'foll_val1' : 0.0,
                  'foll_val2' : 0.0,
                  'eng_rate' : float(row[2]),
                  'eng_val1' : 0.0,
                  'eng_val2' : 0.0
                  }
        dataInf.append(struct)
    return dataInf

# Patokan buat follower [kecil, sedang, besar, sangat besar]
def follower_fuzzy():
    follower = [10000, 25000, 40000]
    for data in dataInf:
        if data['follower'] < follower[0]:
            data['foll_val1'] = 1
            data['foll_val2'] = 0
            data['foll_stat1'] = 'kecil'
            data['foll_stat2'] = 'sedang'
        elif data['follower'] > follower[0] and data['follower'] < follower[1]:
            data['foll_val1'] = (follower[1] - data['follower']) / (follower[1] - follower[0])
            data['foll_val2'] = (data['follower'] - follower[0]) / (follower[1] - follower[0])
            data['foll_stat1'] = 'kecil'
            data['foll_stat2'] = 'sedang'
        elif data['follower'] > follower[1] and data['follower'] < follower[2]:
            data['foll_val1'] = (follower[2] - data['follower']) / (follower[2] - follower[1])
            data['foll_val2'] = (data['follower'] - follower[1]) / (follower[2] - follower[1])
            data['foll_stat1'] = 'sedang'
            data['foll_stat2'] = 'besar'
        else:
            data['foll_val1'] = 0
            data['foll_val2'] = 1
            data['foll_stat1'] = 'besar'
            data['foll_stat2'] = 'sangat besar'

# Patokan buat engagement rate [buruk, cukup, bagus]
def engagement_fuzzy():
    eng_rate = [2.0, 3.0]
    for data in dataInf:
        if data['eng_rate'] < eng_rate[0]:
            data['eng_val1'] = 1
            data['eng_val2'] = 0
            data['eng_stat1'] = 'buruk'
            data['eng_stat2'] = 'cukup'
        elif data['eng_rate'] > eng_rate[0] and data['eng_rate'] < eng_rate[1]:
            data['eng_val1'] = (eng_rate[1] - data['eng_rate']) / (eng_rate[1] - eng_rate[0])
            data['eng_val2'] = (data['eng_rate'] - eng_rate[0]) / (eng_rate[1] - eng_rate[0])
            data['eng_stat1'] = 'buruk'
            data['eng_stat2'] = 'cukup'
        else:
            data['eng_val1'] = 0
            data['eng_val2'] = 1
            data['eng_stat1'] = 'cukup'
            data['eng_stat2'] = 'baik'

def rules(foll_stat, eng_stat):
    if foll_stat == 'kecil' and eng_stat == 'buruk':
        return 'nano'
    elif foll_stat == 'sedang' and eng_stat == 'buruk':
        return 'nano'
    elif foll_stat == 'besar' and eng_stat == 'buruk':
        return 'micro'
    elif foll_stat == 'sangat besar' and eng_stat == 'buruk':
        return 'micro'
    elif foll_stat == 'kecil' and eng_stat == 'cukup':
        return 'nano'
    elif foll_stat == 'sedang' and eng_stat == 'cukup':
        return 'micro'
    elif foll_stat == 'besar' and eng_stat == 'cukup':
        return 'micro'
    elif foll_stat == 'sangat besar' and eng_stat == 'cukup':
        return 'medium'
    elif foll_stat == 'kecil' and eng_stat == 'baik':
        return 'micro'
    elif foll_stat == 'sedang' and eng_stat == 'baik':
        return 'micro'
    elif foll_stat == 'besar' and eng_stat == 'baik':
        return 'medium'
    else:
        return 'medium'

def value(status):
    if status == 'nano':
        return 0.3
    elif status == 'micro':
        return 0.6
    else:
        return 0.9

def defuzzification():
    for data in dataInf:
        nilai1 = min(data['foll_val1'], data['eng_val1'])
        status1 = rules(data['foll_stat1'], data['eng_stat1'])
        nilai2 = min(data['foll_val2'], data['eng_val1'])
        status2 = rules(data['foll_stat2'], data['eng_stat1'])
        nilai3 = min(data['foll_val1'], data['eng_val2'])
        status3 = rules(data['foll_stat1'], data['eng_stat2'])
        nilai4 = min(data['foll_val2'], data['eng_val2'])
        status4 = rules(data['foll_stat2'], data['eng_stat2'])

        data['y*'] = (nilai1 * value(status1)) + (nilai2 * value(status2)) + (nilai3 * value(status3)) + (
                    nilai4 * value(status4)) / (nilai1 + nilai2 + nilai3 + nilai4)


def insertion_sort(dataInf):
    for i in range(1, len(dataInf)):
        j = i - 1
        nxt_element = dataInf[i]
        # Compare the current element with next one
        while (dataInf[j]['y*'] < nxt_element['y*']) and (j >= 0):
            dataInf[j + 1] = dataInf[j]
            j = j - 1
        dataInf[j + 1] = nxt_element

def writeData():
    chosen = open("chosen.csv", "w", newline='')
    w = csv.writer(chosen)

    for i in range(0, 20):
        w.writerow([dataInf[i]['id']])

    chosen.close()


reader = csv.reader(open('influencers.csv', 'r'), delimiter=',', quotechar='|')
dataInf = setData(reader)

follower_fuzzy()
engagement_fuzzy()
defuzzification()
insertion_sort(dataInf)
writeData()