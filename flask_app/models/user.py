from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import painting
from flask import flash
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

# Creates a user AND hashes the password, everytime we want to update a class atribute, we need to recreate the dictionary. Here we are modifying password.
    @classmethod
    def create(cls, data):
        hash = bcrypt.generate_password_hash(data["password"])
        hashed_dict = {
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "email": data["email"],
            "password": hash,
        }
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL("paintings_schema").query_db(query, hashed_dict)

# Selects each user specifically by email
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("paintings_schema").query_db(query, data)
        if result:
            return cls(result[0])
        
# Select each  user by just ID, info that I need to store in SESSION and deploy any specific data from the user in the welcome page.
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL("paintings_schema").query_db(query, data)
        if result:
            return cls(result[0])
        

# This staticmethod validates if my users database already has the writen email and password stored. user = User.get_by_email(data)
    @staticmethod
    def login_validator(data):
        user = User.get_by_email(data)
        if not user:
            return False
        if not bcrypt.check_password_hash(user.password, data["password"]):
            return False
        return True

# This staticmethod handles all the validations from my Register Form, also in line 68 to 71, user = User.get_by_email(data) basically checks if again, the email from the database already exists and checks for duplicates.
    @staticmethod
    def registry_validator(data):
        is_valid = True
        if len(data["first_name"]) <= 2:
            flash("Please insert your First Name.")
            is_valid = False
        if len(data["last_name"]) <= 2:
            flash("Please insert your Last Name.")
            is_valid = False
        user = User.get_by_email(data)
        if user:
            flash("Email is already in use.")
            is_valid = False
        if len(data["email"]) <= 1:
            flash("Please insert your Email.")
            is_valid = False
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!")
            is_valid = False
        if len(data["password"]) <= 8:
            flash("Password must be 8 characters or more.")
            is_valid = False
        if data["password"] != data["confirm_password"]:
            flash("Your password must match")
            is_valid = False
        return is_valid
