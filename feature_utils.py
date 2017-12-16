from pandas.io.parsers import read_csv
from datetime import datetime,date


def wifi_feature_set(fname):

    global threshold1,threshold2,mnr_param,merge
    df_wifi = read_csv(fname)
    merge = 2
    '''
    threshold1 = 0.001
    threshold2 = 0.005
    mnr_param = 0.2

    total_count = 0
    total_true = 0
    
    #wifi_mean = dict()

    for i in range(0,len(df_wifi)):
        total_count = total_count + df_wifi['wifi_count'][i]
        total_true = total_true + df_wifi['wifi_true'][i]
        #wifi_id = df_wifi['wifi_id'][i]
        #wifi_mean[wifi_id] =  df_wifi['wifi_mean'][i]

    threshold1 = int(threshold1*total_count)
    threshold1_mnr = int(threshold1*mnr_param)
    threshold2 = int(threshold2*total_true)
    threshold2_mnr = int(threshold2*mnr_param)

    if threshold2_mnr < 1 :
        threshold2_mnr = 1
    '''
    threshold1 = 30
    threshold1_mnr = 5
    threshold2 = 5
    threshold2_mnr = 2
    
    wifi_set1 = set()
    wifi_set1_mnr = set()
    wifi_set2 = set()
    wifi_set2_mnr = set()

    for i in range(0,len(df_wifi)):
        if df_wifi['wifi_count'][i] >= threshold1 :
            wifi_set1.add(df_wifi['wifi_id'][i])
        elif df_wifi['wifi_count'][i] >= threshold1_mnr :
            wifi_set1_mnr.add(df_wifi['wifi_id'][i])
        if df_wifi['wifi_true'][i] >= threshold2 :
            wifi_set2.add(df_wifi['wifi_id'][i])
        elif df_wifi['wifi_true'][i] >= threshold2_mnr :
            wifi_set2_mnr.add(df_wifi['wifi_id'][i])
    
    return wifi_set1, wifi_set2, wifi_set1_mnr, wifi_set2_mnr


def wifi_set2dict(wifi_set):
    
    index = 0
    wifi_dict = dict()
    for wifi in wifi_set:
        wifi_dict[wifi] = index
        index = index + 1

    return wifi_dict


def wifi_set2dict_mnr(wifi_set):
    
    index = 0
    wifi_dict = dict()
    for wifi in wifi_set:
        wifi_dict[wifi] = index / merge
        index = index + 1

    return wifi_dict


def get_wifi_feature(wifi_infos,wifi_dict1,wifi_dict2,wifi_dict1_mnr,wifi_dict2_mnr):
    
    wifis = wifi_infos.split(';')
    wifi_vector1 = [ -100 for i in range(0,len(wifi_dict1)) ]
    wifi_vector2 = [ 0 for i in range(0,len(wifi_dict2)) ]
    wifi_vector1_mnr = [ -100 for i in range(0,1+len(wifi_dict1_mnr)/merge) ]
    wifi_vector2_mnr = [ 0 for i in range(0,1+len(wifi_dict2_mnr)/merge) ]

    wifi_minus = 0

    for wifi in wifis :
        w_id = wifi.split('|')[0]
        w_strength = float(wifi.split('|')[1])
        if w_strength < wifi_minus :
            wifi_minus = w_strength
        w_flag = wifi.split('|')[2]

        if w_id in wifi_dict1.keys() :
            index = wifi_dict1[w_id]
            wifi_vector1[index] = w_strength
        elif w_id in wifi_dict1_mnr.keys() :
            index = wifi_dict1_mnr[w_id]
            if w_strength > wifi_vector1_mnr[index] :
                wifi_vector1_mnr[index] = w_strength
            
        if w_id in wifi_dict2.keys() :
            index = wifi_dict2[w_id]
            wifi_vector2[index] = (1 if w_flag == 'true' else 0)
        elif w_id in wifi_dict2_mnr.keys() :
            index = wifi_dict2_mnr[w_id]
            if w_flag == 'true' :
                wifi_vector2_mnr[index] = 1

    wifi_vector = wifi_vector1[:]
    wifi_vector.extend(wifi_vector2)
    wifi_vector.extend(wifi_vector1_mnr)
    wifi_vector.extend(wifi_vector2_mnr)
    return wifi_vector


def get_time_feature(time_stamp):
    
    time_stamp = time_stamp.replace('  ',' ')
    dt = time_stamp.split(' ')[0]
    time = time_stamp.split(' ')[1]
    weekday = date.weekday(datetime.strptime(dt,'%Y-%m-%d'))
    minute = int(time.split(':')[0])*60 + int(time.split(':')[1])
    vector = [ 0 for i in range(0,9)]
    vector[weekday] = 1
    vector[7] = minute
    if weekday < 4 :
        vector[8] = 0
    else :
        vector[8] = 1
        
    return vector


def get_user_feature(fname):
    user_df = read_csv(fname)
    
    user_sct = dict()
    for i in range(0,len(user_df)):
        user_id = user_df['user_id'][i]
        vector = list(user_df.iloc[i,2:])
        for j in range(0,len(vector)):
            if vector[j] < 3 :
                vector[j] = 0
        user_sct[user_id] = vector

    length = len(user_df.columns) - 2
    return user_sct,length


def shop2dict(filename):
    shop_df = read_csv(filename)
    
    shop_dict = dict()
    shop_dict_rv = dict()
    for i in range(0,len(shop_df)):
        key = shop_df['shop_id'][i]
        shop_dict[key] = i
        shop_dict_rv[i] = key

    return shop_dict,shop_dict_rv


def target2vector(shop_id,shop_dict):
    vector = [0 for i in range(0,len(shop_dict))]
    index = shop_dict[shop_id]
    vector[index] = 1
    return vector


def count_shop(df):
    count = dict()
    for i in range(0,len(df)) :
        if not count.has_key(df['shop_id'][i]) :
            count[ df['shop_id'][i] ] = 1
        else :
            count[ df['shop_id'][i] ] = count[ df['shop_id'][i] ] + 1
    return count


def get_wifi_pairs(file_name):
    df = read_csv(file_name)
    pairs = set()
    for i in range(0,len(df)):
        pairs.add(df['wifi_pair'][i])
    return pairs


def pairs_feature(wifi_infos,wifi_pairs):
    wifis = wifi_infos.split(';')

    wifi_dict = dict()
    mini_strength = 0

    for wifi in wifis :
        w_id = wifi.split('|')[0]
        w_strength = float(wifi.split('|')[1])
        wifi_dict[w_id] = w_strength
        if w_strength < mini_strength :
            mini_strength = w_strength

    mini_strength = mini_strength - 10
    
    feature = []

    for wp in wifi_pairs :
        w_id1 = wp.split(',')[0]
        w_id2 = wp.split(',')[1]
        delta = 0
        
        if wifi_dict.has_key(w_id1) and wifi_dict.has_key(w_id2) :
            delta = wifi_dict[w_id1] - wifi_dict[w_id2]
        elif wifi_dict.has_key(w_id1) :
            delta = wifi_dict[w_id1] - mini_strength
        elif wifi_dict.has_key(w_id2) :
            delta = mini_strength - wifi_dict[w_id2]

        feature.append(delta)

    return feature
