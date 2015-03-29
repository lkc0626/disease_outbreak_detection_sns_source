import json
import datetime
import os

#Text file containing [city, date, score]

# Warning file should be sorted by date 
#arguments: warning_file, gsr_file, cutoff 
def proc(warning_file, gsr_file, cutoff):
	pred = [] # value to hold city, dt, score 
	# Proc equivalent 
	lines = open(warning_file, "r").readlines() #ADD: Open file with [city, date, score] (add event type as well?) 
	for line in lines:
		items = line.split()
		id = items[0] 
		dt = datetime.datetime.strptime(items[1], "%Y-%m-%d")
		score = float(items[2])
		pred.append((id, dt, score)) #adding city, dt, score values 
	
	
		#gsr_file = "" #ADD: where the gsr file is defined, gsr file should have id, dt, et 
		
		pred = sorted(pred, key = lambda item: item[0]) #sorts pred value based on city 
	
		gsr = dict() #Dictionary to hold gsr events from file 
	
		for line in open(gsr_file).readlines():
			items = line.split()
			id = items[0] 
			dt = items[1] 
		
			# Fills gsr with [(ci,id)][dt] values 
			if gsr.has_key(id):
				gsr[id][dt] = 0
			else:
				gsr[id] = {dt: 0} 
		#curpred = pred[] 	
		tpr_fp(pred, gsr) 
			"""
			tprs = []
			fps = []
			for i in range(1, 300):
				cur_pred = pred[:i] #cur_pred takes predictions to a certain range 
				tpr, fp = tpr_fp(cur_pred, gsr) #proc calls tpr_fp here to return tpr fp 
				tprs.append(tpr)
				fps.append(fp)

			return tprs, fps
			"""
# TP/FP Equivalent 	

#Formula for recall is total true events within two weeks / total true events 
#Formula for true positive rate is true positive / true positive + false positive
#Formula for false positive rate is false positive days / # days 

def tpr_fp(cur_pred, gsr):
	fp = 0 # number of false positives 
	tp = 0 # number of true positives 
	data = dict() # used to hold all the true events 
	n = dict() # number of events that happen within a 2 week window of all nodes 

	"""
	for ci, id, dts in gsr.items():
		n = n + len(dts)
	"""
	#n = dict() number of events that happen in the two week window 
	
	for id, dt, score in cur_pred
		flag = 0
		if score >= cutoff: 
			# First if statement checks if there is an exact match between a gsr event and an EMBERS warning
			if gsr.has_key(id) and gsr[id].has_key(dt):
				data[(id,dt)] = 1
				flag = 1
				#nd = dt
			# Second statement to check if there is  match in the two week window 
			else: 
				nd1, nd2 = dt 
				for i in range(7):
					nd1 = nd1 + datetime.timedelta(days=1)
					nd2 = nd2 - datetime.timedelta(days=1)
					if gsr.has_key(id) and gsr[id].has_key(nd1):
						data[(id,dt)] = 1
						flag = 1
						nd = nd1
						break  
					if gsr.has_key(id) and gsr[id)].has_key(nd2):
						data[(id,dt)] = 1
						flag = 1 
						nd = nd2
						break 
	
			if flag == 0:
				fp = fp + 1
		
			#nd = dt
			if flag == 1:
				nd = dt - datetime.timedelta(days = 7)
				for i in range(14):
					nd = dt + datetime.timedelta(days = 1) 
					if gsr[id].has_key(nd):
						if not n.has_key(id):
							n[id] = dt					
						
					
		
		
		tp = len(data)
		tpr = tp / len(cur_pred)
		fpr = fp / len(cur_pred) 
		recall = tp / len(n) 
	
		print tp
		print tpr
		print fpr
		print recall 

if __name__ == '__main__':
	
	
	proc(warning_file, gsr_file, cutoff)
	 





"""
def tpr_fp(cur_pred, gsr):
    fp = 0
    tp = 0
    data = dict()
    n = 0
    for id, dts in gsr.items():
        n = n + len(dts)
	
	#g
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
        # If there are no flags (predictions or forecasts, adds one to the false positive rating) 
        if flag == 0:
            fp = fp + 1
    tp = len(data)
    return tp / (n * 1.0), fp




def proc(predfolder, co, method):
	#Predfolder is defined as predfolder = '/raid/home/zhoubj/KDD-Code/KDD-NPSS/realDataResult/{0}/civilUnrest/{1}/PValue'.format(method, co)
    #Co is the country (iterated through a list)
    #Method is from the list of methods - only one is necessary for this 
    
    files = [f for f in os.listdir(predfolder)]
    pred = [] # value to hold score, id, date time 
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
    
    # Iterates through each file of the gsr and adds an event to the dictionary for each warning
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
        cur_pred = pred[:i] #cur_pred takes predictions to a certain range 
        tpr, fp = tpr_fp(cur_pred, gsr) #proc calls tpr_fp here to return tpr fp 
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
	
	#g
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
        # If there are no flags (predictions or forecasts, adds one to the false positive rating) 
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

