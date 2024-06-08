from .db import db, environment, SCHEMA, add_prefix_for_prod
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Image(db.Model):
    __tablename__ = 'images'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    type_id = db.Column(db.Integer, nullable=False)
    img_url = db.Column(db.String(250), nullable=False, default='')

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "image"
    }

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'type_id': self.type_id,
            'img_url': self.img_url
        }


class User(Image, UserMixin):
    __tablename__ = 'users'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, db.ForeignKey('images.id'), primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)

    servers = db.relationship("Server", backref="user_owner", cascade='all, delete-orphan', foreign_keys="[Server.owner_id]")
    messages = db.relationship("Message", backref="user_messages", cascade='all, delete-orphan', foreign_keys="[Message.user_id]")
    reactions = db.relationship("Reaction", backref="user_reactions", cascade='all, delete-orphan', foreign_keys="[Reaction.user_id]")

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "inherit_condition": id == Image.id
    }

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'servers': [server.to_dict() for server in self.servers],
            'messages': [message.to_dict() for message in self.messages]
        }


class Server(Image):
    __tablename__ = "servers"

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, db.ForeignKey('images.id'), primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    DM = db.Column(db.Boolean, nullable=False, default=False)
    owner_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)

    channels = db.relationship('Channel', backref='server_channels', cascade='all, delete-orphan')

    __mapper_args__ = {
        "polymorphic_identity": "server",
        "inherit_condition": id == Image.id
    }

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'DM': self.DM,
            'owner_id': self.owner_id,
            'channels': [channel.to_dict() for channel in self.channels]
        }


class Channel(db.Model):
    __tablename__ = "channels"

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('servers.id')), nullable=False)
    name = db.Column(db.String(50), nullable=False, unique=True)

    messages = db.relationship("Message", backref='channel_messages', cascade='all, delete-orphan', foreign_keys="[Message.channel_id]")

    def to_dict(self):
        return {
            'id': self.id,
            'server_id': self.server_id,
            'name': self.name,
            'messages': [message.to_dict() for message in self.messages]
        }


class Message(Image):
    __tablename__ = "messages"

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, db.ForeignKey('images.id'), primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('channels.id')), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    text = db.Column(db.String(250), nullable=False)

    reactions = db.relationship("Reaction", backref='message_reactions', cascade='all, delete-orphan', foreign_keys="[Reaction.message_id]")

    __mapper_args__ = {
        "polymorphic_identity": "message",
        "inherit_condition": id == Image.id
    }

    def to_dict(self):
        return {
            'id': self.id,
            'channel_id': self.channel_id,
            'user_id': self.user_id,
            'text': self.text,
            'reactions': [reaction.to_dict() for reaction in self.reactions]
        }


class Reaction(db.Model):
    __tablename__ = 'reactions'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('messages.id')), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    type = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'message_id': self.message_id,
            'user_id': self.user_id,
            'type': self.type
        }
