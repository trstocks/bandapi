from flask import Flask, jsonify, abort,request, url_for, redirect
import os
app = Flask(__name__)

bands = [
    {
        'id': 1,
        'name': u'Stormageddon and the Dark Lords of All',
        'genre':u'Heavy Metal'
    },
    {
        'id': 2,
        'name': u'The Pickle Ricks',
        'genre': u'Blues'
    },
    {
        'id': 3,
        'name': u'Samwise and the Gamgees',
        'genre':u'Folk'
    },
    {
        'id': 4,
        'name': u'The Porta Potties',
        'genre': u'Grunge'
    },
    {
        'id': 5,
        'name': u'Newsweek Headline',
        'genre':u'Alternative'
    },
    {
        'id': 6,
        'name': u'Syringe Dipity',
        'genre': u'Dubstep'
    },
    {
        'id': 7,
        'name': u'Red Bean and the Mochis',
        'genre': u'Youtube AMV music'
     },
    {
        'id': 8,
        'name': u'FailStorm',
        'genre': u'Crock'
    }
 ]

def make_public_band(band):
    new_band={}
    for field in band:
        if field == 'id':
            new_band['uri'] = url_for('get_band', band_id=band['id'],
            _external=True)
        else:
            new_band[field] = band[field]
    return new_band

@app.route('/',methods=['GET'])
def get_index():
    return "This is a placeholder"

@app.route('/favicon.ico')
def get_favicon():
    return redirect(url_for('static', filename='favicon.ico'), code=302)

@app.route('/band/api/v1.0/bands',methods=['GET'])
def get_bands():
    return jsonify({'bands':[make_public_band(band) for band in bands]})


@app.route('/band/api/v1.0/bands',methods=['POST'])
def create_bands():
    if not request.json or not 'name' in request.json:
        abort(400)
    band = {
        'id': bands[-1]['id'] + 1,
        'name': request.json['name'],
        'genre': request.json.get('genre',"")
    }
    bands.append(band)
    return jsonify({'band': band}),201

@app.route('/band/api/v1.0/bands/<int:band_id>',methods=['GET'])
def get_band(band_id):
    band = [band for band in bands if band['id'] == band_id]
    if len(band) == 0:
        abort(404)
    return jsonify({'band': band[0]})


@app.route('/todo/api/v1.0/bands/<int:band_id>', methods=['PUT'])
def update_band(band_id):
    band = [band for band in bands if band['id'] == band_id]
    if len(band) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) != unicode:
        abort(400)
    if 'genre' in request.json and type(request.json['genre']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    band[0]['name'] = request.json.get('name', band[0]['name'])
    band[0]['genre'] = request.json.get('genre', band[0]['genre'])
    return jsonify({'band': band[0]})

@app.route('/todo/api/v1.0/bands/<int:band_id>', methods=['DELETE'])
def delete_band(band_id):
    band = [band for band in bands if band['id'] == band_id]
    if len(band) == 0:
        abort(404)
    bands.remove(band[0])
    return jsonify({'result': True})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
