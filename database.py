import pandas as pd
from flask import Flask, jsonify, request, abort
from tinydb import TinyDB, Query, where

from energy_factors.buildings import get_df

# Create a TinyDB database and a table
# db = TinyDB('database/tinydb.json')
# table = db.table('buildings')

df = get_df();
# table.insert(df.to_dict())

# Convert the DataFrame to a dictionary and insert it into the table
print("Debug: started loading dataframe into tinydb")

app = Flask(__name__)

@app.route('/data', methods=['GET'])
def get_data():
    street = request.args.get('street')
    housenumber = request.args.get('housenumber')
    postcode = request.args.get('postcode')

    # Search the TinyDB database
    # results = table.search((where('addr:street') == street) & 
    #                        (where('addr:housenumber') == housenumber) &
    #                        (where('addr:postcode') == postcode))
    # # Return the results as a JSON response
    # if results:
    #     return jsonify(results)
    # else:
    #     return jsonify({'error': 'No matching addresses found'})

    record = df[(df['addr:street'] == street) & (df['addr:housenumber'] == housenumber) & (df['addr:postcode'] == postcode)]
    if not record.empty:
        return jsonify(record.to_dict('records')[0])
    else:
        abort(404, description="Record not found")

if __name__ == '__main__':
    app.run(debug=True)
