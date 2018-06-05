import json
import pandas as pd
import requests

pd.set_option('display.max_columns', 500)


triplets_file = '10000.txt'
songs_metadata_file = 'song_data.csv'

song_df_1 = pd.read_table(triplets_file, header = None)

print("song dataframe 1")
print(song_df_1.head())

song_df_1.columns = ['user_id', 'song_id', 'listen_count']

print("song dataframe 1 - columned")
print(song_df_1.head())

song_df_2 = pd.read_csv(songs_metadata_file)

print("song dataframe 2")
print(song_df_2.head())

song_df = pd.merge(song_df_1, song_df_2.drop_duplicates(['song_id']), on="song_id", how = "left")

print("song dataframe merged")
print("song dataframe columns :")
print(song_df.columns)

# df is a dataframe or dataframe chunk coming from your reading logic
df['_id'] = df['column_1'] + '_' + df['column_2'] # or whatever makes your _id
df_as_json = df.to_json(orient='records', lines=True)

final_json_string = ''
for json_document in df_as_json.split('\n'):
    jdict = json.loads(json_document)
    metadata = json.dumps({'index': {'_id': jdict['_id']}})
    jdict.pop('_id')
    final_json_string += metadata + '\n' + json.dumps(jdict) + '\n'

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post('http://elasticsearch.host:9200/my_index/my_type/_bulk', data=final_json_string, headers=headers, timeout=60)