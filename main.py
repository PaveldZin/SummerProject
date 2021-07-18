from flask import Flask, render_template, request, redirect, url_for

import SearchApiHandler

app = Flask(__name__)
anime_finder = SearchApiHandler.AnimeFinder()


@app.route("/")
def start_screen():
    return redirect(url_for('form'))


@app.route("/form")
def form():
    return render_template("form.html")


@app.route("/data", methods=["POST", "GET"])
def data():
    if request.method == "GET":
        return (
            f"The URL /data is accessed directly. Try going to '/form' to submit form"
        )
    if request.method == "POST":
        if not request.files["image"] and not request.form["url"]:
            return (
                f"Fields are empty"
            )
        try:
            if request.files["image"]:
                anilist_data = anime_finder(request.files["image"], 'image')
            else:
                anilist_data = anime_finder(request.form["url"], 'url')
            return render_template("data.html", form_data=anilist_data)
        except SearchApiHandler.BadRequest:
            return (
                f"One of the servers is not responding correctly. Make sure url/image is correct and try again"
            )
        except SearchApiHandler.NotFound:
            return (
                f"Could not find anime source. Make sure you chose right image or try better quality screenshot"
            )
        except SearchApiHandler.InvalidURL:
            return (
                f"Could not find image"
            )


if __name__ == "__main__":
    # Launch the Flask dev server
    app.run(host="localhost", port=5000)
