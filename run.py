from app import create_app,db
from flask_migrate import Migrate
from config import Config

app = create_app(Config)
migrate = Migrate(app,db)

def init_db():
    from app.models import User
    db.create_all(app=create_app(Config))

if __name__ == '__main__':
    app.run()