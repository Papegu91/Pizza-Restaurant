#app/main.py

from flask import Flask
from .models import db  
from flask import jsonify, request

from .models import Restaurant, Pizza, RestaurantPizza


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'

@app.route('/')
def index():
    data = jsonify({"message":"Welcome to pizzaaaa......"})
    return data

#  data
test_data = [
    {
        "id": 1,
        "name": "Dominion Pizza",
        "address": "Good Italian, Ngong Road, 5th Avenue"
    },
    {
        "id": 2,
        "name": "Pizza Hut",
        "address": "Westgate Mall, Mwanzi Road, Nrb 100"
    }
]

@app.route('/restaurants', methods=['GET'])
def get_restaurant():
    restaurants = Restaurant.query.all()
    rest = []

    for restaurant in restaurants:
        rest.append(restaurant.as_dict())

    # Append the dummy data to the rest list
    rest.extend(test_data)
    return jsonify({"Restraunts": rest})

@app.route('/add_restaurants', methods=['POST'])
def add_restaurant():
    try:
        data = request.get_json()
        new_restaurant = Restaurant(**data)
        db.session.add(new_restaurant)
        db.session.commit()
        return jsonify({'message': 'Restaurant added successfully'}), 201
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': str(error)}), 500



@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant_by_id(id):
    # Retrieve the restaurant by ID from the database
    restaurant = Restaurant.query.get(id)

    if restaurant is not None:
        # If the restaurant exists, convert it to a dictionary
        restaurant_data = restaurant.as_dict()

        # Retrieve pizzas associated with the restaurant
        restaurant_data['pizzas'] = [
            pizza.as_dict() for pizza in Pizza.query.filter_by(restaurant_id=id)
        ]

        return jsonify(restaurant_data)
    else:
        # If} the restaurant does not exist, return an error message
        return jsonify({"error": "Restaurant not found"}), 404
    

@app.route('/pizzas', methods=['GET'])
def get_pizza():
    pizzas = Pizza.query.all()
    pizza_list = []

    for pizza in pizzas:
        pizza_list.append(pizza.as_dict())
    
    return jsonify({"Pizzas": pizza_list})



@app.route('/add_pizza', methods=['POST'])
def add_pizza():
    data = request.get_json()

    new_pizza = Pizza(**data)

    db.session.add(new_pizza)

    db.session.commit()

    return jsonify({'Pizza': 'Add Successfully'}), 201



@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()

    # Validate the input data
    if 'price' not in data or 'pizza_id' not in data or 'restaurant_id' not in data:
        return jsonify({'errors': ['validation errors']}), 400

    # Check if the Pizza and Restaurant exist
    pizza = Pizza.query.get(data['pizza_id'])
    restaurant = Restaurant.query.get(data['restaurant_id'])

    if pizza is None or restaurant is None:
        return jsonify({'errors': ['Pizza or Restaurant not found']}), 404

    # Create a new RestaurantPizza object
    new_pizza_order = RestaurantPizza(
        price=data['price'],
        pizza=pizza,
        restaurant=restaurant
    )

    db.session.add(new_pizza_order)
    db.session.commit()

    return jsonify({'message': 'RestaurantPizza created successfully'}), 201


if __name__ == '__main__':
    app.run(port=5000, debug=True)