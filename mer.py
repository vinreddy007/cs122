#Record Linkage
#Link movie titles
import numpy as np
import pandas as pd
import csv
import re
import time

def read_in(lens_file, scripts_file):
    '''
    Read in lens and scripts data
    '''
    lens = pd.read_csv(lens_file)
    scripts = pd.read_csv(scripts_file)
    scripts = scripts.assign(movieId=-1)
    print(scripts.columns)
    return lens, scripts

def basic_linkage(lens, scripts):
    matches = 0
    # jw = 0
    # lens_titles = lens['title'].values.tolist()
    # lens_ID = len

    # for j, scripts_row in scripts[:10].iterrows():
    start = time.time()
    # for j in range(scripts['title'].size):  
    for j in range(7):  
        found_match = False
        t0 = time.time()
        for i in range(lens['title'].size):
        # for i, lens_row in lens.iterrows():

            # l_lower = lens_row['title'].lower()
            # iloc[i, 0] accesses title
            l_lower = lens.iloc[i, 1].lower()
            l = re.sub(r'[^\w]','', l_lower.replace('&', 'and'))
            s_lower = scripts.iloc[j, 0].lower()
            s = re.sub(r'[^\w]','', s_lower.replace('&', 'and'))
            
            # CASE 1 and 2
            if l == s:
                matches += 1
                # print(lens_row['title'])
                found_match = True
                break
            else:
                # l_year = re.search('.*(\d{4})', l)
                # s_year = re.search('.*(\d{4})', s)
                l_year = l[-4:]
                s_year = l[-4:]
                


                # if(l_year is not None and s_year is not None and l_year.group(1) == s_year.group(1):
                #   jwscore = jellyfish.jaro_winkler(l, s)
                    
                #   if jwscore > 0.8:
                #       if len(l_paren) is 2 or len(s_paren) is 2:
                #           print()
                #           print(jwscore)
                #           print(s_lower)
                #           print(l_lower)
                #           jw += 1

                # Case: Mismatched Foreign and English
                # if l_year is not None and s_year is not None and l_year.group(1) == s_year.group(1):
                if l_year == s_year:
                    l_foreng = l_lower.split('(')
                    s_foreng = s_lower.split('(')
                    if len(l_foreng) == 3: 
                        if len(s_foreng) == 3:
                            l_combo = l_foreng[1]+l_foreng[0]+l_foreng[2]
                            l_stripped = re.sub(r'[^\w]','', l_combo.replace('&', 'and'))
                            s_combo = ''.join(s_foreng)
                            s_stripped = re.sub(r'[^\w]','', s_combo.replace('&', 'and'))

                            if l_stripped == s_stripped:
                                matches += 1
                                found_match = True
                                break
                # Case: misplaced a, an, or the     
                    if ', a' in l_lower:
                        l_a = ''.join(l_lower.split(', a'))
                        l_a_stripped = re.sub(r'[^\w]','', l_a.replace('&', 'and'))
                        if l_a_stripped == s or l_a_stripped == s[1:]:
                            matches += 1
                            found_match = True
                            break
                    if ', an' in l_lower:
                        l_an = ''.join(l_lower.split(', an'))
                        l_an_stripped = re.sub(r'[^\w]','', l_an.replace('&', 'and'))
                        if l_an_stripped == s or l_an_stripped == s[2:]:
                            matches += 1
                            found_match = True
                            break
                    if ', the' in l_lower:
                        l_the = ''.join(l_lower.split(', the'))
                        l_the_stripped = re.sub(r'[^\w]','', l_the.replace('&', 'and'))
                        if l_the_stripped == s or l_the_stripped == s[3:]:
                            matches += 1
                            found_match = True
                            break
                # Case: l = [  ](  )year and s = [  ]year 
                        # if len(l_foreng) == 3 and len(s_foreng) != 3:
        if found_match:
            scripts.iat[j,2] = lens.iloc[i, 0]
            # print(scripts_row['movieId'])
            # print(scripts['movieId'])
        if not found_match:
            print(scripts.iloc[j, 0])
        print(time.time()-t0)
    print('matches: {}'.format(matches))
    # print(scripts)
    # Drop rows that didn't match with the movieLens dataset
    # scripts = scripts[pd.notnull(scripts['movieId'])] 
    scripts = scripts[scripts['movieId']!=-1].reset_index(drop=True)    
    print(scripts)
    print("TIME: {}".format(time.time() - start))
    return scripts


if __name__ == '__main__':

    lens_file = "ml-20m/movies.csv"
    scripts_file = "ml-20m/small1000.csv"
    lens, scripts = read_in(lens_file, scripts_file)
    # print(lens)
    # print(scripts)

    scripts = basic_linkage(lens, scripts)
    scripts.to_csv("ml-20m/smallMatched.csv", index = False)
