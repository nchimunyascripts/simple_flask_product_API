# Flask RESTful API with SQLAlchemy

This project demonstrates how to build a RESTful API using Flask and SQLAlchemy. The API supports basic CRUD (Create, Read, Update, Delete) operations for managing items.

## Prerequisites

- Python 3.x
- pip (Python package installer)

## Project Setup

### Step 1: Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/your-username/flask-restful-api.git
cd flask-restful-api
```

### Step 2: Set Up the Virtual Environment

Create and activate a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Step 3: Install Dependencies

#### Option 1: Install Manually

Install the necessary Python packages manually:

```bash
pip install Flask Flask-SQLAlchemy
```

#### Option 2: Install from `requirements.txt`

Alternatively, you can install all dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file should look like this:

```
Flask==2.1.1
Flask-SQLAlchemy==2.5.1
```

### Step 4: Project Structure

The project is structured as follows:

```
flask_api/
│
├── app.py           # Main application file
├── models.py        # Database models
├── config.py        # Configuration settings
└── requirements.txt # List of dependencies
```

### Step 5: Configuration

The `config.py` file contains the configuration settings for the project, including the secret key and database URI.

```python
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### Step 6: Define the Models

The `models.py` file defines the database models used in the project:

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
```

### Step 7: Application Setup

The main application logic is in `app.py`, where the routes and CRUD operations are defined:

```python
from flask import Flask, request, jsonify, abort
from config import Config
from models import db, Item

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items]), 200

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get_or_404(item_id)
    return jsonify(item.to_dict()), 200

@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    if not data or not 'name' in data:
        abort(400, description="Name is required")
    item = Item(name=data['name'], description=data.get('description'))
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    data = request.get_json()
    if not data or not 'name' in data:
        abort(400, description="Name is required")
    item.name = data['name']
    item.description = data.get('description')
    db.session.commit()
    return jsonify(item.to_dict()), 200

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

### Step 8: Run the Application

To start the Flask application, run:

```bash
python app.py
```

### API Endpoints

- **GET /items**: Retrieve all items
- **GET /items/<item_id>**: Retrieve a single item by ID
- **POST /items**: Create a new item
- **PUT /items/<item_id>**: Update an existing item by ID
- **DELETE /items/<item_id>**: Delete an item by ID

### Testing the API

You can use tools like Postman or curl to interact with the API and perform CRUD operations.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
