from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates, relationship
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(64))
    profile_picture = db.Column(db.String(128))

    def __init__(self, username, email, password, profile_picture):
        self.username = username
        self.email = email
        self.password = password
        self.profile_picture = profile_picture

    def __repr__(self):
        return f'<User {self.username}>'

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chat_room_id = db.Column(db.Integer, db.ForeignKey('chat_room.id'), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

    sender = db.relationship('User', backref=db.backref('messages', lazy=True))
    chat_room = db.relationship('ChatRoom', backref=db.backref('messages', lazy=True))

    def __repr__(self):
        return f'<Message {self.id}>'

class ChatRoom(db.Model):
    __tablename__ = 'chat_rooms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    users = relationship('User', secondary='user_chat_rooms', back_populates='chat_rooms')

class UserChatRoom(db.Model):
    __tablename__ = 'user_chat_rooms'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    chatroom_id = db.Column(db.Integer, db.ForeignKey('chat_rooms.id'), primary_key=True)
