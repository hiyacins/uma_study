from HiyaLib import *
import unittest

# app = FlaskBuilder(__name__)
app = Flask(__name__, static_folder='../frontend/dist/static',
            template_folder='../frontend/dist')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')


if __name__ == "__main__":
    app.run(port=5000, debug=True)
    # app.run(host="0.0.0.0", port=80, debug=False)
    # unittest.main()
