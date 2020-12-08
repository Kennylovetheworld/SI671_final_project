from userretrieval import *
import random
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from rake_nltk import Rake

nltk.download('punkt')

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
    if len(game_df[game_df['appid'] == gid]) == 0: 
        return "game"
    try:
        fake_query = game_df[game_df['appid'] == gid]['short_description'].values[0]
    except:
        fake_query = game_df[game_df['appid'] == gid]['short_description'].values
    # print(fake_query)
    # tokens = word_tokenize(fake_query)
    # token_samples = random.sample(tokens, int(len(tokens) * 0.1))
    r = Rake()
    r.extract_keywords_from_text(fake_query)
    token_samples = r.get_ranked_phrases()
    if len(token_samples) < 2:
        fake_query = ' '.join(token for token in token_samples)
    else:
        token_samples = random.sample(token_samples, 2)
        fake_query = ' '.join(token for token in token_samples)
    return fake_query


users = random.sample(list(user_game_df['uid'].unique()), 100)
for uid in users:
    
    last_gid = find_last_game(uid)
    fake_query =gid_to_fake_query(last_gid)
    print(fake_query)
    gname = gid_to_name(last_gid)
    retrieved_games = userBasedRetrieval(uid, fake_query)

    try:
        original_rank = retrieved_games.loc[last_gid]['original_rank']
    except:
        original_rank = -1
    try: 
        new_rank = retrieved_games.loc[last_gid]['new_rank']
    except:
        new_rank = -1
    print(original_rank)
    print(new_rank)
    if original_rank > new_rank:
        pdb.set_trace()
        # retrieved_games[['name', 'score', 'new_score', 'original_rank', 'new_rank']].sort_values('new_rank')

