import datetime as dt
import sqlalchemy as sa
import sqlalchemy.orm as orm
import passlib.hash as ph
import sqlalchemy.ext.declarative as dec
import json

Base = dec.declarative_base()
metadata = Base.metadata

class User(Base):
    __tablename__ = 'users'
    id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.String(50), nullable=False, unique=True)
    hashed_password = sa.Column(sa.String(100), nullable=False)
    teacher = sa.Column(sa.Boolean, default=False)
    is_active = sa.Column(sa.Boolean, default=False)
    profile = orm.relationship('Profile', back_populates='user')
    chats = orm.relationship("Chats", back_populates="user")
    
    def verify_password(self, password):
        return ph.bcrypt.verify(password, self.hashed_password)
    
    def set_password(self, password):
        self.hashed_password = ph.bcrypt.hash(password)
        
    def user_activate(self):
        self.is_active = True
        
    def __repr__(self):
        return f'User: {self.first_name} {self.last_name}; Email: {self.email}'
    
    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.email}'

    
    
class Profile(Base):
    __tablename__ = 'profiles'
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    user = orm.relationship('User', back_populates='profile')
    first_name = sa.Column(sa.String(50), nullable=True)
    last_name = sa.Column(sa.String(50), nullable=True)
    bio = sa.Column(sa.String(1000), nullable=True)
    location = sa.Column(sa.String(100), nullable=True)
    birth_date = sa.Column(sa.Date, nullable=True)
    created_at = sa.Column(sa.DateTime, default=dt.datetime.now)
    updated_at = sa.Column(sa.DateTime, default=dt.datetime.now, onupdate=dt.datetime.now)
    profile_image = sa.Column(sa.String(100), nullable=True)
    
    def __repr__(self):
        return f'Profile: {self.user.first_name} {self.user.last_name}; Bio: {self.bio}'
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} {self.bio}'
    
    

class Chats(Base):
    __tablename__ = "chats"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    prompt = sa.Column(sa.JSON)
    generated_response = sa.Column(sa.JSON)
    created_at = sa.Column(sa.String, server_default=sa.sql.func.now())
    tokens_used = sa.Column(sa.Integer, default=0, nullable=True)
    response_rating = sa.Column(sa.Integer, default=0, nullable=True)
    alt_response = sa.Column(sa.String, nullable=True)

    user = orm.relationship("User", back_populates="chats")
    
    def set_prompt(self, prompt):
        self.prompt = json.dumps(prompt)
        
    def get_prompt(self):
        return json.loads(self.prompt) if self.prompt else []
    
    def set_generated_response(self, generated_response):
        self.generated_response = json.dumps(generated_response)
        
    def get_generated_response(self):
        return json.loads(self.generated_response) if self.generated_response else []
    
    def count_tokens(self):
        self.tokens_used = (len(self.prompt) + len(self.generated_response))/4
        
    def get_tokens_used(self):
        return self.tokens_used
    
