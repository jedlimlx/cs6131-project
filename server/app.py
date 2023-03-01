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


if __name__ == '__main__':
    app.run()
