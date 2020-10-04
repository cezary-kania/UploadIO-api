from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import DevConfig, ProdConfig

from Resources import api_bp
from Models import main_db, mongo_db, mongo_client

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevConfig)

    app.register_blueprint(api_bp, url_prefix='/api')
    cors = CORS(app, resources= {r'/*':{"origins" : "*"}})
    jwt = JWTManager(app)

    mongo_client.host = app.config['MONGO_URI']
    
    main_db.init_app(app)
    with app.app_context():
        main_db.create_all()
        
    return app

if __name__ == "__main__":
    app = create_app()
    app.run()