from frogblog.config import Config
from frogblog import create_app

app = create_app(Config)

def init_db():
    from frogblog.models import User,Category,Tag,Article,Category
    db.create_all(app=create_app(Config))
    
if __name__ == '__main__':
    app.run()