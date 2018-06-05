import pandas as pd
import Recommenders
from sklearn.model_selection import train_test_split

pm = Recommenders.item_similarity_recommender_py()

pd.set_option('display.max_columns', 500)


def test():
	print("hello world !")

	return True

def create_model():
	

	triplets_file = '10000.txt'
	songs_metadata_file = 'song_data.csv'
	global song_df_2
	song_df_1 = pd.read_table(triplets_file, header = None)

	song_df_1.columns = ['user_id', 'song_id', 'listen_count']

	song_df_2 = pd.read_csv(songs_metadata_file)

	song_df = pd.merge(song_df_1, song_df_2.drop_duplicates(['song_id']), on="song_id", how = "left")

	songss = song_df.head(200)
	#train_data, test_data = train_test_split(songss, test_size = 0.20, random_state=0)

	global pm

	#print(song_df['song_id'])
	print("Creating the model")
	pm.create(songss, 'user_id', 'song_id')
	#print(song_df.head())
	#print(song_df[song_df['song_id'] == 'SOAKIMP12A8C130995'])

	return True

def recommend(listSelection):
	print("List selection :")
	print(listSelection)

	result = pm.get_similar_items(listSelection)
	print("result")
	print(result)
	listResults = result.song.tolist()
	print("List results :")
	print(listResults)
	return listResults

def titleOf(song_id):
	row = song_df_2[song_df_2['song_id'] == song_id]
	title = row.iloc[0]['title']
	print("title of "+str(song_id)+ " : ")
	print(title)
	#print(song_df_2[song_df_2['song_id'] == song_id])
	return title
"""
create_model()
l = ['SOAKIMP12A8C130995','SOBBMDR12A8C13253B', 'SOBXHDL12A81C204C0']
recommend(l)
"""