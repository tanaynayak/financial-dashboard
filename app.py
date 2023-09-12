from flask import Flask, render_template
from bokeh.client import pull_session
from bokeh.embed import server_session

app = Flask(__name__)

@app.route('/', methods=['GET'])
def bkapp_page():
    with pull_session(url="http://localhost:5006/bkapp") as session:
        script = server_session(session_id=session.id, url='http://localhost:5006/bkapp')
        return render_template("embed.html", script=script, template="Flask")

if __name__ == '__main__':
    app.run(port=8080)
