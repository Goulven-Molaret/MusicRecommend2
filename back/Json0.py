import pandas as pd
import json
import requests

pd.set_option('display.max_columns', 500)

song_metadata_file = 'song_data.csv'

songs = pd.read_csv(song_metadata_file)

songs['_id'] = songs['song_id']
songs_short = songs.head(20)

#print(songs_short)

df_as_json = songs_short.to_json(orient='records', lines=True)



final_json_string = ''
for json_document in df_as_json.split('\n'):
    jdict = json.loads(json_document)
    metadata = json.dumps({'index': {'_id': jdict['_id']}})
    jdict.pop('_id')
    final_json_string += metadata + '\n' + json.dumps(jdict) + '\n'

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post('http://localhost:9200/index0/my_type/_bulk', data=final_json_string, headers=headers, timeout=60)

print(r.json())