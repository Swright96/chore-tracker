from flask import render_template, redirect, session, request
from flask_app import app
from flask_app.models.user import User
from flask_app.models.chore import Chore

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    return render_template("dashboard.html", user = User.get_by_id(data), this_user = User.get_all_chores_from_logged_in_user(data))

@app.route('/chore/new')
def new_chore():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    return render_template('createChore.html', user = User.get_by_id(data))

@app.route('/chore/create', methods = ['POST'])
def create_chore():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Chore.validate_chore(request.form):
        return redirect('/chore/new')
    data = {
        'chores' : request.form['chores'],
        'requirements' : request.form['requirements'],
        'user_id': session['user_id']
    }
    Chore.save_chore(data)
    return redirect('/dashboard')

@app.route('/chore/<int:id>')
def show_chore(id):
    if 'user_id' not in session:
        return redirect('/logout')
    chore_data = {
        "id": id
    }
    user_data = {
        "id": session['user_id']
    }
    return render_template("choreDetails.html", chores = Chore.get_all_chores_with_one_user(chore_data), user = User.get_by_id(user_data))

@app.route('/chore/edit/<int:id>')
def edit_chore(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "id": session['user_id']
    }
    return render_template("updateChore.html", chore = Chore.get_one_chore(data), user = User.get_by_id(user_data))

@app.route('/chore/update/<int:id>', methods = ['POST'])
def chore_update(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Chore.validate_chore(request.form):
        return redirect(f'/chore/edit/{id}')
    data = {
        'chores' : request.form['chores'],
        'requirements' : request.form['requirements'],
        'user_id': session['user_id'],
        "id": id
    }
    Chore.update(data)
    return redirect('/dashboard')

@app.route('/chore/delete/<int:id>')
def chore_delete(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Chore.delete_chore(data)
    return redirect('/dashboard')