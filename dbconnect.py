import sqlite3

def connect_to_db():
    conn = sqlite3.connect('database.db')
    return conn

def create_db_table():
    output_json = {}
    try:
        conn = connect_to_db()
        conn.execute('''
        DELETE from mapping;
        ''')
        # CREATE TABLE mapping (
        #         id INTEGER NOT NULL,
        #         barcode TEXT NOT NULL,
        #         name TEXT
        #     );
        #CREATE TABLE records (
        #        user_id INTEGER NOT NULL,
        #        barcode TEXT NOT NULL,
        #        qty INTEGER NOT NULL,
        #        created_on TEXT DEFAULT CURRENT_TIMESTAMP
        #    );
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
        print("User table creation failed -","~", e.args)
        output_json = {"stack":e.args}
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

def insert_sku_id(data):
    inserted_user = {}
    s = ""
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        for x in data:
            cur.execute("INSERT INTO mapping (id, barcode, name) VALUES (?, ?, ?)", (x['ID'], x['SKU'], x["Name"]))
        conn.commit()
        inserted_user = {"msg":"success"}
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

def daily_transaction():
    rows = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("""select u.name,r.barcode,r.qty,datetime(r.created_on ||"-05:30") as
        entry_time from users u join records r on u.id=r.user_id order by r.created_on desc""" )
        rows = cur.fetchall();
        print(rows)
    except:
        conn().rollback()
        rows = {"message": "error occured", "code":500}

    finally:
        conn.close()
    return rows


def daily_transaction_report():
    lst = []
    rows = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        # cur.execute(""" select id,barcode,name from mapping""")
        cur.execute("""select u.name,r.barcode,r.qty,datetime(r.created_on ||"-05:30") as
        entry_time,m.name from users u join records r on u.id=r.user_id left join mapping m on m.barcode=r.barcode order by r.created_on desc""")
        rows = cur.fetchall();
        for row in rows:
            d = {}
            d["user"] = row[0]
            d["itemcode"] = row[1]
            d["qty"] = row[2]
            d["entry_date"] = row[3]
            d["name"] = row[4]
            lst.append(d)
    except:
        conn().rollback()
        rows = {"message": "error occured", "code":500}

    finally:
        conn.close()
    return lst

def qrscanner():
    try:

        import cv2

        cap = cv2.VideoCapture(0)
        # initialize the cv2 QRCode detector
        detector = cv2.QRCodeDetector()
        while True:
            _, img = cap.read()
            # detect and decode
            data, bbox, _ = detector.detectAndDecode(img)
            # check if there is a QRCode in the image
            if data:
                a=data
                break
            cv2.imshow("QRCODEscanner", img)
            if cv2.waitKey(1) == ord("q"):
                break

        # b=webbrowser.open(str(a))
        cap.release()
        cv2.destroyAllWindows()
        return str(a)
    except Exception as e:
        print(type(e))    # the exception instance
        print(e.args)     # arguments stored in .args
        print(e)
