from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from datetime import datetime
import csv
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='static')

# Get MongoDB configuration from environment variables
MONGODB_URI = os.getenv('MONGODB_URI')
MONGODB_DATABASE = os.getenv('MONGODB_DATABASE', 'healthcare_survey')
MONGODB_COLLECTION = os.getenv('MONGODB_COLLECTION', 'participants')

# Global variables for MongoDB
mongo_client = None
db = None
collection = None

def init_mongodb():
    """Initialize MongoDB connection with proper error handling"""
    global mongo_client, db, collection
    
    # Check if MongoDB URI is configured
    if not MONGODB_URI:
        print("MongoDB URI not configured. Application will use CSV storage only.")
        return False
    
    try:
        # Connect with longer timeout for Atlas
        mongo_client = MongoClient(
            MONGODB_URI,
            serverSelectionTimeoutMS=10000,  # 10 second timeout
            socketTimeoutMS=45000,           # 45 second socket timeout
            connectTimeoutMS=10000           # 10 second connection timeout
        )
        
        # Test the connection
        mongo_client.server_info()
        
        db = mongo_client[MONGODB_DATABASE]
        collection = db[MONGODB_COLLECTION]
        
        print("Connected to MongoDB successfully")
        return True
        
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        print("Application will use CSV storage only")
        mongo_client = None
        db = None
        collection = None
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Get form data
        age = int(request.form['age'])
        gender = request.form['gender']
        total_income = float(request.form['total_income'])
        
        # Get expense data
        expenses = {
            'utilities': float(request.form.get('utilities', 0)),
            'entertainment': float(request.form.get('entertainment', 0)),
            'school_fees': float(request.form.get('school_fees', 0)),
            'shopping': float(request.form.get('shopping', 0)),
            'healthcare': float(request.form.get('healthcare', 0))
        }
        
        total_expenses = sum(expenses.values())
        
        # Create user document
        user_data = {
            'age': age,
            'gender': gender,
            'total_income': total_income,
            'expenses': expenses,
            'total_expenses': total_expenses,
            'timestamp': datetime.now()
        }
        
        # Insert into MongoDB if available - FIXED: Proper None check
        if collection is not None:
            try:
                collection.insert_one(user_data)
                print("Data successfully saved to MongoDB")
            except Exception as e:
                print(f"Error saving to MongoDB: {e}")
        else:
            print("MongoDB not available, saving to CSV only")
        
        # Append to CSV file (always do this as backup)
        csv_file = 'survey_data.csv'
        file_exists = os.path.isfile(csv_file)
        
        with open(csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['Age', 'Gender', 'Total_Income', 'Utilities', 'Entertainment', 
                               'School_Fees', 'Shopping', 'Healthcare', 'Total_Expenses', 'Timestamp'])
            
            writer.writerow([
                age, gender, total_income,
                expenses['utilities'], expenses['entertainment'],
                expenses['school_fees'], expenses['shopping'],
                expenses['healthcare'], total_expenses, datetime.now()
            ])
        
        print("Data saved to CSV file")
        return redirect(url_for('success'))
    
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/health')
def health_check():
    """Endpoint to check MongoDB connection status"""
    if collection is not None:
        try:
            # Test with a simple operation
            collection.find_one()
            return "MongoDB connection: ACTIVE", 200
        except Exception as e:
            return f"MongoDB connection: ERROR - {str(e)}", 500
    else:
        return "MongoDB: Not connected (using CSV storage only)", 200

@app.route('/config')
def config_check():
    """Endpoint to check configuration (remove in production)"""
    config_info = {
        'mongodb_uri_configured': bool(MONGODB_URI),
        'mongodb_database': MONGODB_DATABASE,
        'mongodb_collection': MONGODB_COLLECTION,
        'flask_env': os.getenv('FLASK_ENV', 'Not set'),
        'flask_debug': os.getenv('FLASK_DEBUG', 'Not set')
    }
    return config_info

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    # Initialize MongoDB connection
    init_mongodb()
    
    # Get port from environment variable or default to 4000
    port = int(os.getenv('PORT', 4000))
    
    app.run(debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true', 
            host='0.0.0.0', port=port)