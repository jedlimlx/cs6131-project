import urllib.parse
from flask import Flask, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'project'
CORS(app)

mysql = MySQL(app)


@app.route('/login/username=<string:username>&password=<string:password>')
def login(username, password):
    cursor = mysql.connection.cursor()

    # Executing SQL Statements
    cursor.execute(f"""SELECT * FROM user WHERE username="{username}" """)
    data = cursor.fetchone()

    # Saving the actions performed on the DB
    mysql.connection.commit()

    # Closing the cursor
    cursor.close()

    if data and data[3] == password:
        return jsonify(
            {
                "status": 1,
                "uid": data[0],
                "username": data[1],
                "email": data[2],
                "password": data[3],
                "firstname": data[4],
                "lastname": data[5]
            }
        )
    else:
        return jsonify(
            {
                "status": 0
            }
        )


@app.route('/update_user/uid=<int:uid>&firstname=<string:firstname>&'
           'lastname=<string:lastname>&email=<string:email>')
def update_user(uid, firstname, lastname, email):
    cursor = mysql.connection.cursor()

    # Executing SQL Statements
    cursor.execute(f"""
    UPDATE user 
    SET email="{email}", firstname="{firstname}", lastname="{lastname}" 
    WHERE uid={uid}
    """)

    # Saving the actions performed on the DB
    mysql.connection.commit()

    # Closing the cursor
    cursor.close()

    return ""


@app.route('/change_password/uid=<int:uid>&password=<string:password>&'
           'new_password=<string:new_password>')
def change_password(uid, password, new_password):
    cursor = mysql.connection.cursor()

    # Executing SQL Statements
    cursor.execute(f"""
    SELECT *
    FROM user 
    WHERE uid={uid}
    """)
    data = cursor.fetchone()

    if data and data[3] == password:
        cursor.execute(f"""
        UPDATE user
        SET password="{new_password}"
        WHERE uid={uid}
        """)

        mysql.connection.commit()
        cursor.close()

        return jsonify(
            {
                "status": 1
            }
        )
    else:
        mysql.connection.commit()
        cursor.close()

        return jsonify(
            {
                "status": 0
            }
        )


@app.route('/reference/doi=<string:doi>')
def get_reference(doi):
    cursor = mysql.connection.cursor()

    # Executing SQL Statements
    doi = doi.replace("$", "%").replace("\"", "")
    doi = urllib.parse.unquote(doi)
    cursor.execute(f"""SELECT * FROM reference WHERE doi="{doi}" """)
    data = cursor.fetchone()

    if data:
        json = {
            "status": 1,
            "doi": data[0],
            "title": data[1],
            "type": data[2]
        }

        cursor.execute(f"""SELECT * FROM authors WHERE doi="{doi}" """)
        data = cursor.fetchall()
        json["authors"] = [x[1] for x in data]

        reference_type = json["type"]
        if reference_type == 0:  # journal
            cursor.execute(f"""SELECT * FROM journalArticle WHERE doi="{doi}" """)
            data = cursor.fetchone()
            json["pname"] = data[1]
            json["minPage"] = data[2]
            json["maxPage"] = data[3]
            json["number"] = data[4]
            json["volume"] = data[5]
            json["date"] = data[6]
        elif reference_type == 1:  # conference
            cursor.execute(f"""SELECT * FROM conferenceArticle WHERE doi="{doi}" """)
            data = cursor.fetchone()
            json["pname"] = data[1]
            json["year"] = data[2]
        elif reference_type == 2:  # book
            cursor.execute(f"""SELECT * FROM book WHERE doi="{doi}" """)
            data = cursor.fetchone()
            json["minPage"] = data[1]
            json["maxPage"] = data[2]
            json["isbn"] = data[3]
        elif reference_type == 3:  # website
            cursor.execute(f"""SELECT * FROM website WHERE doi="{doi}" """)
            data = cursor.fetchone()
            json["dateAccessed"] = data[1]

        mysql.connection.commit()
        cursor.close()

        return jsonify(json)
    else:
        mysql.connection.commit()
        cursor.close()

        return jsonify(
            {
                "status": 0
            }
        )


@app.route('/search_reference/q=<string:query>')
def search_reference(query):
    cursor = mysql.connection.cursor()

    # Executing SQL Statements
    cursor.execute(f"""SELECT doi FROM reference WHERE title LIKE "%{query}%" """)
    data = cursor.fetchall()

    # Saving the actions performed on the DB
    mysql.connection.commit()

    # Closing the cursor
    cursor.close()

    lst = []
    for doi in data:
        lst.append(get_reference(doi[0]).json)

    return jsonify(lst)


@app.route('/references/uid=<int:uid>')
def get_references_1(uid):
    cursor = mysql.connection.cursor()

    # Executing SQL Statements
    cursor.execute(f"""SELECT * FROM isRead WHERE uid={uid} """)
    data = cursor.fetchall()

    # Saving the actions performed on the DB
    mysql.connection.commit()

    # Closing the cursor
    cursor.close()

    lst = []
    for i in data:
        lst.append(get_reference(i[0]).json)

    return jsonify(lst)


@app.route('/references/pid=<int:pid>')
def get_references_2(pid):
    cursor = mysql.connection.cursor()

    # Executing SQL Statements
    cursor.execute(f"""SELECT * FROM cited WHERE pid={pid} """)
    data = cursor.fetchall()

    # Saving the actions performed on the DB
    mysql.connection.commit()

    # Closing the cursor
    cursor.close()

    lst = []
    for i in data:
        lst.append(get_reference(i[0]).json)

    return jsonify(lst)


@app.route('/add_reference/doi=<string:doi>&uid=<int:uid>&read=<int:read>')
def add_reference(doi, uid, read):
    cursor = mysql.connection.cursor()

    # Executing SQL Statements
    doi = doi.replace("$", "%").replace("\"", "")
    doi = urllib.parse.unquote(doi)
    cursor.execute(f"""INSERT INTO isRead VALUES ("{doi}", {uid}, {read}) """)

    # Saving the actions performed on the DB
    mysql.connection.commit()

    # Closing the cursor
    cursor.close()


@app.route('/add_reference/doi=<string:doi>&pid=<int:pid>')
def add_reference_2(doi, pid):
    cursor = mysql.connection.cursor()

    # Executing SQL Statements
    doi = doi.replace("$", "%").replace("\"", "")
    doi = urllib.parse.unquote(doi)
    cursor.execute(f"""INSERT INTO cited VALUES ("{doi}", {pid}) """)

    # Saving the actions performed on the DB
    mysql.connection.commit()

    # Closing the cursor
    cursor.close()


if __name__ == '__main__':
    app.run()
