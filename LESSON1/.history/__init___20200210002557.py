import os
from flask import Flask

app = Flask(__name__)
app.config.from_mapping(SECRET_KEY='dev',
                        DATABASE=os.path.join(app.instance_path,
                                              'site_master.db'))

# アプリケーションコンテキストが終了したときに
# 毎回DBを切断する
from .db import close_db
app.teardown_appcontext(close_db)

# インデックスページの読み込み
import flask_login_site.views

# ログイン機能の追加
import flask_login_site.auth
app.register_blueprint(auth.bp)
