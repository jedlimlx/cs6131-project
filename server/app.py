import hashlib
import secrets
import urllib.parse

from flask import Flask, jsonify, session
from flask_cors import CORS
from flask_mysqldb import MySQL

from arvix import scrape_arxiv
from apl import scrape_apl
from nature import scrape_nature


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'project'
CORS(app)

mysql = MySQL(app)


# Account Management
def process_password(password):
    salt = secrets.token_hex(16)
    return hashlib.sha256((password + salt).encode()).hexdigest() + salt


def check_password(password, stored_password):
    salt = stored_password[-32:]
    return hashlib.sha256((password + salt).encode()).hexdigest() == stored_password[:-32]


@app.route('/login/username=<string:username>&password=<string:password>')
def login(username, password):
    cursor = mysql.connection.cursor()

    # Executing SQL Statements
    cursor.execute(f"""SELECT * FROM user WHERE username=%s """, (username,))
    data = cursor.fetchall()

    # Saving the actions performed on the DB
    mysql.connection.commit()

    # Closing the cursor
    cursor.close()

    if data:
        for i in data:
            if check_password(password, i[3]):
                data = i
                break
        else:
            return jsonify(
                {
                    "status": 0
                }
            )

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


@app.route('/register/username=<string:username>&'
           'email=<string:email>&'
           'first_name=<string:first_name>&'
           'last_name=<string:last_name>&'
           'password=<string:password>')
def register(username, email, first_name, last_name, password):
    try:
        cursor = mysql.connection.cursor()

        # Check largest UID
        cursor.execute(f"""
        SELECT MAX(uid) FROM user
        """)
        uid = cursor.fetchone()[0] + 1

        # Executing SQL Statements
        cursor.execute(f"""
        INSERT INTO user VALUES (%s,%s,%s,%s,%s,%s)
        """, (uid, username, email, process_password(password), first_name, last_name))

        # Saving the actions performed on the DB
        mysql.connection.commit()

        # Closing the cursor
        cursor.close()

        return jsonify(
            {
                "status": 1
            }
        )
    except Exception as e:
        return jsonify(
            {
                "status": 0,
                "error": str(e)
            }
        )


@app.route('/update_user/uid=<int:uid>&firstname=<string:firstname>&'
           'lastname=<string:lastname>&email=<string:email>')
def update_user(uid, firstname, lastname, email):
    cursor = mysql.connection.cursor()

    # Executing SQL Statements
    cursor.execute(f"""
    UPDATE user 
    SET email=%s, firstname=%s, lastname=%s 
    WHERE uid=%s
    """, (email, firstname, lastname, uid,))

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
    WHERE uid=%s
    """, (uid,))
    data = cursor.fetchone()

    if data and check_password(password, data[3]):
        cursor.execute(f"""
        UPDATE user
        SET password=%s
        WHERE uid=%s
        """, (process_password(new_password), uid,))

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


# Getting References
@app.route('/reference/doi=<string:doi>')
def get_reference(doi):
    cursor = mysql.connection.cursor()

    # Executing SQL Statements
    doi = doi.replace("$", "%").replace("\"", "")
    doi = urllib.parse.unquote(doi)
    cursor.execute(f"""SELECT * FROM reference WHERE doi=%s """, (doi,))
    data = cursor.fetchone()

    if data:
        json = {
            "status": 1,
            "doi": data[0],
            "title": data[1],
            "type": data[2]
        }

        cursor.execute(f"""SELECT * FROM authors WHERE doi=%s """, (doi,))
        data = cursor.fetchall()
        json["authors"] = [x[1] for x in data]

        reference_type = json["type"]
        if reference_type == 0:  # journal
            cursor.execute(f"""SELECT * FROM journalArticle WHERE doi=%s """, (doi,))
            data = cursor.fetchone()
            json["pname"] = data[1]
            json["minPage"] = data[2]
            json["maxPage"] = data[3]
            json["number"] = data[4]
            json["volume"] = data[5]
            json["date"] = data[6]
        elif reference_type == 1:  # conference
            cursor.execute(f"""SELECT * FROM conferenceArticle WHERE doi=%s """, (doi,))
            data = cursor.fetchone()
            json["pname"] = data[1]
            json["year"] = data[2]
        elif reference_type == 2:  # book
            cursor.execute(f"""SELECT * FROM book WHERE doi=%s """, (doi,))
            data = cursor.fetchone()
            json["minPage"] = data[1]
            json["maxPage"] = data[2]
            json["isbn"] = data[3]
        elif reference_type == 3:  # website
            cursor.execute(f"""SELECT * FROM website WHERE doi=%s """, (doi,))
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
    cursor.execute(f"""SELECT doi FROM reference WHERE title LIKE %s """, ("%"+query+"%",))
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
    cursor.execute(f"""SELECT * FROM isRead WHERE uid=%s """, (uid,))
    data = cursor.fetchall()

    # Saving the actions performed on the DB
    mysql.connection.commit()

    # Closing the cursor
    cursor.close()

    lst = []
    for i in data:
        lst.append(get_reference(i[0]).json)
        lst[-1]["read"] = i[-1]

    return jsonify(lst)


@app.route('/references/pid=<int:pid>')
def get_references_2(pid):
    cursor = mysql.connection.cursor()

    # Executing SQL Statements
    cursor.execute(f"""SELECT * FROM cited WHERE pid=%s """, (pid,))
    data = cursor.fetchall()

    # Saving the actions performed on the DB
    mysql.connection.commit()

    # Closing the cursor
    cursor.close()

    lst = []
    for i in data:
        lst.append(get_reference(i[0]).json)

    return jsonify(lst)


# Adding References
def check_doi(doi, cursor):
    cursor.execute(f"""SELECT doi FROM reference WHERE doi=%s """, (doi,))
    if len(cursor.fetchall()) == 0:
        if "arxiv" in doi:  # arxiv
            command = scrape_arxiv(doi)
        elif "10.1063" in doi:  # apl
            command = scrape_apl(doi)
        elif "10.1038" in doi:  # nature
            command = scrape_nature(doi)
        else:
            raise Exception("Unsupported DOI")

        for c in command.split(";")[:-1]:
            cursor.execute(c)

        mysql.connection.commit()


@app.route('/add_reference/doi=<string:doi>&uid=<int:uid>&read=<int:read>')
def add_reference(doi, uid, read):
    try:
        cursor = mysql.connection.cursor()

        # Executing SQL Statements
        doi = doi.replace("$", "%").replace("\"", "")
        doi = urllib.parse.unquote(doi)
        check_doi(doi, cursor)
        cursor.execute(f"""INSERT INTO isRead VALUES (%s, %s, %s) """, (doi,uid,read,))

        # Saving the actions performed on the DB
        mysql.connection.commit()

        # Closing the cursor
        cursor.close()

        return jsonify({
            "status": 1
        })
    except Exception as e:
        return jsonify({
            "status": 0,
            "error": str(e)
        })


@app.route('/add_reference/doi=<string:doi>&pid=<int:pid>')
def add_reference_2(doi, pid):
    try:
        cursor = mysql.connection.cursor()

        # Executing SQL Statements
        doi = doi.replace("$", "%").replace("\"", "")
        doi = urllib.parse.unquote(doi)
        check_doi(doi, cursor)
        cursor.execute(f"""INSERT INTO cited VALUES (%s, %s) """, (doi,pid,))

        # Saving the actions performed on the DB
        mysql.connection.commit()

        # Closing the cursor
        cursor.close()

        return jsonify({
            "status": 1
        })
    except Exception as e:
        return jsonify({
            "status": 0,
            "error": str(e)
        })


# Updating References
@app.route('/update_read/doi=<string:doi>&uid=<int:uid>&read=<int:read>')
def update_read(uid, doi, read):
    try:
        cursor = mysql.connection.cursor()

        doi = doi.replace("$", "%").replace("\"", "")
        doi = urllib.parse.unquote(doi)
        check_doi(doi, cursor)
        cursor.execute(f"""UPDATE isRead SET hasRead=%s WHERE doi=%s AND uid = %s; """, (read,doi,uid,))

        # Saving the actions performed on the DB
        mysql.connection.commit()

        # Closing the cursor
        cursor.close()

        return jsonify({
            "status": 1
        })
    except Exception as e:
        return jsonify({
            "status": 0,
            "error": str(e)
        })


@app.route('/delete_reference/doi=<string:doi>&uid=<int:uid>')
def delete_reference_1(doi, uid):
    try:
        cursor = mysql.connection.cursor()

        doi = doi.replace("$", "%").replace("\"", "")
        doi = urllib.parse.unquote(doi)
        check_doi(doi, cursor)
        cursor.execute(f"""DELETE FROM isRead WHERE doi=%s AND uid = %s; """, (doi,uid,))

        # Saving the actions performed on the DB
        mysql.connection.commit()

        # Closing the cursor
        cursor.close()

        return jsonify({
            "status": 1
        })
    except Exception as e:
        return jsonify({
            "status": 0,
            "error": str(e)
        })


@app.route('/delete_reference/doi=<string:doi>&pid=<int:pid>')
def delete_reference_2(doi, pid):
    try:
        cursor = mysql.connection.cursor()

        doi = doi.replace("$", "%").replace("\"", "")
        doi = urllib.parse.unquote(doi)
        check_doi(doi, cursor)
        cursor.execute(f"""DELETE FROM isRead WHERE doi=%s AND pid = %s; """, (doi,pid,))

        # Saving the actions performed on the DB
        mysql.connection.commit()

        # Closing the cursor
        cursor.close()

        return jsonify({
            "status": 1
        })
    except Exception as e:
        return jsonify({
            "status": 0,
            "error": str(e)
        })


# Project Management
@app.route('/projects/uid=<int:uid>')
def get_projects(uid):
    cursor = mysql.connection.cursor()

    cursor.execute(f"""SELECT pid FROM worksOn WHERE uid=%s """, (uid,))
    data = cursor.fetchall()

    projects = []
    for i in data:
        cursor.execute(f"""SELECT * FROM project WHERE pid=%s """, (i[0],))
        project_data = cursor.fetchone()
        project = {
            "pid": project_data[0],
            "name": project_data[1],
            "pname": project_data[2],
            "progress": project_data[3]
        }

        projects.append(project)

        # Get people working on the project
        # cursor.execute(f"""SELECT uid, role FROM worksOn WHERE pid="{i[0]}" """)
        # users = { x[0]: x[1] for x in cursor.fetchall() }
        # project["users"] = users

    mysql.connection.commit()
    cursor.close()

    return jsonify(projects)


@app.route('/publisher/pname=<string:pname>')
def get_publisher_information(pname):
    cursor = mysql.connection.cursor()

    cursor.execute(f"""SELECT * FROM publisher WHERE pname=%s """, (pname,))
    data = cursor.fetchone()

    mysql.connection.commit()
    cursor.close()

    return jsonify({
        "pname": data[0],
        "website": data[1],
        "type": data[2],
        "deadline": data[3]
    })


# Task Management
@app.route('/tasks/pid=<int:pid>')
def get_tasks(pid):
    cursor = mysql.connection.cursor()

    cursor.execute(f"""SELECT * FROM task WHERE pid=%s """, (pid,))
    data = cursor.fetchall()

    tasks = []
    for i in data:
        task = {
            "pid": i[0],
            "tnumber": i[1],
            "title": i[2],
            "description": i[3],
            "deadline": i[4],
            "completed": i[5]
        }

        cursor.execute(f"""
        SELECT u.uid, u.username
        FROM assigned a, user u 
        WHERE pid=%s AND tnumber=%s AND a.uid=u.uid """, (pid,i[1],))
        assigned = cursor.fetchall()

        task["assigned"] = [{"uid": x[0], "username": x[1]} for x in assigned]
        tasks.append(task)

    mysql.connection.commit()
    cursor.close()

    return jsonify(tasks)


@app.route('/assigned/pid=<int:pid>&tnumber=<int:tnumber>')
def get_assigned(pid, tnumber):
    cursor = mysql.connection.cursor()

    cursor.execute(f"""
    SELECT u.uid, u.firstname, u.username 
    FROM assigned a, user u 
    WHERE a.pid=%s AND a.tnumber=%s AND a.uid = u.uid """, (pid,tnumber,))
    data = cursor.fetchall()

    assigned = []
    for i in data:
        assigned.append(
            {
                "uid": i[0],
                "firstname": i[1],
                "username": i[2]
            }
        )

    mysql.connection.commit()
    cursor.close()

    return jsonify(assigned)


if __name__ == '__main__':
    app.run()
