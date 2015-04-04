import os
import json
import datetime
import pickle
import inspect
from sys import argv
from utils import normalize_str as nstr

#script, gsrfile = argv 

def gdt(str):
    return datetime.datetime.strptime(str, "%Y-%m-%d")

def deletePreviousOutput(path):
	for file in os.listdir(path):
			file_path = os.path.join(path+"/output/gsr_pkl", file)
			try: 
				if os.path.isfile(file_path):
					os.unlink(file_path)
			except Exception, e:
				print e

def generateGsr(gsrfile, co1, eventTypes):
	events = [json.loads(line) for line in open(gsrfile).readlines()] #Loads all events from the gsr file
	gsr = dict()

	
	for event in  events[:]:
		et = event['eventType']
		if et in eventTypes:
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
	return gsr 
			
def generateGsrPkl(path, gsr):	
	for key in gsr: 
		#Writes files to unique gsr text file 
		pathName = os.path.join(path+"/output/gsr_pkl", str(key[1])+'_'+str(key[3])+'_gsr.txt')
		open(pathName, 'a').write(pickle.dumps(gsr[key]))
	
	
def generateGsrCutoff(path, co1, gsr, cutdt, enddt):	
	
	pathName = os.path.join(path+"/c_id", co1+'_ci_2_id.txt')
	ci_2_id = json.loads(open(pathName).read())
	items = sorted(ci_2_id.keys())

	for (ci, co, st, et), dts in gsr.items():
		if co == co1:
			ci = ci + '_' + co + '_' + st
			if ci_2_id.has_key(ci):
				id = ci_2_id[ci]
				for dt in sorted(dts):
					if dt >= cutdt and dt <= enddt: 
						pathName = os.path.join(path+"/output/gsr_cutoff", 'Gsr_'+co+'_'+et+'.txt'.format(co1))
						open(pathName, 'a').write('{0} {1}\n'.format(id, dt.strftime('%Y-%m-%d')))   
					
def gsr(co1, eventTypes, gsrfile, cutdt, enddt): 
	path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory
	deletePreviousOutput(path)
	gsr = generateGsr(gsrfile, co1, eventTypes)
	generateGsrPkl(path, gsr)
	generateGsrCutoff(path, co1, gsr, cutdt, enddt)



if __name__ == '__main__':
	gsrfile = 'gsrFebruary_all.mjson' 
	path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory
	deletePreviousOutput(path)
	
	#take cutdt, enddt, cos, event types
	cutdt = gdt('2013-12-31') #cutoff date 
	enddt = gdt('2015-03-29') #end date 
	cos = ['ecuador', 'argentina', 'chile', 'mexico', 'colombia'] #List of countries 
	eventTypes = ['0311', '0312', '0313', '0314'] #List of events 

	gsr = generateGsr(gsrfile, cos, eventTypes)
	generateGsrPkl(path, gsr)
	generateGsrCutoff(path, cos, gsr, cutdt, enddt)
	