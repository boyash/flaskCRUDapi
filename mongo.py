from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

app = Flask(__name__)

# app.config['MONGO_DBNAME'] = ''
app.config['MONGO_URI'] = 'mongodb://rendi:rendimaagi123@ds261540.mlab.com:61540/firstfly'

mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def home():
	return "<h1>HAIL MONGO<h1>"

@app.route('/star', methods=['GET'])
def get_all_stars():
 	star = mongo.db.stars
 	output = []
 	for s in star.find():
 		output.append({'name': s['name'], 'distance' : s['distance']})
 	print(output)
 	return jsonify ({'result' : output})
 	# return output

@app.route('/star/<name>', methods=['GET'])
def get_one_star(name):
 	star = mongo.db.stars
 	s = star.find_one({'name' : name})
 	if s:
 	  output = {'name' : s['name'], 'distance' : s['distance']}
 	else:
 	  output = "No such name"
 	return jsonify({'result' : output})

@app.route('/star', methods=['POST'])
def add_star():
 	star = mongo.db.stars
 	name = request.json['name']
 	distance = request.json['distance']
 	star_id = star.insert({'name' : name, 'distance' : distance})
 	new_star = star.find_one({'_id': star_id })
 	output = {'name' : new_star['name'], 'distance' : new_star['distance']}
 	return jsonify ({'result' : output})

@app.route('/star/delete/<name>', methods=['GET'])
def delete_one_star(name):
  star = mongo.db.stars
  s = star.remove({'name': name})
  print( 'successfully deleted')
  return 'deleted' 

@app.route('/star/update', methods=['POST'])
def update():
 	star = mongo.db.stars
 	name = request.json['name']
 	distance = request.json['distance']
 	s = star.update({'name': name}, {'$set':{'distance':distance}})
 	print('records successfully updated')
 	return name


if __name__ == '__main__':
 	 app.run(debug=True, port=8080)