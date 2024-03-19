from flask_app import app
from flask import render_template, redirect, request
from flask_app.models.month import Month
from flask_app.models.purchase import Purchase
from flask_app.controllers import users



@app.route("/month/<int:month_id>")
def single_month(month_id):
    data = {
        "id": month_id
    }
    purchases = Purchase.get_all_by_month(data)
    return render_template("month.html", month = Month.get_by_id(data), purchases = purchases)


@app.route("/month/create", methods = ["POST"])
def create_month():
    Month.save(request.form)
    return redirect("/success")

@app.route("/success")
def success():
    return redirect("/welcome")