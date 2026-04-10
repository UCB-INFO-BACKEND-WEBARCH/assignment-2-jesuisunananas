from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    
    from app.routes.tasks import tasks_blp
    from app.routes.categories import categories_blp

    app.register_blueprint(tasks_blp)
    app.register_blueprint(categories_blp)

    db_url = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from app.models import db
    from flask_migrate import Migrate

    db.init_app(app)
    Migrate(app, db)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)