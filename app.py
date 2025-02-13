from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Make sure to use a secure key in production

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirect to login if not logged in

# Load users from JSON file
def load_users():
    with open('users.json') as f:
        return json.load(f)

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id):
        self.id = id

    @staticmethod
    def get(user_id):
        users = load_users()
        return User(user_id) if user_id in users else None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Validate username/password (simplified)
        users = load_users()
        if username in users and users[username] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('home'))

        flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)