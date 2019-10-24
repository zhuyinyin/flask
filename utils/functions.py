import os
from flask import Flask
# 用户登录蓝图
from user.views import userlogin_bpt
from user.models import db


def create_app():
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(BASE_DIR, 'static')
    templates_dir = os.path.join(BASE_DIR, 'templates')

    app = Flask(__name__,
                static_folder=static_dir,
                template_folder=templates_dir)
    # 注册用户登录蓝图
    app.register_blueprint(blueprint=userlogin_bpt, url_prefix='/user')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:123456@127.0.0.1:3306/flaskdemo2'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 设置session密钥
    app.config['SECRET_KEY'] = 'secret_key'

    db.init_app(app=app)

    with app.app_context():
        db.create_all()

    return app
