import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from xgboost import XGBClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.linear_model import RidgeClassifier, LogisticRegression
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn import linear_model
from sklearn.metrics import mean_absolute_error
from sklearn.svm import SVR, SVC
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
import xgboost as xg 
import pickle
from joblib import dump, load
import sys
import warnings
warnings.simplefilter("ignore")

uid = sys.argv[1]
iid = int(sys.argv[2])

clf1 = load('clf_xgb.joblib') 

try:
    ## Get feature
    clf1 = load('clf_xgb.joblib') 
    df_user = pd.read_csv('user_feature.csv')
    df_item = pd.read_csv('game_property.csv')
    feature = []
    #User
    feature.append(df_user[df_user['uid'] == uid]['items_count'].values[0])
    feature.append(df_user[df_user['uid'] == uid]['avg_playtime'].values[0])
    feature.append(df_user[df_user['uid'] == uid]['count_review'].values[0])
    feature.append(df_user[df_user['uid'] == uid]['count_recommend'].values[0])
    feature.append(df_user[df_user['uid'] == uid]['avg_review_length'].values[0])
    #Game

    feature.append(df_item[df_item['appid'] == iid]['english'].values[0])
    feature.append(df_item[df_item['appid'] == iid]['required_age'].values[0])
    feature.append(df_item[df_item['appid'] == iid]['achievements'].values[0])
    feature.append(df_item[df_item['appid'] == iid]['positive_ratings'].values[0])
    feature.append(df_item[df_item['appid'] == iid]['negative_ratings'].values[0])
    feature.append(df_item[df_item['appid'] == iid]['median_playtime'].values[0])
    feature.append(df_item[df_item['appid'] == iid]['price'].values[0])

    result_xgb = clf1.predict(np.array([feature]))[0]
except:
    result_xgb = -1



model = pickle.load(open( "utime_svd.pkl", "rb" ) )
result_surprise = model.predict(iid, uid).est
if result_xgb != -1: 
    result = 0.5 * result_surprise + 0.5 * result_xgb
else:
    result = result_surprise

print('prediction result is ' + str(result))