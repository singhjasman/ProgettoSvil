
from flask import Flask, render_template, url_for

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static"
)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/test-css")
def test_css():
    return f"""
    <h1 style="color: green;">Flask funziona!</h1>
    <p>Indirizzo CSS: {url_for('static', filename='css/style.css')}</p>
    <link rel="stylesheet" href="{url_for('static', filename='css/style.css')}">
    """

if __name__ == "__main__":
    app.run(debug=True, port=5000)
