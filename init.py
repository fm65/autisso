from flask import Flask, render_template

app = Flask(_name_)

@app.route('/')
def home():
	return "<h1>Hello World</h1>"
	#return render_template("index.html")
