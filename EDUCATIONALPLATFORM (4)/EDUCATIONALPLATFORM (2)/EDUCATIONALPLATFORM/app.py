from flask import Flask, render_template, request, redirect, url_for, flash, session
import pymongo
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['Projectnest']
users_collection = db['user']

@app.route('/')
def navbarr():
    return render_template('navbarr.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/course')
def course():
    return render_template('course.html')

@app.route('/videos')
def videos():
    return render_template('videos.html')

@app.route('/syllabus')
def syllabus():
    return render_template('syllabus.html')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        
        if users_collection.find_one({'username': username}):
            flash('Username already exists', 'error')
            return redirect('/signup')

    
        user_data = {
            'username': username,
            'email': email,
            'password': hashed_password
        }
        users_collection.insert_one(user_data)

        flash('Account created successfully', 'success')
        return redirect('/login')

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        entered_password_hashed = hashlib.sha256(password.encode()).hexdigest()
        user = users_collection.find_one({'username': username, 'password': entered_password_hashed})

        if user:
            flash('Login successful', 'success')
            session['username'] = username  
            return redirect('/')
        else:
            flash('Login failed. Please check your username and password.', 'error')

    return render_template('login.html')



if __name__ == '__main__':
    app.run(debug=True)