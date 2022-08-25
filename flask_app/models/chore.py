from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user

class Chore:
    schema_name = 'chore_tracker_schema'

    def __init__(self, data):
        self.id = data['id']
        self.chores = data['chores']
        self.requirements = data['requirements']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None
    
    @staticmethod
    def validate_chore(chore):
        is_valid = True
        if len(chore['chores']) < 3:
            flash("Chore is required!")
            is_valid = False
        if len(chore['requirements']) < 3:
            flash("Requirements must be at least 3 characters!")
            is_valid = False
        return is_valid

    @classmethod
    def update(cls, data):
        query = "UPDATE chores SET chores = %(chores)s, requirements = %(requirements)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.schema_name).query_db(query, data)
    
    @classmethod
    def delete_chore(cls, data):
        query = "DELETE FROM chores WHERE id = %(id)s;"
        return connectToMySQL(cls.schema_name).query_db(query, data)

    @classmethod
    def save_chore(cls, data):
        query = "INSERT INTO chores (chores, requirements, user_id) VALUES (%(chores)s, %(requirements)s, %(user_id)s);"
        return connectToMySQL(cls.schema_name).query_db(query, data)

    @classmethod
    def get_one_chore(cls, data):
        query = "SELECT * FROM chores WHERE id = %(id)s;"
        results = connectToMySQL(cls.schema_name).query_db(query, data)
        return cls( results[0] )

    @classmethod
    def get_all_chores_with_one_user(cls, data):
        query = "SELECT * FROM chores LEFT JOIN users ON users.id = chores.user_id WHERE chores.id = %(id)s;"
        results = connectToMySQL(cls.schema_name).query_db(query, data)
        print(results)
        one_chore = cls(results[0])
        user_data = {
            "id": results[0]['users.id'],
            "first_name": results[0]['first_name'],
            "last_name": results[0]['last_name'],
            "email": results[0]['email'],
            "password": results[0]['password'],
            "created_at": results[0]['users.created_at'],
            "updated_at": results[0]['users.updated_at']
            }
        chore_master = user.User(user_data)
        one_chore.user = chore_master
        return one_chore