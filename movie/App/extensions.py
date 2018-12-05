from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cache import Cache
from flask_migrate import Migrate
from  flask_moment import Moment
from flask_uploads import UploadSet,configure_uploads,patch_request_class,IMAGES

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
migrate = Migrate(db=db)
login_manager = LoginManager()
cache = Cache(config={'CACHE_TYPE':'redis'})

file = UploadSet('photos',IMAGES)


def ext_init(app):
    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    migrate.init_app(app)
    cache.init_app(app)
    configure_uploads(app, file)
    patch_request_class(app, None)


    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    login_manager.login_message = '先登录再访问'
    login_manager.session_protection = 'strong'