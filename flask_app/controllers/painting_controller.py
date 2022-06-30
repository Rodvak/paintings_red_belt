from flask import Flask, render_template, request, redirect, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models.user import User
from flask_app.models.painting import Painting

#===========================DISPLAY ROUTES==========================

# Shows the create_painting html
@app.route("/paintings/new")
def new():
    if "user_id" not in session:
        return redirect ("/welcome")
    logged_in_user = User.get_by_id({"id": session["user_id"]}) # We use this in order to get user in session.
    return render_template("create_painting.html", user = logged_in_user) # 

# Shows the show_painting html
@app.route("/paintings/<int:id>")
def show_paintings(id):
    if "user_id" not in session:
        return redirect ("/welcome")
    painting = Painting.get_one({ "id": id }) # get_painting _of_user is here because it will show the method that I wrote in user.py We will be able to see each painting from each user.   
    logged_in_user = User.get_by_id({ "id": session["user_id"] })
    return render_template("show_painting.html", painting = painting, logged_in_user = logged_in_user) # user is used in html with jinja. 


# Renders the edit_painting html, BUT also checks the get_one which gets the paint by ID. Then checks if the user in session will be able to modify the painting.
@app.route('/paintings/edit/<int:id>')
def edit_band(id):
    if "user_id" not in session:
        return redirect('/welcome')
    paintings = Painting.get_one({ "id": id })
    if session["user_id"] != paintings.user_id:
        return redirect('/welcome')
    logged_in_user = User.get_by_id({ "id": session["user_id"] })
    return render_template("edit_painting.html", painting = paintings, user=logged_in_user)


#========================ACTION ROUTES==========================

# Creates the painting after validating it.
@app.route('/new/painting', methods = ["POST"])
def create_painting():
    if not Painting.paint_validator(request.form):
        return redirect("/paintings/new")
    data= {
        "user_id": session["user_id"],
        "title": request.form["title"],
        "description": request.form["description"],
        "price": request.form["price"],
        }
    Painting.create_painting(data)
    return redirect ("/welcome")

# Updates the painting after validating it.
@app.route('/update/painting', methods = ["POST"])
def update():
    if "user_id" not in session:
        return redirect('/welcome')
    if not Painting.paint_validator(request.form):
        return redirect("/welcome") #It is not redirecting to the same page.
    Painting.update_painting(request.form)
    return redirect("/welcome")


# Deletes the painting. 
@app.route('/paint/delete/<int:id>')
def delete_painting(id):
    if "user_id" not in session:
        return redirect("/welcome")    
    data = { "id": id }
    Painting.delete_painting(data)
    return redirect("/welcome")

