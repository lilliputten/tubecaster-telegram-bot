from flask import Flask

from flask import send_from_directory


app = Flask(
    __name__,
    static_url_path="",  # "/static",
    static_folder="static",
    # template_folder="web/templates", # TODO?
)


@app.route("/")
def home():
    #  return app.send_static_file("project-info.txt")
    return "Site index!"


@app.route("/about")
def about():
    return "About route"


@app.route("/project-info")
def static_file():
    print("project-info")
    return app.send_static_file("project-info.txt")
