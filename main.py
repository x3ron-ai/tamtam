from flask import Flask, render_template, Response, request
import subprocess
import json
import find_quote

app = Flask(__name__)

@app.route('/getfiles')
def getFiles():
	return json.dumps(find_quote.find_files('xacaton/'))

@app.route('/')
def index():
	return render_template('main.html')

@app.route('/quotas')
def find_qq():
	return render_template('quotas.html')

@app.route('/blacklist')
def find_bb():
	return render_template('blacklist.html')

@app.route('/getData')
def getData():
	file_name = request.args.get('file')
	return find_quote.process_json_file(file_name)

@app.route('/getBlackList')
def getBlackList():
	subprocess.run(["python", 'find_blackurl.py'])
	return json.dumps({'text':open('resulttest.txt', 'r', encoding='utf-8').read()})

if __name__ == '__main__':
	app.run(debug=True)