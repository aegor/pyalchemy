from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from safrs import SAFRSAPI
from models import *
from flasgger import Swagger


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///desserts.db'
db = SQLAlchemy(app)
swagger = Swagger(app)

def create_api(app, HOST='localhost:5000', PORT=5000, API_PREFIX='/api'):
    api = SAFRSAPI(app, host=HOST, port=PORT, prefix=API_PREFIX)
    api.expose_object(Dessert)
    api.expose_object(Menu)
    d1 = Dessert(name='dessert1', price=50, calories=2000)
    d2 = Dessert(name='dessert2', price=60, calories=3000)
    m1 = Menu(name="menu1")
    m2 = Menu(name="menu2")
    print('Starting API: http://{}:{}/{}'.format(HOST,PORT,API_PREFIX))

if __name__ == "__main__":

    # We need to make sure Flask knows about its views before we run
    # the app, so we import them. We could do it earlier, but there's
    # a risk that we may run into circular dependencies, so we do it at the
    # last minute here.

    from views import *

    with app.app_context():
        create_api(app)
    app.run(debug=True)
