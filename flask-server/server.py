
from flask import Flask
from flask_cors import CORS
from routes.auth import auth_bp
from routes.data_source import data_source_bp
from routes.language_model import language_model_bp
from routes.query import query_bp
from routes.tools_list import tools_bp

app=Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(data_source_bp, url_prefix='/data-source')
app.register_blueprint(language_model_bp, url_prefix='/language-model')
app.register_blueprint(query_bp, url_prefix='/query')
app.register_blueprint(tools_bp, url_prefix='/tools')

if __name__=="__main__":
    app.run(debug=True, port=5001)