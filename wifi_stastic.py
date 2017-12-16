import os
import csv
import pandas as pd
from pandas.io.parsers import read_csv

my_path = 'D:/tianchi/data'
dir_count = 0

for dirpath,_,_ in os.walk(my_path):
    if dirpath == 'D:/tianchi/data':
        continue
    
    dir_count = dir_count + 1
    print dir_count
    
    df_user = read_csv( dirpath +'/user_info.csv' )

    wifi_count = dict()
    wifi_true = dict()
    wifi_mean = dict()

    for i in range(0,len(df_user)):
            
        wifi_infos = df_user['wifi_infos'][i]
        wifis = wifi_infos.split(';')

        for wifi in wifis :
            w_id = wifi.split('|')[0]
            w_strength = float(wifi.split('|')[1])
            w_flag = wifi.split('|')[2]

            if w_id in wifi_count.keys() :
                wifi_count[w_id] = wifi_count[w_id] + 1
                wifi_mean[w_id] = wifi_mean[w_id]*(wifi_count[w_id]-1)/wifi_count[w_id]\
                                  + w_strength/wifi_count[w_id]
                if w_flag == 'true' :
                    wifi_true[w_id] = wifi_true[w_id] + 1
            else :
                wifi_count[w_id] = 1
                wifi_mean[w_id] = w_strength
                if w_flag == 'true' :
                    wifi_true[w_id] = 1
                else :
                    wifi_true[w_id] = 0
        
    fname = dirpath +'/wifi_info.csv'
    df_result = pd.DataFrame(columns=('wifi_id','wifi_count','wifi_true','wifi_mean'))
    df_result.to_csv(fname)

    csvfile = file(fname, 'ab+')
    for w_id in wifi_count.keys() :        
        writer = csv.writer(csvfile)
        writer.writerow(['',w_id,wifi_count[w_id],wifi_true[w_id],wifi_mean[w_id]])
    csvfile.close()

