from flask import Flask

#from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from config import DevConfig, ProdConfig

from Resources import api_bp
from Models import db
def create_app():
    app = Flask(__name__)
    app.config.from_object(DevConfig)

    app.register_blueprint(api_bp, url_prefix='/api')
    cors = CORS(app, resources= {r'/*':{"origins" : "*"}})

    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app

if __name__ == "__main__":
    app = create_app()
    app.run()