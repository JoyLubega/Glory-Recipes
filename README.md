[![Glory](https://img.shields.io/badge/GloryRecipes-API-yellow.svg)]()
[![Coverage Status](https://coveralls.io/repos/github/JoyLubega/Glory-Recipes/badge.svg?branch=ft-166540411-SetUp-Project)](https://coveralls.io/github/JoyLubega/Glory-Recipes?branch=ft-166540411-SetUp-Project)
[![Maintainability](https://api.codeclimate.com/v1/badges/608cf40af2de75aaab0b/maintainability)](https://codeclimate.com/github/JoyLubega/Glory-Recipes/maintainability)


# Glory-Recipes
A recipes Api for user to create and re use their recipes.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.
- Just clone this repository by typing: `https://github.com/JoyLubega/Glory-Recipes.git`
- Switch to project directory: `cd Glory-Recipes`
- Install project requirements using python pip3. But wait, you have to have some stuff before you get to this point. So these are:

### Prerequisites

- Python3.6 and above
- Python virtual environment
Just type:
```
python -V
```
in your terminal and if its not greater than or equal to 3.6, you're not in big trouble, there are tons of tutorials to get up up and running with these. Just grub one then come back when done.

### Installing

Now, you have python3 and a way of running a virtual environment. Lets set up the project environment.(remember we're still in the app directory)

1. Create your virtual environment. Usually, without any wrappers:
```
python -m venv my_venv
```
2. Start your virtual environment:
```
source my_venv/bin/activate
```
3. Install the project requirements specified in the requirements.txt file. Usually,
```
pip3 install -r requirements.txt
```
4. *Do Migrations*. This application uses postgresql. If you don't have psql you may install it here.
Create a `glory-recipe` database to be used by the application while running on your localhost.
Then, you can do migrations as:
```
python manage.py db migrate
python manage.py db upgrade
```

This is enough to get you started.
You can now run the application using:

`make run.py`

    
## Running the tests:

`make test`

## API Endpoints
You can use postman or even curl to reach out to the following api endpoints:

URL Endpoint	|               HTTP Request   | Resource Accessed | Access Type| json fields
----------------|-----------------|-------------|------------------ |------------|
/auth/register   |      POST	| Register a new user|public| name, email, password
/auth/login	  |     POST	| Login and retrieve token|public| email, password
/auth/users   |     GET     | Get all users in the database | public
/auth/users/<user_id>   |     GET     | Get a user by id in the database | public
/auth/users/<user_id>   |     PUT     | Update a user in the database | public
/auth/users/<user_id>   |     DELETE     | Delete a user permanently in the database | public
/category	              |      POST	|Create a new category|private| name, Parent_id is optional
/categories	              |      GET	|     Retrieve all categories|private
/categories/<category_id>            |  	GET	    | Retrieve a category by ID | private
/categories/<category_id> 	          |      PUT	|     Update a category |private
/categories/<category_id> 	          |      DELETE	| Delete a category |private


### Searching for categories

Functionality to search catego using the parameter `q` in the GET request is enabled. 
Example:

`GET http://localhost:/categories?q=<keyword>`

This request will return all categories with `keyword` in their name