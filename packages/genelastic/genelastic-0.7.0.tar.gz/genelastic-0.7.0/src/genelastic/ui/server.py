import requests
from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object("src.genelastic.ui.settings.Config")


@app.route("/")
def home() -> str:
    api_url = app.config["GENUI_API_URL"]
    try:
        version_reponse = requests.get(f"{api_url}version", timeout=20)
        version = version_reponse.json().get("version")
        wet_processes_reponse = requests.get(
            f"{api_url}wet_processes", timeout=20
        )
        wet_processes = wet_processes_reponse.json()
        bi_processes_reponse = requests.get(
            f"{api_url}bi_processes", timeout=20
        )
        bi_processes = bi_processes_reponse.json()
        analyses_reponse = requests.get(f"{api_url}analyses", timeout=20)
        analyses = analyses_reponse.json()
    except requests.exceptions.RequestException:
        version = "API not reachable"
        wet_processes = []
        bi_processes = []
        analyses = []
    return render_template(
        "home.html",
        version=version,
        wet_processes=wet_processes,
        bi_processes=bi_processes,
        analyses=analyses,
    )


@app.route("/analyses")
def show_analyses() -> str:
    api_url = app.config["GENUI_API_URL"]
    try:
        analyses_reponse = requests.get(f"{api_url}analyses", timeout=20)
        analyses = analyses_reponse.json()
    except requests.exceptions.RequestException:
        analyses = ["Error fetching data."]

    return render_template("analyses.html", analyses=analyses)


@app.route("/bi_processes")
def show_bi_processes() -> str:
    api_url = app.config["GENUI_API_URL"]
    try:
        bi_processes_reponse = requests.get(
            f"{api_url}bi_processes", timeout=20
        )
        bi_processes = bi_processes_reponse.json()
    except requests.exceptions.RequestException:
        bi_processes = ["Error fetching data."]

    return render_template("bi_processes.html", bi_processes=bi_processes)


@app.route("/wet_processes")
def show_wet_processes() -> str:
    api_url = app.config["GENUI_API_URL"]
    try:
        wet_processes_reponse = requests.get(
            f"{api_url}wet_processes", timeout=20
        )
        wet_processes = wet_processes_reponse.json()
    except requests.exceptions.RequestException:
        wet_processes = ["Error fetching data."]

    return render_template("wet_processes.html", wet_processes=wet_processes)


@app.route("/version")
def show_version() -> str:
    api_url = app.config["GENUI_API_URL"]
    try:
        version_reponse = requests.get(f"{api_url}version", timeout=20)
        version = version_reponse.json().get("version", "Version not found")
    except requests.exceptions.RequestException:
        version = "Error fetching version."

    return render_template("version.html", version=version)
