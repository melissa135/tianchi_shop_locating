import os
import csv
import random
import numpy as np
import pandas as pd
from pandas.io.parsers import read_csv

  
def user_scatter(path):

    df_user = read_csv(path + '/user_info.csv')
    length = len(df_user)
    num = 5

    time_list = []
    for i in range(0,len(df_user)):
        time = df_user['time_stamp'][i]
        time_list.append(time)

    time_list.sort()
    
    for k in range(0,num) :

        fname = path + '/subset_%d.csv'%k
        df_subset = pd.DataFrame(columns=('user_id','shop_id','time_stamp',
                                          'longitude','latitude','wifi_infos'))
        df_subset.to_csv(fname)
        csvfile_test = file(fname, 'ab+')
        writer_test = csv.writer(csvfile_test)

        lower = time_list[k*length/num]
        try :
            upper = time_list[(k+1)*length/num]
        except Exception as e:
            upper = time_list[-1]

        for i in range(0,length):
            if df_user['time_stamp'][i]>=lower and df_user['time_stamp'][i]<upper :
                writer_test.writerow(['',df_user['user_id'][i],df_user['shop_id'][i],df_user['time_stamp'][i],
                                      df_user['longitude'][i],df_user['latitude'][i],df_user['wifi_infos'][i]])

        csvfile_test.close()
    
    
if __name__ == '__main__':

    my_path = 'D:/tianchi_multiclass/data'
    dir_count = 0

    for dirpath,_,_ in os.walk(my_path):
        #if dirpath != 'D:/tianchi_multiclass/data\m_615' :
        #    continue
        if dirpath == 'D:/tianchi_multiclass/data' or len(dirpath) >= 40:
            continue
        
        user_scatter(dirpath)
        
        print dirpath
