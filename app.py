from flask import Flask, render_template, redirect, request
from servo import on, off
from subprocess import call

sw = 1

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return redirect("/switch")   

@app.route("/switch", methods =["POST", "GET"])
def switch():
    global sw 
    if request.method == "POST":
        sw = sw * -1
        if sw > 0:
            on()
        else:
            off()

    return render_template("button.html")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

