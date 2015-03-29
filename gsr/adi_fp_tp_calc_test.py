import json
import datetime
import os




"""
def proc(predfolder, co, method):
	#Predfolder is defined as predfolder = '/raid/home/zhoubj/KDD-Code/KDD-NPSS/realDataResult/{0}/civilUnrest/{1}/PValue'.format(method, co)
    #Co is the country (iterated through a list)
    #Method is from the list of methods - only one is necessary for this 
    
    files = [f for f in os.listdir(predfolder)]
    pred = []
    for f in files:
        for line in open(os.path.join(predfolder, f)).readlines():
            if line.find('null') < 0 and len(line) > 5:
                items = line.split()
                id = int(items[0])
                score = float(items[1])
                dt = datetime.datetime.strptime(items[2], "%Y-%m-%d")
                pred.append((score, id, dt))
    folder = '/raid/home/zhoubj/KDD-Code/KDD-NPSS/realDataSet/CivilUnrest/{0}'.format(co)

    gsr_file = os.path.join(folder, 'gsr.txt')

    pred = sorted(pred, key = lambda item: item[0] * -1)
    
    n = len(pred)

    gsr = dict()
    for line in open(gsr_file).readlines():
        items = line.split()
        id = int(items[0])
        dt = datetime.datetime.strptime(items[1], "%Y-%m-%d")
        if gsr.has_key(id):
            gsr[id][dt] = 0
        else:
            gsr[id] = {dt: 0}

    tprs = []
    fps = []
    for i in range(1, 300):
        cur_pred = pred[:i]
        tpr, fp = tpr_fp(cur_pred, gsr) #proc calls tpr, fp here 
        tprs.append(tpr)
        fps.append(fp)

    return tprs, fps


# This is a function that determines the precision (True positive rate) 
def tpr_fp(cur_pred, gsr):
    fp = 0
    tp = 0
    data = dict()
    n = 0
    for id, dts in gsr.items():
        n = n + len(dts)

    for score, id, dt in cur_pred:
        flag = 0
        if gsr.has_key(id) and gsr[id].has_key(dt):
            data[(id, dt)] = 1
            flag = 1
        nd = dt
        for i in range(7):
            nd = nd + datetime.timedelta(days=1)
            if gsr.has_key(id) and gsr[id].has_key(nd):
                data[(id, nd)] = 1
                flag = 1
        nd = dt
        for i in range(7):
            nd = nd - datetime.timedelta(days=1)
            if gsr.has_key(id) and gsr[id].has_key(nd):
                data[(id, nd)] = 1
                flag = 1
        if flag == 0:
            fp = fp + 1
    tp = len(data)
    return tp / (n * 1.0), fp

methods = ['kCCSM', 'EventTree', 'KDDGreedy', 'LTSS'] #only KDDGreedy is passed up to the proc function 
#cos = ['Argentina', 'Mexico', 'Colombia', 'Chile', 'Ecuador']

cos = ['Argentina', 'Colombia', 'Chile', 'Ecuador']

# Main method 
for co in cos[3]: # Just looks at chile 
    print co
    data = []
    for method in methods:
        predfolder = '/raid/home/zhoubj/KDD-Code/KDD-NPSS/realDataResult/{0}/civilUnrest/{1}/PValue'.format(method, co)
        if os.path.exists(predfolder):
            tpr, fp = proc(predfolder, co, method) # proc returns value for tp, fp 
            data.append([tpr, fp])
        else:
            print predfolder
    n = len(data[0][0])
    m = len(data)
    items = []
    for i in range(n):
        item = [i]
        for j in range(m):
            item.append(data[j][0][i])
            item.append(data[j][1][i])
        items.append(item)
    for item in items[n-5:n]:
        print item
"""

