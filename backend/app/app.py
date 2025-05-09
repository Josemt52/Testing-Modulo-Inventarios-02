from flask import Flask
from flask_cors import CORS
from database import init_db
from routes.routes import *

app = Flask(__name__)

CORS(app)

init_db(app)

app.register_blueprint(producto_routes)
app.register_blueprint(movimiento_routes)
app.register_blueprint(categoria_routes)
app.register_blueprint(marca_routes)
app.register_blueprint(almacen_routes)


if __name__ == "__main__":
    app.run(debug=True)
