import os
import csv
import random
import numpy as np
import pandas as pd
import xgboost as xgb
from feature_utils import * 
from pandas.io.parsers import read_csv

  
def train_xgb(path):

    global wifi_dict1,wifi_dict2,wifi_dict1_mnr,wifi_dict2_mnr,shop_dict,shop_dict_rv
    global num

    fname = path + '/wifi_info.csv'
    wifi_set1, wifi_set2, wifi_set1_mnr, wifi_set2_mnr = wifi_feature_set(fname)
    wifi_dict1 = wifi_set2dict(wifi_set1)
    wifi_dict2 = wifi_set2dict(wifi_set2)
    wifi_dict1_mnr = wifi_set2dict_mnr(wifi_set1_mnr)
    wifi_dict2_mnr = wifi_set2dict_mnr(wifi_set2_mnr)

    fname = path + '/shop_info.csv'
    shop_dict,shop_dict_rv = shop2dict(fname)

    xgb_list = []
    score_list = []

    for k in range(0,num):

        fname = path + '/user_scatter_%d.csv'%k
        user_sct,length = get_user_feature(fname)

        df_test = read_csv(path + '/subset_%d.csv'%k)

        tmp_list = [ j for j in range(0,num) ]
        tmp_list.remove(k)
        df_train = read_csv(path + '/subset_%d.csv'%tmp_list[0])
        for j in range(1,len(tmp_list)) :
            df_tmp = read_csv(path + '/subset_%d.csv'%tmp_list[j])
            df_train = pd.concat([df_train,df_tmp],ignore_index=True)
        df_train = pd.DataFrame(df_train)

        samples_per_shop = (len(df_train)+0.0)/len(shop_dict)
        shop_count = count_shop(df_train)

        train_X = []  
        train_Y = []
        test_X = []  
        test_Y = []

        for i in range(0,len(df_train)):
                
            time_stamp = df_train['time_stamp'][i]
            longitude = df_train['longitude'][i]
            latitude = df_train['latitude'][i]
            rotate_x = longitude + latitude
            rotate_y = -longitude + latitude
            wifi_infos = df_train['wifi_infos'][i]
            shop_id = df_train['shop_id'][i]
            user_id = df_train['user_id'][i]

            vector = get_time_feature(time_stamp)
            vector.extend([longitude,latitude,rotate_x,rotate_y])
            
            v_wifi = get_wifi_feature(wifi_infos,wifi_dict1,wifi_dict2,wifi_dict1_mnr,wifi_dict2_mnr)
            vector.extend(v_wifi)
            '''
            if user_sct.has_key(user_id) :
                u_vec = user_sct[user_id]
            else :
                u_vec = [ 0 for j in range(0,length)]
            vector.extend(u_vec)
            '''
            train_X.append(vector)
            train_Y.append(shop_dict[shop_id])
            rand = random.uniform(0,samples_per_shop/shop_count[shop_id])
            if int(rand) >= 1 :
                for m in range(0,int(rand)-1):
                    train_X.append(vector)
                    train_Y.append(shop_dict[shop_id])

        for i in range(0,len(df_test)):
                
            time_stamp = df_test['time_stamp'][i]
            longitude = df_test['longitude'][i]
            latitude = df_test['latitude'][i]
            rotate_x = longitude + latitude
            rotate_y = -longitude + latitude
            wifi_infos = df_test['wifi_infos'][i]
            shop_id = df_test['shop_id'][i]
            user_id = df_test['user_id'][i]

            vector = get_time_feature(time_stamp)
            vector.extend([longitude,latitude,rotate_x,rotate_y])
            
            v_wifi = get_wifi_feature(wifi_infos,wifi_dict1,wifi_dict2,wifi_dict1_mnr,wifi_dict2_mnr)
            vector.extend(v_wifi)
            '''
            if user_sct.has_key(user_id) :
                u_vec = user_sct[user_id]
            else :
                u_vec = [ 0 for j in range(0,length)]
            vector.extend(u_vec)
            '''
            test_X.append(vector)
            test_Y.append(shop_dict[shop_id])
                
        train_X = np.array(train_X)
        train_Y = np.array(train_Y)
        test_X = np.array(test_X)
        test_Y = np.array(test_Y)

        xgb_train = xgb.DMatrix( train_X, label=train_Y)  
        xgb_test = xgb.DMatrix( test_X, label=test_Y )
             
        param = {}    
        param['eta'] = 0.10
        param['gamma'] = 0.1
        param['max_depth'] = 5
        param['min_child_weight'] = 1
        param['subsample'] = 0.5
        param['colsample_bytree'] = 0.5
        param['scale_pos_weight'] = 2
        param['lambda'] = 2.0
        param['alpha'] = 0.4
        param['silent'] = 1  
        param['num_class'] = len(shop_dict) 
              
        evallist = [ (xgb_train,'train'), (xgb_test, 'test') ]  
        num_round = 200

        param['eval_metric'] = 'merror'
        param['objective'] = 'multi:softmax' 
        bst = xgb.train(param, xgb_train, num_round, evallist )

        pred = bst.predict( xgb_test )
        score = (sum( int(pred[i]) != test_Y[i] for i in range(len(test_Y))) / float(len(test_Y)) )

        xgb_list.append(bst)
        score_list.append(score)

    return xgb_list,score_list


def predict_xgb(path,xgb_list):

    df_test = read_csv(path + '/test_info.csv')

    global wifi_dict1,wifi_dict2,wifi_dict1_mnr,wifi_dict2_mnr,shop_dict,shop_dict_rv
    global num

    pred_list = []

    for k in range(0,num):

        fname = path + '/user_scatter_%d.csv'%k
        user_sct,length = get_user_feature(fname)

        test_X = []
        
        for i in range(0,len(df_test)):
                
            time_stamp = df_test['time_stamp'][i]
            longitude = df_test['longitude'][i]
            latitude = df_test['latitude'][i]
            rotate_x = longitude + latitude
            rotate_y = -longitude + latitude
            wifi_infos = df_test['wifi_infos'][i]
            user_id = df_test['user_id'][i]

            vector = get_time_feature(time_stamp)
            vector.extend([longitude,latitude,rotate_x,rotate_y])
            
            v_wifi = get_wifi_feature(wifi_infos,wifi_dict1,wifi_dict2,wifi_dict1_mnr,wifi_dict2_mnr)
            vector.extend(v_wifi)
            '''
            if user_sct.has_key(user_id) :
                u_vec = user_sct[user_id]
            else :
                u_vec = [ 0 for j in range(0,length)]
            vector.extend(u_vec)
            '''
            test_X.append(vector)

        test_X = np.array(test_X)
        xgb_test = xgb.DMatrix( test_X )

        bst = xgb_list[k]
        pred = bst.predict( xgb_test )
        pred_list.append(pred)
        
    result = []

    for i in range(0,len(test_X)):
        
        vote = dict()
        for k in range(0,num):
            if pred_list[k][i] in vote.keys() :
                vote[pred_list[k][i]] = vote[pred_list[k][i]] + 1
            else :
                vote[pred_list[k][i]] = 1
                
        maxi = 0
        max_index = 0
        for k in vote.keys() :
            if vote[k] > maxi :
                max_index = k
                maxi = vote[k]

        result.append(max_index)

    df_result = pd.DataFrame(columns=('row_id','shop_id'))
    fname = path + '/result.csv'
    df_result.to_csv(fname)

    csvfile = file(fname, 'ab+')
    for i in range(0,len(df_test)) :        
        writer = csv.writer(csvfile)
        writer.writerow([ '',df_test['row_id'][i],shop_dict_rv[result[i]] ])
    csvfile.close()


if __name__ == '__main__':

    my_path = 'D:/tianchi_multiclass/data'
    dir_count = 0

    global num
    num = 5

    for dirpath,_,_ in os.walk(my_path):
        if dirpath == 'D:/tianchi_multiclass/data':
            continue
        if len(dirpath) > 40 :
            continue

        dir_count = dir_count + 1
        if dir_count < 78 :
            continue

        print dirpath
        
        xgb_list,score_list = train_xgb(dirpath)

        xgb_list_disk = [ '' for i in range(0,num) ]
        score_list_disk = [ 1.0 for i in range(0,num) ]

        for root,_,files in os.walk(dirpath):
            for f in files :
                if os.path.splitext(f)[1] == '.model':
                    model_name = os.path.join(root,f)
                    try :
                        tmp = f.replace('.model','')
                        model_index = int(tmp.split('_')[1])
                        model_score = float(tmp.split('_')[2])
                        xgb_list_disk[model_index] = model_name
                        score_list_disk[model_index] = model_score
                    except Exception as e:
                        print e
        
        for i in range(0,num) :
            print score_list_disk[i],score_list[i]
            if score_list[i] < score_list_disk[i] :
                try :
                    os.remove(xgb_list_disk[i])
                except Exception as e :
                    print e
                xgb_list[i].save_model(dirpath + '/xgb_%d_%f.model'%(i,score_list[i]))

        xgb_list_best = []
        for root,_,files in os.walk(dirpath):
            for f in files :
                if os.path.splitext(f)[1] == '.model':
                    model_name = os.path.join(root,f)
                    bst = xgb.Booster()
                    bst.load_model(model_name)
                    xgb_list_best.append(bst)
                    
        predict_xgb(dirpath,xgb_list_best)
