from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import user
from flask import flash
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class Painting:
    def __init__(self,data):
        self.id = data["id"]
        self.user_id = data["user_id"] # We add user_id session in order to display edit page
        self.title = data["title"]
        self.description = data["description"]
        self.price = data["price"]        
        self.created_at = data["created_at"]        
        self.updated_at = data["updated_at"]       
        
# Function made in order to display all paintings in welcome page, specifically in line 22 of user controller.
    @classmethod
    def get_all_paintings(cls):
        query = "SELECT * FROM paintings JOIN users ON paintings.user_id = users.id;"
        results = connectToMySQL('paintings_schema').query_db(query)
        paintings = []
        if results:
            for row in results:
                temp_var = (cls(row))
                data = {
                    "id": row["users.id"],
                    "first_name": row["first_name"],
                    "last_name": row["last_name"],
                    "email": row["email"],
                    "password": row["password"],
                    "created_at": row["users.created_at"],
                    "updated_at": row["users.updated_at"]
                }
                temp_var.creator = user.User(data)
                paintings.append(temp_var)
        return paintings 
    
# Creates a painting and assignes it to the creator with USER_ID.
    @classmethod
    def create_painting(cls, data):
        query = "INSERT INTO paintings (user_id, title, description, price, created_at, updated_at) VALUES ( %(user_id)s, %(title)s, %(description)s,%(price)s, NOW(), NOW());"
        result = connectToMySQL('paintings_schema').query_db(query, data)
        return result
    
# Updates a painting.
    @classmethod
    def update_painting(cls, data):
        query = "UPDATE paintings SET title = %(title)s, description = %(description)s, price = %(price)s, updated_at = NOW() WHERE id = %(id)s;"
        connectToMySQL("paintings_schema").query_db(query, data)
        
# Deletes a painting.
    @classmethod
    def delete_painting(cls, data):
        query = "DELETE FROM paintings WHERE id = %(id)s;"
        connectToMySQL("paintings_schema").query_db(query, data)
       
# Gets the specific painting with id 
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM paintings JOIN users ON paintings.user_id = users.id WHERE paintings.id = %(id)s;"
        results = connectToMySQL("paintings_schema").query_db(query, data)
        if results:
            paintings = cls(results[0])
            paintings.creator = user.User(results[0])
            return paintings

# Try to do GET_ONE with this function instead.
    # @classmethod
    # def get_one(cls, data):
    #     query = "SELECT * FROM paintings JOIN users ON paintings.user_id = users.id WHERE paintings.id = %(id)s;"
    #     results = connectToMySQL("paintings_schema").query_db(query, data)
    #     paintings = []
    #     if results:
    #         for row in results:
    #             temp = (cls(row))
    #             data = {
    #                 "id": row["users.id"],
    #                 "first_name": row["first_name"],
    #                 "last_name": row["last_name"],
    #                 "email": row["email"],
    #                 "password": row["password"],
    #                 "created_at": row["users.created_at"],
    #                 "updated_at": row["users.updated_at"]
    #             }
    #             temp.creator = user.User(row)
    #             paintings.append = (temp)
    #     return paintings

        
        
# Validates data from the paintings section.
    @staticmethod
    def paint_validator(data):
        is_valid = True
        if len(data["title"]) <= 3:
            flash("Title must be at least 2 characters")
            is_valid = False
        if len(data["description"]) <= 3:
            flash("Description must be at least 10 characters")
            is_valid = False
        if len(data["price"]) <= 1:
            flash("Price must be higher than $1.00")
            is_valid = False
        return is_valid

        
        
        
        

