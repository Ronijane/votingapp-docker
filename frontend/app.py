from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

BACKEND_URL = "http://backend:3000"

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Voting App</title>
  <style>
    body { font-family: Arial; background:#f4f4f4; text-align:center; }
    .box { background:white; padding:20px; width:300px;
           margin:auto; margin-top:50px; border-radius:10px; }
    button { padding:10px; margin:5px; width:100%; }
  </style>
</head>
<body>
  <div class="box">
    <h2>Vote your favorite language</h2>
    <form method="post">
      <button name="candidate" value="Python">Python</button>
      <button name="candidate" value="JavaScript">JavaScript</button>
      <button name="candidate" value="Go">Go</button>
    </form>

    <h3>Results</h3>
    {% for k, v in votes.items() %}
      <p>{{k}}: {{v}}</p>
    {% endfor %}
  </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        requests.post(f"{BACKEND_URL}/vote",
                      json={"candidate": request.form["candidate"]})

    votes = requests.get(f"{BACKEND_URL}/votes").json()
    return render_template_string(HTML, votes=votes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
