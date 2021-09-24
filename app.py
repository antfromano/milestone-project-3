import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_complete_slices")
def get_complete_slices():
    complete_slices = list(mongo.db.complete_slices.find().sort("restaurant", 1))
    return render_template("library.html", complete_slices=complete_slices)


@app.route("/library", methods=["GET", "POST"])
def library():
    return render_template("library.html")


@app.route("/add_slice", methods=["GET", "POST"])
def add_slice():
    if request.method == "POST":
        slice = {
            "style": request.form.get("style"),
            "sauce": request.form.get("sauce"),
            "topping": request.form.get("topping"),
            "restaurant": request.form.get("restaurant"),
        }
        mongo.db.complete_slices.insert_one(slice)
        flash("Slice made")
        return redirect(url_for("get_complete_slices"))

    styles = mongo.db.styles.find().sort("style_name", 1)
    return render_template("add_slice.html", styles=styles)

@app.route("/delete_slice/<complete_slices_id>")
def delete_slice(complete_slices_id):
    mongo.db.complete_slices.remove({"_id": ObjectId(complete_slices_id)})
    flash("Slice deleted")
    return redirect(url_for("get_complete_slices"))


@app.route("/update_slice/<complete_slices_id>", methods=["GET", "POST"])
def update_slice(complete_slices_id):
        if request.method == "POST":
            submit = {
                "complete_slices": request.form.get("complete_slices")
            }
            mongo.db.complete_slices.update({"_id": ObjectId(complete_slices_id)}, submit)
            flash("Slice updated")
            return redirect(url_for("get_complete_slices"))

        complete_slices = mongo.db.complete_slices.find_one({"_id": ObjectId(complete_slices_id)})
        return render_template("update_slice.html", complete_slices=complete_slices)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
    port=int(os.environ.get("PORT")),
    debug=True)