import os
import csv
import pandas as pd
from pandas.io.parsers import read_csv

my_path = 'D:/tianchi/'
df_shop = read_csv( my_path +'ccf_first_round_shop_info.csv' )

mall_set = set()
shop2mall = dict()

for i in range(0,len(df_shop)):
    
    mall_id = df_shop['mall_id'][i]
    shop_id = df_shop['shop_id'][i]
    shop2mall[shop_id] = mall_id

df_user = read_csv( my_path +'ccf_first_round_user_shop_behavior.csv' )

for i in range(0,len(df_user)):
    if i%10000 == 0:
        print i
        
    shop_id = df_user['shop_id'][i]
    mall_id = shop2mall[shop_id]
    
    fname = my_path +'data/%s/user_info.csv'%mall_id
    
    if not mall_id in mall_set :
        df_result = pd.DataFrame(columns=('user_id','shop_id','time_stamp',
                                          'longitude','latitude','wifi_infos'))
        df_result.to_csv(fname)
        mall_set.add(mall_id)
        
    csvfile = file(fname, 'ab+')
    writer = csv.writer(csvfile)
    writer.writerow(['',df_user['user_id'][i],df_user['shop_id'][i],df_user['time_stamp'][i],
                     df_user['longitude'][i],df_user['latitude'][i],df_user['wifi_infos'][i]])
    csvfile.close()
