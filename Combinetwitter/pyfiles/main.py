import sys
#from sys import gsr_proc
from adi_gsr_test import gsr
from geo_proc_twitter import geo_proc_twitter_f
from twitter_calc_pvalues import  mainproc
from getinfnpss import getinfnpss_f
from adi_fp_tp_calc_test import fp_tp_calc
import pickle
import json
import datetime
def gdt(str):
    return datetime.datetime.strptime(str, "%Y-%m-%d")

cos = [ 'chile']
for co1 in cos:
    event_Type='0313'
    stdt  = gdt('2012-08-25')
    cutdt = gdt('2012-08-27')
    enddt = gdt('2012-10-29')

    key_terms=['virus', 'epidemia', 'enfermos', 'hanta', 'viral', 'territorio', 'pneumonia', 'sangre', 'ratones', 'cardiopulmonar', 'vacuna', 'campos', 'provincial', 'hantavirus', 'tosse', 'nariz', 'estornudar', 'abdominal', 'lluvia', 'renal', 'paciente', 'transmissor', 'lixo', 'criaderos', 'respiratorias', 'manos', 'boca', 'rural', 'musculares', 'roedores']
    

    folder = '../input/raw/twitter-2012'
    
    gsrfile1 = 'gsrFebruary_all.mjson' 
	
	#Generates GSR pkl and cutoff files using cutoff/enddates and specified event types/countries
    gsr(co1,event_Type,gsrfile1, cutdt,enddt)

    geo_proc_twitter_f(key_terms,folder,co1)

    gsrfile=co1+'_'+event_Type+'_gsr.txt'
  
    databaseName='{0}_twitter_cnt_data.txt'.format(co1)
    mainproc(co1,gsrfile,databaseName,stdt,cutdt,enddt)


    alpha_max = 1

    graphfile='chile_k_25_graph.txt'
    getinfnpss_f(alpha_max,graphfile)

    cutoff_score=0
    k = 50 
    # Calculates fp/tp and draws graphs 
    fp_tp_calc(cutoff_score, k)