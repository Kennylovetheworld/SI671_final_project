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

from interactive import *

def getGameList(query, Ri_amount = 500, top_n_game = 50):
    try:
        with open('Retrieval_base.pickle', 'rb') as handle:
            Rb = pickle.load(handle)
    except:
        Rb = Retrieval_base()
        with open('Retrieval_base.pickle', 'wb') as handle:
            pickle.dump(Rb, handle, protocol=pickle.HIGHEST_PROTOCOL)
    Ri = Retrival_Interface(Rb, query, Ri_amount)
    base_retrieve_list = Ri.Base_Retrieve_List()
    out_df = Ri.retrieve_detail_info(top_n_game, score_mode=True)
    
    return out_df


def getUserGameScore(uid, iid, df_user, df_item):
    clf1 = load('models/clf_xgb.joblib') 

    try:
        ## Get feature
        clf1 = load('clf_xgb.joblib') 
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

    model = pickle.load(open( "models/utime_svd.pkl", "rb" ) )
    result_surprise = model.predict(iid, uid).est
    if result_xgb != -1: 
        result = 0.5 * result_surprise + 0.5 * result_xgb
    else:
        result = result_surprise

    return result

def userBasedRetrieval(uid, query):
    df_user = pd.read_csv('user_game/user_feature.csv')
    df_item = pd.read_csv('user_game/game_property.csv')
    retrieved_games = getGameList(query)
    user_game_scores = []
    for gid in list(retrieved_games.index):
        user_game_scores.append(getUserGameScore(uid, gid, df_user, df_item))
    retrieved_games['user_game_score'] = user_game_scores
    retrieved_games['new_score'] = retrieved_games['score'] + retrieved_games['user_game_score']
    retrieved_games['original_rank'] = retrieved_games['score'].rank(ascending = False)
    retrieved_games['new_rank'] = retrieved_games['new_score'].rank(ascending = False)
    return retrieved_games
