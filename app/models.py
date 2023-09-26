# app/models.py

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    address = db.Column(db.String(50), unique=True)

    # Establish a one-to-many relationship between Restaurant and RestaurantPizza
    # pizza_orders = relationship('RestaurantPizza', backref='restaurant')

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
        }

class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    ingredients = db.Column(db.String(200), nullable=False)
    created_at = db.Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(DateTime, nullable=False, default=datetime.utcnow)

    
    def as_dict(self):
        return {
            'id': self.id,
            'ingredients': self.ingredients,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    # Establish a one-to-many relationship between Pizza and RestaurantPizza
    # restaurant_pizzas = relationship('RestaurantPizza', backref='pizza')

class RestaurantPizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    created_at = db.Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(DateTime, nullable=False, default=datetime.utcnow)
    pizza_id = db.Column(db.Integer, ForeignKey('pizza.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, ForeignKey('restaurant.id'), nullable=False)

    pizza = db.relationship('Pizza', backref='restaurant_pizza', lazy=True)
    restaurant = db.relationship('Restaurant', backref='pizza_orders', lazy=True)


    def as_dict(self):
        return {
            'id': self.id,
            'price': self.price,  # Corrected to use 'price' from the model
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'pizza_id': self.pizza_id,
            'restaurant_id': self.restaurant_id,
        }