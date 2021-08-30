import sqlite3
from flask import Flask, request
from flask_cors import CORS
from flask_mail import Mail, Message
import cloudinary
import cloudinary.uploader

# user table
class User(object):
    def __init__(self, id, firstname, surname, email, password):
        self.id = id
        self.firstname = firstname
        self.surname = surname
        self.email = email
        self.password = password

def table():
    conn = sqlite3.connect('e-store.db')
    print("Database opened successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS users"
                 "(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "firstname TEXT NOT NULL,"
                 "surname TEXT NOT NULL,"
                 "email TEXT NOT NULL,"
                 "password TEXT NOT NULL)")
    print("user table created succussfully")
    conn.close()

table()

def get_users():
    with sqlite3.connect('e-store.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * from users')
        users = cursor.fetchall()

        new_info = []

        for data in users:
            new_info.append(User(data[0], data[1], data[2], data[3], data[4]))
    return new_info


users = get_users()

# products table
class Products(object):
    def __init__(self, id, product_name, product_description, product_quantity, product_price, product_image):
        self.id = id
        self.product_name = product_name
        self.product_description = product_description
        self.product_quantity = product_quantity
        self.product_price = product_price
        self.product_image = product_image

def products_table():
    conn = sqlite3.connect('e-store.db')
    print("Database opened successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS products"
                 "(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "product_name TEXT NOT NULL,"
                 "product_description TEXT NOT NULL,"
                 "product_quantity TEXT NOT NULL,"
                 "product_price TEXT NOT NULL,"
                 "product_image TEXT NOT NULL)")
    print("products table created successfully")
    conn.close()

products_table()


def get_products():
    with sqlite3.connect('e-store.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * from products')
        users = cursor.fetchall()

        new_info = []

        for data in users:
            new_info.append(Products(data[0], data[1], data[2], data[3], data[4], data[5]))
    return new_info

products = get_products()


def image_url():
    app.logger.info('in upload route')
    cloudinary.config(cloud_name= "dz9atuzxv",
                      api_key= "245543481577747",
                      api_secret= "qTUbSOYMv9sGXQftdvCn23PRPek")

    upload_result = None
    if request.method == 'POST' or request.method == 'PUT':
        product_image = request.json['product_image']
        app.logger.info('%s file_to_upload', product_image)
        if product_image:
            upload_result = cloudinary.uploader.upload(product_image)
            app.logger.info(upload_result)
            return upload_result['url']


app = Flask(__name__)
CORS(app)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'isaacscassiem2003@gmail.com'
app.config['MAIL_PASSWORD'] = 'CassiemIsaacs@2003'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# user registrastion
@app.route('/user-registration/', methods=["POST"])
def user_registration():
    response = {

    }
    if request.method == "POST":
        with sqlite3.connect("e-store.db") as conn:
            firstname = request.json['firstname']
            surname = request.json['surname']
            email = request.json['email']
            password = request.json['password']
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (firstname, surname, email, password) VALUES(?, ?, ?, ?)",
                           (firstname, surname, email, password))
            conn.commit()
            response["message"] = 'Success'
            response["status_code"] = 201

        msg = Message('Hello Message', sender='isaacscassiem2003@gmail.com', recipients=[email])
        msg.body = "My email using Flask"
        mail.send(msg)
        print("message sent!")
    return response

# login route
@app.route('/user-login/', methods=["PATCH"])
def user_login():
    response = {}

    if request.method == 'PATCH':
        email = request.json['email']
        password = request.json['password']

        with sqlite3.connect('e-store.db') as conn:
            cursor = conn.cursor()
            cursor.row_factory = sqlite3.Row
            cursor.execute('SELECT * FROM users WHERE email=? and password=?', (email, password))
            user = cursor.fetchall()
            data = []

            for a in user:
                data.append({u: a[u] for u in a.keys()})

            response['message'] = 'Account collected'
            response['status_code'] = 200
            response['data'] = data

        return response



# gets users
@app.route('/get-users/', methods=['GET'])
def get_users():
    response = {}
    with sqlite3.connect('e-store.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        account = cursor.fetchall()

    response['status_code'] = 201
    response['data'] = account
    return response

# shows one user
@app.route('/get-user/<int:id>', methods=['GET'])
def get_user(id):
    response = {}
    with sqlite3.connect('e-store.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id=" + str(id))
        carts = cursor.fetchall()

    response['status_code'] = 201
    response['data'] = carts
    return response

# delete users
@app.route("/delete-users/<int:id>", )
def delete_user(id):
    response = {}
    with sqlite3.connect("e-store.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=" + str(id))
        conn.commit()
        response['status_code'] = 201
        response['message'] = "user deleted successfully"
    return response

# route to edit users
@app.route('/edit-users/<int:id>/', methods=['PUT'])
def edit_user(id):
    response = {}

    if request.method == "PUT":
        with sqlite3.connect('e-store.db') as conn:
            firstname = request.json['firstname']
            surname = request.json['surname']
            email = request.json['email']
            password = request.json['password']
            put_data = {}
            if firstname is not None:
                put_data["firstname"] = firstname
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET firstname =? WHERE id =?", (put_data['firstname'], id))
                conn.commit()
                response['message'] = "Update was successful"
                response["status_code"] = 201

            if surname is not None:
                put_data["surname"] = surname
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET surname =? WHERE id =?", (put_data['surname'], id))
                conn.commit()
                response['message'] = "Update was successful"
                response["status_code"] = 201

            if email is not None:
                put_data["email"] = email
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET email =? WHERE id =?", (put_data['email'], id))
                conn.commit()
                response['message'] = "Update was successful"
                response["status_code"] = 201

            if password is not None:
                put_data["password"] = password
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET password =? WHERE id =?", (put_data['password'], id))
                conn.commit()
                response['message'] = "Update was successful"
                response["status_code"] = 201
            return response


# creates products
@app.route('/products-create/', methods=['POST'])
def products_create():
    response = {}

    if request.method == "POST":
        product_name = request.json['product_name']
        product_description = request.json['product_description']
        product_quantity = request.json['product_quantity']
        product_price = request.json['product_price']
        product_image = image_url()

        with sqlite3.connect('e-store.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (product_name, product_description, product_quantity, product_price, "
                           "product_image)"
                           "VALUES(?, ?, ?, ?, ?)",
                           (product_name, product_description, product_quantity, product_price, product_image))
            conn.commit()
            response['message'] = "item added successfully"
            response['status_code'] = 201
        return response


# show product
@app.route('/get-products/', methods=['GET'])
def get_products():
    response = {}
    with sqlite3.connect('e-store.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        carts = cursor.fetchall()

    response['status_code'] = 201
    response['data'] = carts
    return response

# shows one product
@app.route('/get-product/<int:id>', methods=['GET'])
def get_product(id):
    response = {}
    with sqlite3.connect('e-store.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id=" + str(id))
        carts = cursor.fetchall()

    response['status_code'] = 201
    response['data'] = carts
    return response

# delete product
@app.route("/delete-product/<int:id>", )
def delete_product(id):
    response = {}
    with sqlite3.connect("e-store.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id=" + str(id))
        conn.commit()
        response['status_code'] = 201
        response['message'] = "product deleted successfully"
    return response

# route to edit products
@app.route('/edit-product/<int:id>/', methods=['PUT'])
def edit_product(id):
    response = {}

    if request.method == "PUT":
        with sqlite3.connect('e-store.db') as conn:
            product_name = request.json['product_name']
            product_description = request.json['product_description']
            product_quantity = request.json['product_quantity']
            product_price = request.json['product_price']
            product_image = request.json['product_image']
            put_data = {}

            if product_name is not None:
                put_data["product_name"] = product_name
                cursor = conn.cursor()
                cursor.execute("UPDATE products SET product_name =? WHERE id =?", (put_data['product_name'], id))
                conn.commit()
                response['message'] = "Update was successful"
                response["status_code"] = 201

            if product_description is not None:
                put_data["product_description"] = product_description
                cursor = conn.cursor()
                cursor.execute("UPDATE products SET product_description =? WHERE id =?", (put_data['product_description'], id))
                conn.commit()
                response['message'] = "Update was successful"
                response["status_code"] = 201

            if product_quantity is not None:
                put_data["product_quantity"] = product_quantity
                cursor = conn.cursor()
                cursor.execute("UPDATE products SET product_quantity =? WHERE id =?", (put_data['product_quantity'], id))
                conn.commit()
                response['message'] = "Update was successful"
                response["status_code"] = 201

            if product_price is not None:
                put_data["product_price"] = product_price
                cursor = conn.cursor()
                cursor.execute("UPDATE products SET product_price =? WHERE id =?", (put_data['product_price'], id))
                conn.commit()
                response['message'] = "Update was successful"
                response["status_code"] = 201

            if product_image is not None:
                put_data["product_image"] = image_url()
                cursor = conn.cursor()
                cursor.execute("UPDATE products SET product_image =? WHERE id =?",
                               (put_data['product_image'], id))
                conn.commit()
                response['message'] = "Update was successful"
                response["status_code"] = 201
            return response



if __name__ == '__main__':
    app.run()
