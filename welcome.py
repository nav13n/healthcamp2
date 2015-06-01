import os
from flask import Flask, render_template, send_from_directory, request, jsonify
from csvcollection import CSVCollection

app = Flask(__name__, static_url_path='/static/')
collection = CSVCollection("factors.csv")


@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


@app.route('/')
def Welcome():
	return render_template('index.html')
	
	
@app.route('/run_model', methods=['POST'])
def run_model():
	values = []
	print "request.form", request.form
	for i in range(len(request.form)):
		form_var = "var%s" % (i)
		try:
			values.append(float(request.form[form_var])) 
		except:
			values.append(0)
	return jsonify(index = calculate(values))

def calculate(array):
	sum = 77.076590
	coefficients = [float(r[2]) for r in collection.data]
	for i in range(len(array)):
		if not array[i] is None:
			sum = sum + array[i] * coefficients[i]
	return sum

@app.route('/load')
def load():
	global collection
	import csv
	districts = []
	with open("data.csv", "r") as f:
		i = 0
		for row in csv.reader(f, delimiter=','):
			if i > 0:
				district = {}
				district["name"] = row[0]
				district["features"] = [float(n) for n in row[1:]] 
				district["mortality_index"] = calculate(district["features"]);
				districts.append(district);
			i = i + 1
	return jsonify(districts = districts, factors = collection.data)


@app.route('/myapp')
def WelcomeToMyapp():
    return 'Welcome again to my app running on Bluemix!'
    
    
port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port), debug = True)