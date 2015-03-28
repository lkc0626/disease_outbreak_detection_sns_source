import json
import pickle
import datetime
import os
from utils import normalize_str as nstr


#loc = pickle.load(open('../data/co_st_ci.pkl', 'rb'))

#loc = pickle.load(open('../data/ci_co_st_2_latlong.pkl', 'rb'))

#cos = ['ecuador', 'colombia', 'chile', 'argentina', 'mexico']
key_terms=['virus', 'epidemia', 'enfermos', 'hanta', 'viral', 'territorio', 'pneumonia', 'sangre', 'ratones', 'cardiopulmonar', 'vacuna', 'campos', 'provincial', 'hantavirus', 'tosse', 'nariz', 'estornudar', 'abdominal', 'lluvia', 'renal', 'paciente', 'transmissor', 'lixo', 'criaderos', 'respiratorias', 'manos', 'boca', 'rural', 'musculares', 'roedores']
#open('hantavirus_keywords.txt', 'w').write(json.dumps(key_terms))

vocab = json.dumps(open('hantavirus_keywords.txt').read())
vocab = {kw.strip().lower(): 1 for kw in vocab if len(kw.strip().split()) == 1}
#key_terms = ['protest', 'protesta', 'march', 'marcha', 'patriotic', 'patri', 'manifest', 'manifiesta']


new_terms = []
for kw, i in vocab.items():
    flag = 0
    for t in key_terms:
        if kw.find(t) >= 0:
            flag = 1
            break
    if flag == 1 or kw.find('@') >= 0 or kw.find('#') >= 0:
        new_terms.append(kw)
vocab = {t: 1 for t in new_terms}

database = dict()
#for co1 in cos[4:]:
folder = 'dataset/news-2012'
#    files = [file for file in os.listdir(folder) if file.find(co1) >= 0]
files = [file for file in os.listdir(folder)]
for file in files[:]:
    print file
    for line in open(os.path.join(folder, file)).readlines():
        tweet = json.loads(line)
        dt = datetime.datetime.strptime(tweet['date'][:10], "%Y-%m-%d")
        kws = {kw: 1 for kw in tweet['content'].split() if kw in key_terms}
        flag = 0
        if len(kws.keys()) == 1:
            for kw in kws.keys():
                if vocab.has_key(kw):
                  if kw in key_terms:
                    flag = 1
                    break
        elif len(kws.keys()) > 1:
            flag = 1
        if flag == 1:
        
             geo = tweet['embersGeoCode']
             for ci in geo:        
               ci = geo['city']
             for co in geo:
               co = geo['country']
             for st in geo:
               st = geo['admin1']
               flag = 0
        
            
             if ci and co and st and kws:
                ci = nstr(ci)
                co = nstr(co)
                st = nstr(st)
                ci = ci.lower()
                co = co.lower()
                st = st.lower()
                if not database.has_key((ci, co, st)):
                    database[(ci, co, st)] = {dt: 1}
                else:
                    if database[(ci, co, st)].has_key(dt):
                        database[(ci, co, st)][dt] += 1
                    else:
                        database[(ci, co, st)][dt] = 1

#    open('data/{0}_ci_count_data.txt'.format(co1), 'w').write(pickle.dumps(database))
#    database = pickle.loads(open('data/{0}_ci_count_data.txt'.format(co1)).read())
    open('data/{0}_news_cnt_data.txt'.format('chile'), 'w').write(pickle.dumps(database))
database = pickle.loads(open('data/{0}_news_cnt_data.txt'.format('chile')).read())
print database 
