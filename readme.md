# What is this?

Hello and welcome aboard! This project presents an automated data visualization tool using multi agent framework. Submit a prompt and it will visualize your data. It's that simple!

# How to run?

### Make sure you have installed:

- Python 3.8+
- Node.js 14+ and npm (or yarn)
- pip (Python package installer)

### Project Structure:

- /flask-server      → Flask app (Backend)
- /my-react-app      → React app (Frontend)

### Running the App:

## Step 1: Run the Flask Backend

- cd flask-server
- python -m venv venv

#### on Linux/macOS:
- source venv/bin/activate 

#### on Windows
- venv\Scripts\activate     

- pip install -r requirements.txt
- python server.py

## Step 2: Run the React Frontend

- cd my-react-app
- npm install
- npm start

# How to visualize my data?

### Step 1: Login

- Create and account and login

### Step 2: Database conenction

- Make the connection to your local MySQL database. 
- From the main menu, navigate to Data Source > Connect to Data Source. 
- The credentials required are your database username, host, database name, and password.

### Step 3: Navigate to the prompt field page

- Navigate back to the main menu and go to Generate Visual and Analysis page.

### Step 4: Choose your visual

- Click on the Choose Tools button to open a dropdown of tools list. Select at least one (1) visual you wish to produce.

### Step 5: Submit your prompt.

- Enter the prompt and witness the magic!