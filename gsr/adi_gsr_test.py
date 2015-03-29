import os
import json
import datetime
import pickle
from utils import normalize_str as nstr

def gdt(str):
    return datetime.datetime.strptime(str, "%Y-%m-%d")

gsrfile = 'gsrFebruary_all.mjson' 
savePath = '/Users/Adityan/Documents/Github_Repos/disease_outbreak_detection/gsr/output' #Change this to where you want to save the output

#Code to delete any previous output in the output folder 
for file in os.listdir(savePath):
	file_path = os.path.join(savePath, file)
	try: 
		if os.path.isfile(file_path):
			os.unlink(file_path)
	except Exception, e:
		print e


events = [json.loads(line) for line in open(gsrfile).readlines()] #Loads all events from the gsr file

cos = ['ecuador', 'argentina', 'chile', 'mexico', 'colombia'] #List of countries 
gsr = dict() 

# Iterates through each country, looks for events that match and adds them to the gsr dictionary
for co1 in cos:
    for event in  events[:]:
    	et = event['eventType']
    	if et == '0311' or et == '0312' or et == '0313' or et == '0314':  
        	(co, st, ci) = event['location']
        	if co and st and ci and co != '-' and st != '-' and ci != '-':
        		co = nstr(co).lower()
        		st = nstr(st).lower()
        		ci = nstr(ci).lower()
        		dtstr = event['eventDate'][:10]
        		dt = datetime.datetime.strptime(dtstr, "%Y-%m-%d")
        		
        		# Checks if the key (ci, co, st, et) is in gsr, otherwise adds it to the dictionary
        		if not gsr.has_key((ci, co, st, et)): 
        			gsr[(ci, co, st, et)] = {dt: 1}
        		else:        			
        			gsr[(ci, co, st, et)][dt] = 1 
        	

for key in gsr: 
	#Writes files to unique gsr text file 
	pathName = os.path.join(savePath, str(key[1])+'_'+str(key[3])+'_gsr.txt')
	open(pathName, 'a').write(pickle.dumps(gsr[key]))

# Cuts off any events that are older than the cutoff date 	
cutdt = gdt('2013-12-31')
enddt = gdt('2015-03-29') 
for co1 in cos[0:]:
    ci_2_id = json.loads(open(co1+'_ci_2_id.txt'.format(co1)).read())
    items = sorted(ci_2_id.keys())

    for (ci, co, st, et), dts in gsr.items():
        if co == co1:
            ci = ci + '_' + co + '_' + st
            if ci_2_id.has_key(ci):
                id = ci_2_id[ci]
                for dt in sorted(dts):
                    print co+' '+et+' '+dt.strftime('%Y-%m-%d')
                    if dt >= cutdt and dt <= enddt: 
                    	pathName = os.path.join(savePath, 'Gsr_'+co+'_'+et+'.txt'.format(co1))
                        open(pathName, 'a').write('{0} {1}\n'.format(id, dt.strftime('%Y-%m-%d')))   	