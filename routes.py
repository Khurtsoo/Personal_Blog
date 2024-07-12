from flask import Flask, render_template, request,  redirect, flash, send_from_directory
from extensions import app, db
from forms import AddBlog, AddComment, RegisterForm, LoginForm
import os
from models import BlogModel, Comments, User
from flask_login import logout_user, login_user, login_required, current_user
from datetime import datetime


@app.route('/')
def home():
    blogs = BlogModel.query.all();
    return render_template('index.html', data = blogs)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You successgfully registered", category="success")
        redirect("/login")
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        exists = User.query.filter(User.username==form.username.data).first()
        print(exists)
        if exists and exists.password == form.password.data:
            login_user(exists)
            flash("You successfully logged in", category="success")
            return redirect("/")

    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

@app.route('/blog/<int:id>', methods=["GET", "POST"])
def blog(id):
    form = AddComment()
    if form.validate_on_submit():
        obj = Comments(
            comment = form.comment.data, 
            user = current_user.username,
            blog_id = id, 
            date = datetime.now()
        )
        db.session.add(obj)
        db.session.commit()
        flash("You successfully added the comment", category="success")
    current = BlogModel.query.get(id)
    comments = Comments.query.filter_by(blog_id = id).all()
    print(comments)
    return render_template("details.html", blog=current, form= form, comments = comments)


@app.route("/addblog", methods=["GET", "POST"])
@login_required
def add_blog():
    if current_user.role == "admin":
        form = AddBlog()
        if form.validate_on_submit():
            file = request.files['file']
            if file:
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
                obj = BlogModel(name=form.name.data,
                            file=filename,
                            description = form.description.data)
                db.session.add(obj)
                db.session.commit()
                flash("You successfully added the product", category="success")
            
            return redirect("/")
        
        if form.errors:
            print(form.errors)
            for error in form.errors:
                print(error)

            flash("You didn't add the product properly", category="danger")
            

        return render_template("addblog.html", form=form)
    else:
        return "You are not permitted to this action!", 401

@app.route("/deleteBlog/<int:id>")
@login_required
def delete_blog(id):
    if current_user.role == "admin":
        current = BlogModel.query.get(id)
        print(current)
        db.session.delete(current)
        db.session.commit()
        return redirect("/")
    else:
        return "You are not permitted to this action!", 401
    
@app.route("/deleteComment/<int:id>")
@login_required
def delete_comment(id):
    if current_user.role == "admin":
        current = Comments.query.get(id)
        print(current)
        db.session.delete(current)
        db.session.commit()
        return redirect("/")
    else:
        return "You are not permitted to this action!", 401

@app.route("/editBlog/<int:id>", methods=["GET", "POST"])
@login_required
def edit_product(id):
    if current_user.role == "admin":

        current = BlogModel.query.get(id)
        print(current)
        form = AddBlog(
            name=current.name,
            description=current.description,
        )
        if form.validate_on_submit():
            file = request.files['file']
            if file:
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else: 
                filename = current.file
            current.name = form.name.data
            print("name", current.name)
            current.file = filename
            current.description = form.description.data

            db.session.commit()
            flash("You successfully added the product", category="success")
            
            return redirect("/")
        
        if form.errors:
            print(form.errors)
            for error in form.errors:
                print(error)

            flash("You didn't add the product properly", category="danger")
        return render_template("addblog.html", form=form)
    else:
        return "You are not permitted to this action!", 401
    