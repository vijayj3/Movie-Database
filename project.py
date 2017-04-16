from flask import Flask, render_template, request,redirect,url_for,jsonify
app = Flask(__name__)

from movie import MovieAPI

def loadMovies(example) :
	movieapi = MovieAPI(example)
	return movieapi.parser()

#Movie Routing Methods

@app.route('/')
@app.route('/movie/',methods = ['GET','POST'])
def mainPage():
	if request.method == 'POST':
		phrase = request.form['name']
		results = loadMovies(phrase)
		return render_template("moviemaintwo.html",results = results)
	else:
		return render_template("moviemain.html")


#Main Method
if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0',port = 5000)
