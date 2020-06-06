from flask import Flask, render_template
# from flask_restful import Api, Resource
# from models import get_all, init_db, insert

app = Flask(__name__, static_folder='../frontend/dist/static',
            template_folder='../frontend/dist')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myspa.db'
# api = Api(app)


# class Spam(Resource):
#     def get(self):
#         return [{'id': x.pk, 'name': x.name, 'note': x.note} for x in get_all()]


# api.add_resource(Spam, '/api/spam')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')


if __name__ == '__main__':
    # with app.app_context():
    #     init_db(app)
    #     if not get_all():
    #         insert('foo', 'This is foo.')
    #         insert('bar', 'This is bar.')
    app.run()
