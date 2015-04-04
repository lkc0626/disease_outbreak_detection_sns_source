import json
import datetime
import os
import dateutil
import matplotlib.pyplot as plt



#File to take warning files 
def makeWarningFile(path):
	warningPath = os.path.join(path, 'warning_file.txt')	
	warning_file = open(warningPath, 'a')
	warning_file.seek(0)
	warning_file.truncate()	 # Deletes contents in warning file from previous use 
	
	#subgraphPath = os.path.join(path, '/subgraph')
	
	for filename in os.listdir(path+'/subgraph'):
		dateobj = datetime.datetime.strptime(filename[0:10],'%Y-%m-%d').date()		
		file_path = os.path.join(path+'/subgraph', filename)
		items = open(file_path).read().split()
		print items
		score = items[-1]
		for id in range(len(items)-1):							
			warning_file.write('{0} {1} {2}\n'.format(items[id], filename[0:10], score))
			#print(items[id], filename[0:10], score)
			

def proc(warning_file, gsr_file, cutoff):
	pred = [] # value to hold city, dt, score 
	# Proc equivalent 
	lines = open(warning_file, "r").readlines() #ADD: Open file with [id, date, score] 
	for line in lines:
		items = line.split()
		id = items[0] 
		dt = datetime.datetime.strptime(items[1], "%Y-%m-%d")
		score = float(items[2])
		pred.append((id, dt, score)) #adding id, dt, score values 
	
	
		#gsr_file = "" #ADD: where the gsr file is defined, gsr file should have id, dt, et 
		
		pred = sorted(pred, key = lambda item: item[2]) #sorts pred value based on score
	
		gsr = dict() #Dictionary to hold gsr events from file 
	
		for line in open(gsr_file).readlines():
			items = line.split()
			id = items[0] 
			dt = items[1] 
		
			# Fills gsr with [id][dt] values 
			if gsr.has_key(id):
				gsr[id][dt] = 0
			else:
				gsr[id] = {dt: 0} 
		
	print "GSR Events: "+str(len(gsr))
	print "Predictions: "+str(len(pred))
	tpr_fp(pred, gsr, cutoff) 
			
# TP/FP Equivalent 	

#Formula for recall is total true events within two weeks / total true events 
#Formula for true positive rate is true positive / true positive + false positive
#Formula for false positive rate is false positive days / # days 

def tpr_fp(cur_pred, gsr, cutoff):
	fp = 0 # number of false positives 
	tp = 0 # number of true positives 
	data = dict() # used to hold all the true events 
	n = dict() # number of events that happen within a 2 week window of all nodes 

	
	#n = dict() number of events that happen in the two week window 
	
	for id, dt, score in cur_pred:
		flag = 0
		if score >= cutoff: 
			# First if statement checks if there is an exact match between a gsr event and an EMBERS warning
			if gsr.has_key(id) and gsr[id].has_key(dt):
				print "Found true positive"
				data[(id,dt)] = 1
				flag = 1
				#nd = dt
			# Second statement to check if there is  match in the two week window 
			else: 
				nd1 = nd2 = dt 
				for i in range(7):
					nd1 = nd1 + datetime.timedelta(days=1)
					nd2 = nd2 - datetime.timedelta(days=1)
					if gsr.has_key(id) and gsr[id].has_key(nd1):
						#print "Found true positive" 
						data[(id,dt)] = 1
						flag = 1
						nd = nd1
						break  
					if gsr.has_key(id) and gsr[id].has_key(nd2):
						#print "Found true positive" 
						data[(id,dt)] = 1
						flag = 1 
						nd = nd2
						break 
						
			# Statement that increments the false positive 
			if flag == 0:
				#print "Found false positive"
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
	if (len(n) != 0):
		recall = tp / len(n) 
		print "Recall: " +str(recall )

	print "True positive: "+str(tp)
	print "False positive: "+str(fp)
	print "True positive rate: "+str(tpr)
	print "False positive rate: "+str(fpr)
	
#def graph(tpr, fpr, recall, ):

		

if __name__ == '__main__':
	makeWarningFile('/Users/Adityan/Documents/Github_Repos/disease_outbreak_detection/gsr')
	
	pathtoGsrFile = os.path.join('/Users/Adityan/Documents/Github_Repos/disease_outbreak_detection/gsr/output/gsr_cutoff/', 'Gsr_mexico_0312.txt')
	proc('warning_file.txt',pathtoGsrFile, 0) 
	#proc(warning_file, gsr_file, cutoff)
	 

