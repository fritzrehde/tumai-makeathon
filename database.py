import pandas as pd
from flask import Flask, jsonify
from tinydb import TinyDB, Query, where

from energy_factors.buildings import get_df

# Create a TinyDB database and a table
db = TinyDB('database/tinydb.json')
table = db.table('buildings')

# Convert the DataFrame to a dictionary and insert it into the table
print("Debug: started loading dataframe into tinydb")

# df = get_df();
df = pd.read_csv('generated_data/test_bremen.csv');
table.insert(df.to_dict())

print("Debug: finished loading dataframe into tinydb")

app = Flask(__name__)

@app.route('/data/<float:latitude>/<float:longitude>', methods=['GET'])
def get_data(latitude, longitude):
    # record = db.search((where('roof_location_latitude') == latitude) & (where('roof_location_longitude') == longitude))
    # if record:
    #     return jsonify(record[0])
    # else:
    #     return jsonify({'error': 'Record not found'})

    # record = df[(df['roof_location_latitude'] == latitude) & (df['roof_location_longitude'] == longitude)]
    # if not record.empty:
    #     return jsonify(record.to_dict('records')[0])
    # else:
    #     return jsonify({'error': 'Record not found'})

    query = Query()
    record = table.search((query.roof_location_latitude == latitude) & (query.roof_location_longitude == longitude))
    if record:
        return jsonify(record[0])
    else:
        return jsonify({'error': 'Record not found'})

if __name__ == '__main__':
    app.run(debug=True)
