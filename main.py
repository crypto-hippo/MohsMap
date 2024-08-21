from flask import Flask, render_template
from config import config
from jinja_vars import jinja_vars
from google.cloud import firestore
from utility import load_blueprints, setup_google_cloud_logging
import jinja2
import os

client = firestore.Client()
setup_google_cloud_logging()


def create_flask_app():
    # csrf = CSRFProtect()
    flask_app = Flask(__name__)
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)
    flask_app.secret_key = config["secret_key"]
    flask_app.debug = True
    blueprints = load_blueprints()
    for bp in blueprints:
        flask_app.register_blueprint(bp)
    return flask_app


app = create_flask_app()
app.jinja_env.globals.update(**jinja_vars)


# routes 
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/contact_us")
def contact_us():
    try:
        return render_template("contact_us.html")
    except Exception as e:
        return "Your request cannot be processed"


@app.route("/about_us")
def about_us():
    try:
        return render_template("about_us.html")
    except Exception as e:
        return "Your request cannot be processed"


@app.route("/why_acms")
def why_acms():
    try:
        return render_template("why_acms.html")
    except Exception as e:
        return "Your request cannot be processed"


@app.route("/tos")
def tos():
    try:
        return render_template("tos.html")
    except Exception as e:
        return "Your request cannot be processed"


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
