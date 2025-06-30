# How to run?

### Make sure you have installed:

Python 3.8+
Node.js 14+ and npm (or yarn)
pip (Python package installer)

### Project Structure:

/flask-server      → Flask app (Backend)
/my-react-app      → React app (Frontend)

### Running the App:

## Step 1 - Run the Flask Backend

cd flask-server
python -m venv venv

#### on Linux/macOS:
source venv/bin/activate 

#### on Windows
venv\Scripts\activate     

pip install -r requirements.txt
python server.py

## Step 2 - Run the React Frontend

cd my-react-app
npm install
npm start