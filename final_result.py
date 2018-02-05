'''
intergrate the predict results in every mall directory into a single file, according to the initial order in evaluation_public.csv.
record the search position in each result.csv to improve the search efficiency.
'''
import os
import csv
import time
import pandas as pd
from pandas.io.parsers import read_csv

my_path = 'D:/tianchi_multiclass/'
mall_set = set()
df_eval = read_csv( my_path + 'evaluation_public.csv' )

df_final = pd.DataFrame(columns=('row_id','shop_id'))
fname_f = my_path + 'final_result.csv'
df_final.to_csv(fname_f)
csvfile = file(fname_f, 'ab+')

start_dict = dict()

for i in range(0,len(df_eval)):
    if i%10000 == 0:
        print i

    row_id = df_eval['row_id'][i]
    user_id = df_eval['user_id'][i]
    mall_id = df_eval['mall_id'][i]
    
    df_result = read_csv(my_path +'data/%s/result.csv'%mall_id)
    
    if not mall_id in start_dict.keys() :
        start_dict[mall_id] = 0
    start = start_dict[mall_id]
        
    index = start
    for j in range(start,len(df_result)):
        if df_result['row_id'][j] == row_id :
            index = j
            break
        if j == len(df_result)-1 :
            print 'Not found.'
            start_dict[mall_id] = start_dict[mall_id] - 1
            
    start_dict[mall_id] = start_dict[mall_id] + 1
    shop_id = df_result['shop_id'][index]
        
    writer = csv.writer(csvfile)
    writer.writerow(['',row_id,shop_id])

csvfile.close()
