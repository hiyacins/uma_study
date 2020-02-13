# MySQLの接続と切断

import mysql.connector
from flask import current_app, g


def get_db():
    """DBへの接続"""
    if 'db' not in g:
        g.db = mysql.connector.connect(current_app.config['DATABASE'],
                                       detect_types=mysql.PARSE_DECLTYPES)

        # 列に名前でアクセスできるようにする
        g.db.row_factory = mysql.Row

    return g.db


def close_db(e=None):
    """DBの切断"""
    db = g.pop('db', None)

    if db is not None:
        db.close()
