import sqlite3

def connect_to_db():
    conn = sqlite3.connect('database.db')
    return conn

def create_db_table():
    output_json = {}
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE records (
                user_id INTEGER NOT NULL,
                barcode TEXT NOT NULL,
                qty INTEGER NOT NULL,
                created_on TEXT DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        # CREATE TABLE users (
        #         id INTEGER PRIMARY KEY AUTOINCREMENT,
        #         username VARCHAR(100) UNIQUE,
        #         name VARCHAR(100) NOT NULL,
        #         email VARCHAR(100),
        #         phone VARCHAR(30),
        #         password TEXT
        #     );

        conn.commit()
        print("User table created successfully")
        output_json = {"message":"done"}
    except Exception as e:
        print("User table creation failed -", e.message,"~", e.args)
        output_json = {"error":e.message,"stack":e.args}
    finally:
        conn.close()
    return output_json

def insert_user(user):
    inserted_user = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, name, email, phone, password) VALUES (?, ?, ?, ?, ?)", (user['username'], user['name'],   
                    user['email'], user['phone'], user['password'] ))
        conn.commit()
        inserted_user = get_user_by_id(cur.lastrowid)
    except Exception as e:
        conn().rollback()
        inserted_user = {"error":e.message,"stack":e.args}

    finally:
        conn.close()

    return inserted_user

def get_user_by_id(user_id):
    user = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id = ?", 
                       (user_id,))
        row = cur.fetchone()

        # convert row object to dictionary
        user["id"] = row["id"]
        user["username"] = row["username"]
        user["name"] = row["name"]
        user["email"] = row["email"]
        user["phone"] = row["phone"]
    except:
        user = {}

    return user

def login(user_data):
    user = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (user_data["username"], user_data["password"]))
        row = cur.fetchone()
        # convert row object to dictionary
        user["id"] = row[0]
        user["name"] = row[2]
    except Exception as e:
        user = {"error":e.args}
    return user

def submitproduct(product_data):
    row_data = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO records (user_id, barcode, qty) VALUES (?, ?, ?)", (product_data['user_id'], product_data['barcode'],   
                    product_data['qty'] ))
        conn.commit()
        row_data = {"message": "submitted successfully", "code":200}
    except:
        conn().rollback()
        row_data = {"message": "error occured", "code":500}

    finally:
        conn.close()

    return row_data
