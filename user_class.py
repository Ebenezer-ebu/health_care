import csv
from datetime import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB configuration from environment variables
MONGODB_URI = os.getenv('MONGODB_URI')
MONGODB_DATABASE = os.getenv('MONGODB_DATABASE', 'healthcare_survey')
MONGODB_COLLECTION = os.getenv('MONGODB_COLLECTION', 'participants')

class User:
    def __init__(self, age, gender, total_income, expenses):
        self.age = age
        self.gender = gender
        self.total_income = total_income
        self.expenses = expenses
        self.total_expenses = sum(expenses.values())
        self.timestamp = datetime.now()
    
    def to_dict(self):
        return {
            'Age': self.age,
            'Gender': self.gender,
            'Total_Income': self.total_income,
            'Utilities': self.expenses.get('utilities', 0),
            'Entertainment': self.expenses.get('entertainment', 0),
            'School_Fees': self.expenses.get('school_fees', 0),
            'Shopping': self.expenses.get('shopping', 0),
            'Healthcare': self.expenses.get('healthcare', 0),
            'Total_Expenses': self.total_expenses,
            'Timestamp': self.timestamp
        }
    
    @classmethod
    def load_from_csv(cls, filename):
        users = []
        try:
            with open(filename, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    expenses = {
                        'utilities': float(row.get('Utilities', 0)),
                        'entertainment': float(row.get('Entertainment', 0)),
                        'school_fees': float(row.get('School_Fees', 0)),
                        'shopping': float(row.get('Shopping', 0)),
                        'healthcare': float(row.get('Healthcare', 0))
                    }
                    
                    user = cls(
                        age=int(row['Age']),
                        gender=row['Gender'],
                        total_income=float(row['Total_Income']),
                        expenses=expenses
                    )
                    users.append(user)
        except FileNotFoundError:
            print(f"File {filename} not found.")
        return users
    
    @classmethod
    def export_mongodb_to_csv(cls, csv_filename):
        """
        Export data from MongoDB to CSV file by looping through the collection
        Uses environment variables for MongoDB configuration
        """
        # Check if MongoDB is configured
        if not MONGODB_URI:
            print("MongoDB URI not configured in environment variables.")
            return False
            
        try:
            # Connect to MongoDB
            client = MongoClient(
                MONGODB_URI,
                serverSelectionTimeoutMS=10000,
                socketTimeoutMS=45000,
                connectTimeoutMS=10000
            )
            db = client[MONGODB_DATABASE]
            collection = db[MONGODB_COLLECTION]
            
            # Get all documents from the collection
            documents = collection.find()
            
            # Prepare data for CSV
            csv_data = []
            for doc in documents:
                # Convert MongoDB document to CSV row format
                csv_row = {
                    'Age': doc.get('age', ''),
                    'Gender': doc.get('gender', ''),
                    'Total_Income': doc.get('total_income', ''),
                    'Utilities': doc.get('expenses', {}).get('utilities', 0),
                    'Entertainment': doc.get('expenses', {}).get('entertainment', 0),
                    'School_Fees': doc.get('expenses', {}).get('school_fees', 0),
                    'Shopping': doc.get('expenses', {}).get('shopping', 0),
                    'Healthcare': doc.get('expenses', {}).get('healthcare', 0),
                    'Total_Expenses': doc.get('total_expenses', ''),
                    'Timestamp': doc.get('timestamp', '')
                }
                csv_data.append(csv_row)
            
            # Write to CSV file
            if csv_data:
                fieldnames = ['Age', 'Gender', 'Total_Income', 'Utilities', 'Entertainment', 
                             'School_Fees', 'Shopping', 'Healthcare', 'Total_Expenses', 'Timestamp']
                
                with open(csv_filename, 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(csv_data)
                
                print(f"Successfully exported {len(csv_data)} records from MongoDB to {csv_filename}")
                return True
            else:
                print("No data found in MongoDB collection")
                return False
                
        except Exception as e:
            print(f"Error exporting MongoDB to CSV: {e}")
            return False

# Example usage
if __name__ == "__main__":
    # Create sample users
    sample_expenses = {
        'utilities': 200,
        'entertainment': 150,
        'healthcare': 300
    }
    
    user1 = User(30, 'Male', 5000, sample_expenses)
    print(user1.to_dict())
    
    # Example of exporting MongoDB to CSV
    csv_filename = 'survey_data.csv'
    
    # Export data from MongoDB to CSV
    User.export_mongodb_to_csv(csv_filename)