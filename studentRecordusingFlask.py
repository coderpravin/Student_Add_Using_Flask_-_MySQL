from flask import Flask, render_template, request, redirect,url_for
import mysql.connector
import pymysql

app = Flask(__name__)

#mysql connection database

db_config = {
    "host" : "localhost",
    "user" : "root", 
    "password" : "pramodmore",
    "database" : "student_db"
}

#Database Connection
def get_connection():
    return pymysql.connect(**db_config)
    
#create route
@app.route("/")
def index():
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', students=students)


@app.route("/addStudent", methods=["GET", "POST"])
def add_Student():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        mobile = request.form["mobile"]

    #insert the connection 
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("Insert into students (name, email, mobile) Values(%s, %s, %s)", (name, email, mobile))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('addStudent.html')

@app.route("/delete_student/<int:student_id>")
def delete_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("Delete from students Where id = %s", (student_id))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug=True)