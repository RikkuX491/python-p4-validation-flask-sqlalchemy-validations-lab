import ipdb

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 

    @validates('name')
    def validate_name(self, attr, value):
        author_with_same_name = Author.query.filter(Author.name == value).first()
        if (value == None) or value == "":
            raise ValueError(f"Author must have a name!")
        elif author_with_same_name:
            raise ValueError(f"Author names must be unique!")
        return value
    
    @validates('phone_number')
    def validate_phone_number(self, attr, value):
        if (not (len(value) == 10)) or (not (value.isdigit())):
            raise ValueError(f"Invalid phone number!")
        else:
            return value

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('content')
    def validate_content(self, attr, value):
        if len(value) < 250:
            raise ValueError("Content is too short. Must be at least 250 characters.")
        else:
            return value
        
    @validates('summary')
    def validate_summary(self, attr, value):
        if len(value) > 250:
            raise ValueError("Summary is too long. Cannot be longer than 250 characters.")
        else:
            return value
        
    @validates('category')
    def validate_category(self, attr, value):
        if not (value in ["Fiction", "Non-Fiction"]):
            raise ValueError("Category must be either Fiction or Non-Fiction!")
        else:
            return value
        
    @validates('title')
    def validate_title(self, attr, value):
        clickbait_list = ["Won't Believe", "Secret", "Top", "Guess"]

        if not value:
            raise ValueError('Must have a title! Title cannot be empty!')
        elif not (any([c in value for c in clickbait_list])):
            raise ValueError('Not clickbaity enough!')
        else:
            return value

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
