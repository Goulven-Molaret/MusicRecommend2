import pandas as pd
import json
import requests

pd.set_option('display.max_columns', 500)

triplets_file = '10000.txt'
songs_metadata_file = 'song_data.csv'

song_df_1 = pd.read_table(triplets_file, header = None)
song_df_2 = pd.read_csv(songs_metadata_file)
song_df_1.columns = ['user_id', 'song_id', 'listen_count']
song_df = pd.merge(song_df_1, song_df_2.drop_duplicates(['song_id']), on="song_id", how = "left")
songs = song_df[song_df['listen_count'] > 100]
fsongs = songs.drop_duplicates(subset = 'song_id')

fsongs['_id'] = fsongs['song_id']
fsongs = fsongs[['_id', 'song_id', 'title', 'artist_name', 'release', 'year']]
print(fsongs.head(100))
print(fsongs.size)

#print(songs_short)

for i in range(0, songs.size, 10):
	songs_short = fsongs[i:i+20]
	df_as_json = songs_short.to_json(orient='records', lines=True)

	final_json_string = ''
	for json_document in df_as_json.split('\n'):
	    jdict = json.loads(json_document)
	    metadata = json.dumps({'index': {'_id': jdict['_id']}})
	    jdict.pop('_id')
	    final_json_string += metadata + '\n' + json.dumps(jdict) + '\n'

	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	r = requests.post('http://localhost:9200/famoussongs100/text/_bulk', data=final_json_string, headers=headers, timeout=60)

	print(r.json())

"""
df_as_json = songs_short.to_json(orient='records', lines=True)



final_json_string = ''
for json_document in df_as_json.split('\n'):
    jdict = json.loads(json_document)
    metadata = json.dumps({'index': {'_id': jdict['_id']}})
    jdict.pop('_id')
    final_json_string += metadata + '\n' + json.dumps(jdict) + '\n'

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post('http://localhost:9200/index0/my_type/_bulk', data=final_json_string, headers=headers, timeout=60)

print(r.json())"""