# Import necessary modules from Flask and external files
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from .send_email import send_mail

# Initialize the Flask application
app = Flask(__name__)

# Set the environment variable for development or production
ENV = 'dev'

# Configure the app based on the environment
if ENV == 'dev':
    app.debug = True  # Enable debug mode in development
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Hussein_Farhat10@localhost/lexus'  # Database URI for dev
else:
    app.debug = False  # Disable debug mode in production
    app.config['SQLALCHEMY_DATABASE_URI'] = ''  # Placeholder for production database URI

# Disable SQLAlchemy event notifications for performance
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Bind SQLAlchemy to the Flask app
db = SQLAlchemy(app)

# Define a database model for storing feedback
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    customer = db.Column(db.String(200), unique=True)  # Unique customer name column
    dealer = db.Column(db.String(200))  # Dealer name column
    rating = db.Column(db.Integer)  # Rating column
    comments = db.Column(db.Text())  # Comments column

    # Constructor to initialize feedback attributes
    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments

# Define the route for the homepage
@app.route('/')
def index():
    return render_template('index.html')  # Render the homepage template

# Define the route to handle feedback submissions
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':  # Check if the request method is POST
        customer = request.form.get('customer')  # Get customer input from the form
        dealer = request.form.get('dealer')  # Get dealer input from the form
        rating = request.form.get('rating')  # Get rating input from the form
        comments = request.form.get('comments')  # Get comments input from the form
        if customer == "" or dealer == "":  # Check for missing required fields
            return render_template('index.html', message='please fill in the required fields')
        # Check if the feedback from the customer already exists
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, dealer, rating, comments)  # Create a new Feedback object
            db.session.add(data)  # Add the feedback to the database session
            db.session.commit()  # Commit the session to save the feedback
            send_mail(customer, dealer, rating, comments)  # Send feedback details via email
            return render_template('success.html')  # Render the success page
        # If feedback already exists, return to the homepage with a message
        return render_template('index.html', message='you have already submitted feedback')

# Run the Flask app when executed directly
if __name__ == '__main__':
    app.run()