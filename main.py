from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import openai as ai
from bardapi import Bard
import os
import google.generativeai as palm
from data_manager import allQuestions

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = '1a2b3c4d5e6d7g8h9i10'
allResponses = []
# allQuestions = []
# os.environ['_BARD_API_KEY'] = "cQgmCmv-R5APARwdlDoA4T1ieWJiObeqOddxD-rLHIIYuIQdGetuIwoKAA7_a_OdrasAlQ."
palm.configure(api_key="AIzaSyAHilJk5w8Ha9pYFxG5amaqZoWQvWSBjHg")
# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'  # Replace ******* with  your database password.
app.config['MYSQL_DB'] = 'loginapp'

# ai.api_key = "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"

# Intialize MySQL
mysql = MySQL(app)


# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            role = account['role']
            page = '';
            if role == 'admin':
                page = 'adminhome'
            else:
                print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                page = 'home'
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("select question, answer from chat WHERE username LIKE %s", [username])
                print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                questionsFromDb = cursor.fetchall()
                if len(questionsFromDb) == 0:
                    noQues = {'qustions':'No Previous Questions Found'}
                    allQuestions.append({'questionsList': noQues})
                else:
                    allQuestions.append({'questionsList': questionsFromDb})
                # jsonify({'ques': allQuestions})
            # return jsonify({'ques': allQuestions})
            return redirect(url_for(page))
        else:
            # Account doesnt exist or username/password incorrect
            flash("Incorrect username/password!", "danger")
    return render_template('auth/login.html', title="Login")

@app.route('/get_all_questions', methods=['GET'])
def get_all_questions():
    print("[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]")
    print(allQuestions);
    return jsonify({'allQuestions': allQuestions})


# http://localhost:5000/pythonlogin/register
# This will be the registration page, we need to use both GET and POST requests
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('SELECT * FROM accounts WHERE username = %s', (username))
        cursor.execute("SELECT * FROM accounts WHERE username LIKE %s", [username])
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            flash("Account already exists!", "danger")
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash("Invalid email address!", "danger")
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash("Username must contain only characters and numbers!", "danger")
        elif not username or not password or not email:
            flash("Incorrect username/password!", "danger")
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, email, password))
            mysql.connection.commit()
            flash("You have successfully registered!", "success")
            return redirect(url_for('login'))

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash("Please fill out the form!", "danger")
    # Show registration form with message (if any)
    return render_template('auth/register.html', title="Register")


@app.route('/pythonresult/', methods=['GET', 'POST'])
def response():

    print("Request Form Data:", request.form)
    question = request.form.get('question')
    username = request.form.get('username')
    print("Username:", username)
    print("Question:", question)
    # print(Bard().get_answer(question['content']))
    response = palm.generate_text(prompt=question)
    allResponses.append({'response': response.result})
    print(response)
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('insert into chat values (NULL, %s, %s, %s) ', (username, question, response.result))
        mysql.connection.commit()
        cursor1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor1.execute("select question, answer from chat WHERE username LIKE %s", [username])
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        questionsFromDb = cursor.fetchall()
        # print(questionsFromDb)
        if len(questionsFromDb) == 0:
            noQues = {'qustions': 'No Previous Questions Found'}
            allQuestions.append({'questionsList': noQues})
        else:
            allQuestions.append({'questionsList': questionsFromDb})
    except Exception as e:
        print(e)

    print("===============================================================")
    print(allResponses)

    return jsonify({'resp': allResponses})
    # return render_template('home/home.html')


# http://localhost:5000/pythinlogin/home
# This will be the home page, only accessible for loggedin users

@app.route('/')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home/home.html', username=session['username'], title="Home")
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/adminhome')
def adminhome():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home/adminhome.html', username=session['username'], title="Admin Home")
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('auth/profile.html', username=session['username'], title="Profile")
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
