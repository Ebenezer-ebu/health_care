import os

def setup_directories():
    """Create necessary directories for the project"""
    directories = [
        'templates',
        'static/css',
        'data'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")
    
    # Create empty CSV file with headers if it doesn't exist
    csv_file = 'survey_data.csv'
    if not os.path.exists(csv_file):
        with open(csv_file, 'w') as f:
            f.write('Age,Gender,Total_Income,Utilities,Entertainment,School_Fees,Shopping,Healthcare,Total_Expenses,Timestamp\n')
        print(f"Created CSV file: {csv_file}")
    
    print("Setup completed successfully!")

if __name__ == "__main__":
    setup_directories()