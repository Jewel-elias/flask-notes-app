from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Note
from flask import flash
import json
from markupsafe import escape

# Blueprint is used to organize routes
# This file can be expanded with route definitions later
views = Blueprint('views', __name__)

# define our first view
@views.route('/', methods=['GET', 'POST'])
# This function will run whenever we go to the / route
# can't access this route unless we are logged in
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    # when we use get, it access the primary key
    # and it will return None if the note doesn't exist
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            
    return jsonify({})

@views.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'