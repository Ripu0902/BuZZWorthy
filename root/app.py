import os
from flask import Flask
from application.config import LocalDevelopementConfig
from application.database import db


app = None

def create_app():
    app = Flask(__name__,template_folder="templates")
    if os.getenv('ENV',"developement") == "production":
        raise Exception("Currently no production config is setup.")
    else:
        print("Starting local developement")
        app.config.from_object(LocalDevelopementConfig)
    
        
    db.init_app(app)
    app.app_context().push()
    # with app.app_context():
    db.create_all()


    return app

app = create_app()


from application.controllers import *

if __name__ == "__main__":
    app.run()