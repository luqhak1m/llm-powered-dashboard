
from flask import Flask
from flask_cors import CORS
from routes.auth import auth_bp
from routes.data_source import data_source_bp

app=Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(data_source_bp, url_prefix='/data-source')

if __name__=="__main__":
    app.run(debug=True, port=5001)