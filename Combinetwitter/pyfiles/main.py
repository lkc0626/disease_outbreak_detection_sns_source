import sys
#from sys import gsr_proc
from adi_gsr_test import generateGSR
from geo_proc_twitter import geo_proc_twitter_f
from twitter_calc_pvalues import  mainproc
from getinfnpss import getinfnpss_f
from adi_fp_tp_calc_test import adi_fp_tp_calc_f
import pickle
import json
import datetime
def gdt(str):
    return datetime.datetime.strptime(str, "%Y-%m-%d")

cos = [ 'chile']
for co1 in cos:
    event_Type='0313'
    #key_terms='/Users/flyingfish88888/Desktop/disease_outbreak_detection-master/disease_outbreak_detection-master/twitter/input/hantavirus_keywords.txt'
    stdt  = gdt('2012-08-25')
    cutdt = gdt('2012-08-27')
    enddt = gdt('2012-08-29')

    key_terms=['virus', 'epidemia', 'enfermos', 'hanta', 'viral', 'territorio', 'pneumonia', 'sangre', 'ratones', 'cardiopulmonar', 'vacuna', 'campos', 'provincial', 'hantavirus', 'tosse', 'nariz', 'estornudar', 'abdominal', 'lluvia', 'renal', 'paciente', 'transmissor', 'lixo', 'criaderos', 'respiratorias', 'manos', 'boca', 'rural', 'musculares', 'roedores']
    

    folder = '../input/raw/twitter-2012'
    
    gsrfile1 = 'gsrFebruary_all.mjson' 
    
    generateGSR(cos,event_Type,gsrfile1, cutdt,enddt)
    
    geo_proc_twitter_f(key_terms,folder,co1)
    ######
    
    gsrfile=co1+'_'+event_Type+'_gsr.txt'
    ci2idfile=co1+'_ci_2_id.txt'
    ci_2_id = json.loads(open(ci2idfile).read())
   # gsr = pickle.loads(open(os.path.join(folder1, gsrfile)).read())
  
    databaseName='{0}_twitter_cnt_data.txt'.format(co1)
    mainproc(co1,gsrfile,ci_2_id,databaseName,stdt,cutdt,enddt)

############3
    alpha_max = 1
    #folder = 'blogs_output'
  #  subgraphfolder =  '/Users/flyingfish88888/Desktop/disease_outbreak_detection-master/disease_outbreak_detection-master/twitter/output/subraph'
    #print subgraphfolder
    graphfile='chile_k_25_graph.txt'
    getinfnpss_f(alpha_max,graphfile)
    
    #************
    cutoff_score=0
    adi_fp_tp_calc_f(cutoff_score,co1,event_Type)