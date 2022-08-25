from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_app.models import chore

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    schema_name = 'chore_tracker_schema'

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.chores = []
    
    @staticmethod
    def form_validate(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.schema_name).query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken!", 'register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!", 'register')
            is_valid = False
        if len(user['first_name']) < 3:
            flash("First Name must be at least 3 characters", 'register')
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last Name must be at least 2 characters", 'register')
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters long", 'register')
            is_valid = False
        if (user['password']) != (user['password_match']):
            flash("Passwords do not match!", 'register')
            is_valid = False
        return is_valid

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL(cls.schema_name).query_db(query,data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.schema_name).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.schema_name).query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_all_chores_from_logged_in_user(cls, data):
        query = "SELECT * FROM users JOIN chores ON users.id = chores.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.schema_name).query_db(query, data)
        if len(results) < 1:
            return None
        else:
            this_user = cls(results[0])
            for this_chore in results:
                chore_data = {
                    "id": this_chore['chores.id'],
                    "chores": this_chore['chores'],
                    "requirements": this_chore['requirements'],
                    "user_id": this_chore['user_id'],
                    "created_at": this_chore['chores.created_at'],
                    "updated_at": this_chore['chores.updated_at']
                }
                this_chore_instance = chore.Chore(chore_data)
                this_user.chores.append(this_chore_instance)
            return this_user