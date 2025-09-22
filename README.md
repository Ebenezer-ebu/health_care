# Healthcare Spending Survey Tool
A comprehensive web application for collecting and analyzing income and spending data, specifically designed for healthcare industry research and product launch preparation.

## 📋 Overview
This tool enables Washington, DC-based data analysis companies to:
- Collect participant demographic and financial data through a user-friendly web interface
- Store data in both MongoDB and CSV formats for flexibility
- Analyze spending patterns across different categories
- Generate visualizations for client presentations
- Deploy on AWS for scalable data collection

## 🚀 Features
- **Web Form**: Responsive survey form with age, gender, income, and expense category inputs
- **Data Storage**: Dual storage in MongoDB database and CSV file
- **Data Analysis**: Python class for processing user data with comprehensive visualization capabilities
- **Visualizations**: Multiple charts showing income distribution, spending patterns, and demographic insights
- **AWS Ready**: Configured for easy deployment on Amazon Web Services

## 🛠️ Installation & Setup

**Prerequisites**
- Python 3.8+
- MongoDB (optional, but recommended)
- pip (Python package manager)

**Step 1: Clone or Download the Project**
```
mkdir healthcare_survey
cd healthcare_survey
```
**Step 2: Install Dependencies**
```
pip install flask pymongo pandas matplotlib seaborn
```
**Step 3: Set Up MongoDB**
1. Download and install MongoDB Community Edition from https://www.mongodb.com/try/download/community
2. Start the MongoDB service (process varies by operating system)
3. The application will automatically create the healthcare_survey database

**Step 4: Run Setup Script**
```
python setup.py
```
This will create all necessary directories and the CSV file with proper headers.
**Step 5: Launch the Application**
```
python app.py
```
**Step 6: Access the Application**
Open your web browser and navigate to:
```
http://localhost:4000
```

**Step 7: Export data from MongoDB to CSV**
```
python user_class.py
```

## 📁 Project Structure
```
healthcare_survey/
├── app.py         
├── user_class.py      
├── setup.py            
├── requirements.txt  
├── data_processing.ipynb     
├── survey_data.csv      
├── templates/
│   ├── index.html     
│   └── success.html 
└── static/
    └── css/
        └── style.css  
```

## 🎯 How to Use
## Data Collection
1. Navigate to the survey form at http://localhost:4000
2. Fill in participant details:
    - Age (18-100)
    - Gender (Male, Female)
    - Total monthly income
    - Expense categories (check boxes and enter amounts)
3. Submit the form
4. Data is saved to both MongoDB and CSV file

## Data Analysis
1. Run the Jupyter notebook data_processing.ipynb:
```
jupyter notebook data_processing.ipynb
```
2. Execute all cells to generate visualizations:
    - Age vs. Income distribution
    - Gender distribution across spending categories
    - Healthcare spending by age
    - Income vs. Expenses scatter plot

## 📊 Output Visualizations
The tool generates the following charts for client presentations:
1. **Age-Income Distribution**: Shows which age groups have the highest income
2. **Gender Distribution**: Pie chart of participant demographics
3. **Spending by Category**: Bar charts showing spending patterns across categories
4. **Healthcare Spending by Age**: Line chart tracking healthcare expenses across age groups
5. **Income vs Expenses**: Scatter plot showing correlation between income and spending

All charts are saved as high-resolution PNG files suitable for PowerPoint presentations.

## 🔧 Troubleshooting
## Common Issues
1. MongoDB Connection Error:
    - The application will still work and save data to CSV
    - Install MongoDB or check if the service is running
2. Styling Not Appearing:
    - Check if the static/css/style.css file exists
    - Run the setup script again: python setup.py
3. Port Already in Use:
    - Change the port in app.py or stop other applications using port 4000

## Aws EC2 Instance
The app is hosted here. Access link below
```
http://34.201.92.55:4000/
```
