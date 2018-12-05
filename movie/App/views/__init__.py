from .main import main
from .user import user

blueprintConfig = [
    (main,''),
    (user,''),
]

def register_blueprint(app):
    for blueprint,prefix in blueprintConfig:
        app.register_blueprint(blueprint,url_prefix=prefix)