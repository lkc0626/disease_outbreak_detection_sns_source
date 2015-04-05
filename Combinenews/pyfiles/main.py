import sys
#from sys import gsr_proc
from adi_gsr_test import gsr
from geo_proc_news import geo_proc_news_f
from calc_pvalues import  mainproc
from getinfnpss import getinfnpss_f
from adi_fp_tp_calc_test import fp_tp_calc
import pickle
import json
import datetime
import os
def gdt(str):
    return datetime.datetime.strptime(str, "%Y-%m-%d")

#os.chdir('..')

cos = [ 'chile']
for co1 in cos:

	event_Type='0313'
	stdt  = gdt('2012-01-01')
	cutdt = gdt('2012-03-01')
	enddt = gdt('2012-12-31')

	key_terms=['virus', 'epidemia', 'enfermos', 'hanta', 'viral', 'territorio', 'pneumonia', 'sangre', 'ratones', 'cardiopulmonar', 'vacuna', 'campos', 'provincial', 'hantavirus', 'tosse', 'nariz', 'estornudar', 'abdominal', 'lluvia', 'renal', 'paciente', 'transmissor', 'lixo', 'criaderos', 'respiratorias', 'manos', 'boca', 'rural', 'musculares', 'roedores']


	#folder = '../input/raw/twitter-2012'

	folder = os.path.abspath(os.path.pardir)+'/input/raw/news-2012'
	path = os.path.abspath(os.path.pardir)

	gsrfile1 = 'gsrFebruary_all.mjson'
 
	gsr(co1,event_Type,gsrfile1, cutdt,enddt)

	geo_proc_news_f(key_terms,folder, path,co1)

	gsrfile=co1+'_'+event_Type+'_gsr.txt'

	databaseName='{0}_news_cnt_data.txt'.format(co1)
	mainproc(co1,gsrfile,databaseName,stdt,cutdt,enddt, path)


	alpha_max = 1

	graphfile=path+'/pyfiles/chile_k_25_graph.txt'
	getinfnpss_f(alpha_max,graphfile, path)
	cutoff_score=0
	k = 50 
	# Calculates fp/tp and draws graphs 
	fp_tp_calc(cutoff_score, k, path)