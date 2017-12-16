import os
import csv
import pandas as pd
from pandas.io.parsers import read_csv

my_path = 'D:/tianchi/'
mall_set = set()
df_user = read_csv( my_path +'evaluation_public.csv' )

for i in range(0,len(df_user)):
    if i%10000 == 0:
        print i
        
    mall_id = df_user['mall_id'][i]
    
    fname = my_path +'data/%s/test_info.csv'%mall_id
    
    if not mall_id in mall_set :
        df_result = pd.DataFrame(columns=('row_id','user_id','mall_id','time_stamp',
                                          'longitude','latitude','wifi_infos'))
        df_result.to_csv(fname)
        mall_set.add(mall_id)
        
    csvfile = file(fname, 'ab+')
    writer = csv.writer(csvfile)
    writer.writerow(['',df_user['row_id'][i],df_user['user_id'][i],
                     df_user['mall_id'][i],df_user['time_stamp'][i],
                     df_user['longitude'][i],df_user['latitude'][i],df_user['wifi_infos'][i]])
    csvfile.close()
