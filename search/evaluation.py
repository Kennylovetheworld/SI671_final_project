from userretrieval import *
import random
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

df_item = pd.read_csv('user_game/game_property.csv')
game_df = pd.read_excel("steam_clean.xlsx",index_col=0)
user_game_df =  pd.read_csv('user_game/sampled_time.csv')

def find_last_game(uid):
    gid = user_game_df[user_game_df['uid'] == uid]['gid'].values[-1]
    return gid

def gid_to_name(gid):
    try: 
        output = game_df[game_df['appid'] == gid]['name'].values[0]
    except:
        output = game_df[game_df['appid'] == gid]['name'].values
    return output

def gid_to_fake_query(gid):
    try:
        fake_query = game_df[game_df['appid'] == gid]['short_description'].values[0]
    except:
        fake_query = game_df[game_df['appid'] == gid]['short_description'].values
    
    return fake_query


users = random.sample(list(user_game_df['uid'].unique()), 100)
for uid in users:
    pdb.set_trace()
    last_gid = find_last_game(uid)
    fake_query =gid_to_fake_query(last_gid)
    gname = gid_to_name(last_gid)
    retrieved_games = userBasedRetrieval(uid, fake_query)
    
    original_rank = retrieved_games.loc[last_gid]['original_rank']
    new_rank = retrieved_games.loc[last_gid]['new_rank']
    print(original_rank)
    print(new_rank)

# userBasedRetrieval(uid, query)

