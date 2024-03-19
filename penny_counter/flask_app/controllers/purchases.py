from flask_app import app
from flask_app.models.purchase import Purchase
from flask import redirect, request, render_template, flash
from flask_app.controllers import months


@app.route("/purchase/create", methods=["POST"])
def create_purchase():
    # want to make it so that an empty form can't be submitted or any days that
    # arent <=0 for days
    # if request.form == None:
    #     flash("Can't be blank", "purchase")
    #     return redirect(request.referrer)
    # if len(request.form) > 1:
    #     flash("Can't be blank", "purchase")
    if request.form['purchase_date'] < "1":
        flash("Form can't be empty or days cant be negative/zero", "purchase")
        return redirect(request.referrer)
    else:
        Purchase.save_purchase(request.form)
    return redirect(request.referrer)

@app.route("/delete/<int:id>")
def delete_purchase(id):
    data = {
        "id": id
    }
    Purchase.delete_purchase(data)
    return redirect(request.referrer)

@app.route('/edit/<int:purchase_id>/<int:month_id>')
def edit_purchase(purchase_id, month_id):
    month = month_id
    data = {
        "purchase_id": purchase_id
    }
    purchase = Purchase.get_by_id(data)
    return render_template("purchase.html", purchase = purchase, month = month)

@app.route("/update/<int:purchase_id>/<int:month_id>", methods=["POST"])
def updated_purchase(purchase_id, month_id):
    if int(request.form["purchase_date"]) < 1:
        flash("Negative or a zeroth day?", "purchase")
        return redirect(f"/edit/{purchase_id}/{month_id}")
    else:
        data = {
            "purchase_id": purchase_id,
            "purchase_date": request.form["purchase_date"],
            "description": request.form["description"],
            "price": request.form["price"]
        }
        Purchase.update(data);
    return redirect(f"/month/{month_id}")