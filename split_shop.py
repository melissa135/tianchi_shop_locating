'''
Split shops from ccf_first_round_shop_info.csv into shop_info.csv in each mall directory.
Meanwhile, mkdir if the mall_id is met firstly.
'''
import os
import csv
import pandas as pd
from pandas.io.parsers import read_csv

my_path = 'D:/tianchi/'
df_shop = read_csv( my_path +'ccf_first_round_shop_info.csv' )

mall_set = set()

for i in range(0,len(df_shop)):
    
    mall_id = df_shop['mall_id'][i]
    fname = my_path +'data/%s/shop_info.csv'%mall_id
    
    if not mall_id in mall_set :
        os.mkdir(my_path + 'data/%s'%mall_id)
        df_result = pd.DataFrame(columns=('shop_id','category_id',
                                          'longitude','latitude','price','mall_id'))
        df_result.to_csv(fname)
        mall_set.add(mall_id)
        
    csvfile = file(fname, 'ab+')
    writer = csv.writer(csvfile)
    writer.writerow(['',df_shop['shop_id'][i],df_shop['category_id'][i],
                     df_shop['longitude'][i],df_shop['latitude'][i],
                     df_shop['price'][i],df_shop['mall_id'][i]])
    csvfile.close()
