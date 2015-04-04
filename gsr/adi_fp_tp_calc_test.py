import json
import datetime
import os
import inspect
import dateutil
import matplotlib.pyplot as plt



#File to take warning files from subgraph files 
def makeWarningFile(path):
	warningPath = os.path.join(path, 'warning_file.txt')	
	warning_file = open(warningPath, 'a')
	warning_file.seek(0)
	warning_file.truncate()	 # Deletes contents in warning file from previous use 
		
	for filename in os.listdir(path+'/subgraph'):
		dateobj = datetime.datetime.strptime(filename[0:10],'%Y-%m-%d').date()		
		file_path = os.path.join(path+'/subgraph', filename)
		items = open(file_path).read().split()
		print items
		score = items[-1]
		for id in range(len(items)-1):							
			warning_file.write('{0} {1} {2}\n'.format(items[id], filename[0:10], score))

#Makes a list of predictions based on the warning file that Embers generates 

def makePredictionList(warning_file, cutoff):
	pred = [] # value to hold city, dt, score 
	# Proc equivalent 
	lines = open(warning_file, "r").readlines() #ADD: Open file with [id, date, score] 
	for line in lines:
		items = line.split()
		id = items[0] 
		dt = datetime.datetime.strptime(items[1], "%Y-%m-%d")
		score = float(items[2])
		if score >= cutoff:
			pred.append((id, dt, score)) #adding id, dt, score values 
			
	pred = sorted(pred, key = lambda item: item[2], reverse=True) #sorts pred value based on score
	#print pred
	#print "Predictions: "+str(len(pred))
	return pred 

			
#Makes a gsr list based off the gsr_file 

def makeGsrList(gsr_file):
	gsr = dict() #Dictionary to hold gsr events from file 
	
	for line in open(gsr_file).readlines():
		items = line.split()
		id = items[0] 
		dt = items[1] 
		
		if gsr.has_key(id):
			gsr[id][dt] = 0
		else:
			gsr[id] = {dt: 0} 
		
	#print "GSR Events: "+str(len(gsr))
	return gsr 
			
# TP/FP Equivalent 	

#Formula for recall is total true events within two weeks / total true events 
#Formula for true positive rate is true positive / true positive + false positive
#Formula for false positive rate is false positive days / # days 

def tpr_fp(pred, gsr, k):
	fp = 0 # number of false positives 
	tp = 0 # number of true positives 
	data = dict() # used to hold all the true events 
	n = dict() # number of events that happen within a 2 week window of all nodes 
	i = 0 
	for id, dt, score in pred:
		if (i > k):
			break
		i += 1 
		flag = 0
		
		# First if statement checks if there is an exact match between a gsr event and an EMBERS warning
		if gsr.has_key(id) and gsr[id].has_key(dt):
			data[(id,dt)] = 1
			flag = 1
			
		# Second statement to check if there is  match in the two week window 
		else: 
			nd1 = nd2 = dt 
			for i in range(7):
				nd1 = nd1 + datetime.timedelta(days=1)
				nd2 = nd2 - datetime.timedelta(days=1)
				if gsr.has_key(id) and gsr[id].has_key(nd1):
					data[(id,dt)] = 1
					flag = 1
					nd = nd1
					break  
				if gsr.has_key(id) and gsr[id].has_key(nd2):
					data[(id,dt)] = 1
					flag = 1 
					nd = nd2
					break 
				
		# Statement that increments the false positive 
		if flag == 0:
			fp = fp + 1

		if flag == 1:
			nd = dt - datetime.timedelta(days = 7)
			for i in range(14):
				nd = dt + datetime.timedelta(days = 1) 
				if gsr[id].has_key(nd):
					if not n.has_key(id):
						n[id] = dt					
				
			


	tp = len(data)
	tpr = tp / len(pred)
	fpr = fp / len(pred) 
	if (len(n) != 0):
		recall = tp / len(n) 
		return tpr, fpr, recall 

	return tpr, fpr, 0 # returns 0 for recall if it is not detected 



	
	
def graph(tprList, fprList, recallList, filename):
	
	# Shows plot of tpr vs. fpr 
	plt.plot(tprList, fprList, '-')
	plt.xlabel('True Positive Rate')
	plt.ylabel('False Positive Rate')
	plt.show()
	# Shows plot of tpr vs. recall 
	if not (recallList[0] == 0): # only show if there is an element in recall, edit to make more robust
		plt.plot(tprList, recallList, '-')
		plt.xlabel('True Positive Rate')
		plt.ylabel('False Positive Rate') 
		plt.show()	

if __name__ == '__main__':
	
	path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory
	makeWarningFile(path)
	cutoff = 0 # change this 
	k = 50 # change this 
	pred = makePredictionList('warning_file.txt', cutoff) 
	gsrPath = path+'/output/gsr_cutoff'
	
	
		
	for filename in os.listdir(gsrPath):
		gsr = makeGsrList(os.path.join(gsrPath,filename))
		tprList = []
		fprList = []
		recallList = []
		for i in range(k):
			#print i
			tpr,fpr, recall = tpr_fp(pred, gsr, i)
			tprList.append(tpr)
			fprList.append(fpr)
			recallList.append(recall)
		graph(tprList, fprList, recallList, filename) 
		

