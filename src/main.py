from flask import Flask, request, render_template
app = Flask(__name__)


@app.route("/login", methods=['get', 'post'])
def login():
	print request.method
	if request.method == "GET":
		return render_template("login.html")
	elif request.method == "POST":
		for key, arg in request.values.iteritems():
			print key, arg
		return ""

app.run('0.0.0.0', debug=True)