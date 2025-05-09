from flask import Blueprint, request, jsonify
from database import get_db_connection

producto_routes = Blueprint('producto_routes', __name__)
categoria_routes = Blueprint('categoria_routes', __name__)
marca_routes = Blueprint('marca_routes', __name__)
movimiento_routes = Blueprint('movimiento_routes', __name__)
almacen_routes = Blueprint('almacen_routes', __name__)

# CRUD de productos
@producto_routes.route('/producto', methods=['POST'])
def crear_producto():
    data = request.get_json()
    # Validar campos obligatorios
    required_fields = ['nombre', 'categoria_id', 'marca_id', 'precio', 'stock_actual', 'stock_minimo', 'activo']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Falta el dato obligatorio: {field}'}), 400

    # Insertar producto
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO productos (nombre, categoria_id, marca_id, precio, stock_actual, stock_minimo, activo)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, tuple(data[field] for field in required_fields))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'Producto creado exitosamente'}), 201


@producto_routes.route('/productos', methods=['GET'])
def listar_productos():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.id, p.nombre, c.nombre AS categoria, m.nombre AS marca, p.precio, p.stock_actual, p.activo
        FROM productos p
        JOIN categorias c ON p.categoria_id = c.id
        JOIN marcas m ON p.marca_id = m.id
        WHERE p.activo = 1
    """)
    productos = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(productos)


@producto_routes.route('/producto/<int:id>', methods=['GET'])
def obtener_producto(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.id, p.nombre, c.nombre AS categoria, m.nombre AS marca, p.precio, p.stock_actual, p.activo
        FROM productos p
        JOIN categorias c ON p.categoria_id = c.id
        JOIN marcas m ON p.marca_id = m.id
        WHERE p.id = %s AND p.activo = 1
    """, (id,))
    producto = cursor.fetchone()
    cursor.close()
    connection.close()

    if producto:
        return jsonify(producto)
    else:
        return jsonify({'message': 'Producto no encontrado'}), 404


@producto_routes.route('/producto/<int:id>', methods=['PUT'])
def editar_producto(id):
    data = request.get_json()

    if 'stock_actual' not in data:
        return jsonify({'message': 'Falta el dato obligatorio: stock_actual'}), 400

    try:
        stock_actual = int(data['stock_actual'])
    except ValueError:
        return jsonify({'message': 'El valor de stock_actual debe ser un número entero'}), 400

    if stock_actual < 0:
        return jsonify({'message': 'El valor de stock_actual debe ser mayor o igual a 0'}), 400
    
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM productos WHERE id = %s AND activo = 1", (id,))
    producto = cursor.fetchone()

    if not producto:
        return jsonify({'message': 'Producto no encontrado o desactivado'}), 404

    cursor.execute("UPDATE productos SET stock_actual = %s WHERE id = %s", (stock_actual, id))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'Stock actual actualizado exitosamente'}), 200


@producto_routes.route('/producto/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM productos WHERE id = %s AND activo = 1", (id,))
    producto = cursor.fetchone()

    if not producto:
        return jsonify({'message': 'Producto no encontrado o ya desactivado'}), 404

    cursor.execute("UPDATE productos SET activo = 0 WHERE id = %s", (id,))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'Producto desactivado exitosamente'}), 200


# CRUD de categorías
@categoria_routes.route('/categoria', methods=['POST'])
def crear_categoria():
    nombre = request.get_json().get('nombre')
    if not nombre:
        return jsonify({'message': 'El nombre es obligatorio'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO categorias (nombre) VALUES (%s)", (nombre,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'Categoría creada exitosamente'}), 201


@categoria_routes.route('/categorias', methods=['GET'])
def listar_categorias():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre FROM categorias WHERE activo=1")
    categorias = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(categorias)


@categoria_routes.route('/categoria/<int:id>', methods=['GET'])
def obtener_categoria(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre FROM categorias WHERE id = %s", (id,))
    categoria = cursor.fetchone()
    cursor.close()
    connection.close()

    if categoria:
        return jsonify(categoria)
    else:
        return jsonify({'message': 'Categoría no encontrada'}), 404


@categoria_routes.route('/categoria/<int:id>', methods=['DELETE'])
def eliminar_categoria(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE categorias SET activo = 0 WHERE id = %s", (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'Categoría desactivada exitosamente'}), 200


# CRUD de marcas
@marca_routes.route('/marca', methods=['POST'])
def crear_marca():
    nombre = request.get_json().get('nombre')
    if not nombre:
        return jsonify({'message': 'El nombre es obligatorio'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO marcas (nombre) VALUES (%s)", (nombre,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'Marca creada exitosamente'}), 201


@marca_routes.route('/marcas', methods=['GET'])
def listar_marcas():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre FROM marcas WHERE activo=1")
    marcas = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(marcas)


@marca_routes.route('/marca/<int:id>', methods=['GET'])
def obtener_marca(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre FROM marcas WHERE id = %s", (id,))
    marca = cursor.fetchone()
    cursor.close()
    connection.close()

    if marca:
        return jsonify(marca)
    else:
        return jsonify({'message': 'Marca no encontrada'}), 404


@marca_routes.route('/marca/<int:id>', methods=['DELETE'])
def eliminar_marca(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE marcas SET activo = 0 WHERE id = %s", (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'Marca desactivada exitosamente'}), 200


# CRUD de movimientos
@movimiento_routes.route('/movimiento', methods=['POST'])
def crear_movimiento():
    data = request.get_json()
    required_fields = ['producto_id', 'tipo', 'cantidad', 'fecha']
    
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Falta el dato obligatorio: {field}'}), 400
    
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO movimientos (producto_id, tipo, cantidad, fecha)
        VALUES (%s, %s, %s, %s)
    """, tuple(data[field] for field in required_fields))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'Movimiento registrado exitosamente'}), 201


@movimiento_routes.route('/movimiento/<int:id>', methods=['GET'])
def obtener_movimiento(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM movimientos WHERE id = %s", (id,))
    movimiento = cursor.fetchone()
    cursor.close()
    connection.close()

    if movimiento:
        return jsonify(movimiento)
    else:
        return jsonify({'message': 'Movimiento no encontrado'}), 404


@movimiento_routes.route('/movimiento/<int:id>', methods=['DELETE'])
def eliminar_movimiento(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM movimientos WHERE id = %s", (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'Movimiento eliminado exitosamente'}), 200


# CRUD de almacenes
@almacen_routes.route('/almacen', methods=['POST'])
def crear_almacen():
    data = request.get_json()
    
    nombre = data.get('nombre')
    ubicacion = data.get('ubicacion')
    if not nombre:
        return jsonify({'message': 'El nombre es obligatorio'}), 400
    if not ubicacion:
        return jsonify({'message': 'La ubicación es obligatoria'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO almacenes (nombre, ubicacion) VALUES (%s, %s)", (nombre, ubicacion))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'Almacén creado exitosamente'}), 201


@almacen_routes.route('/almacenes', methods=['GET'])
def listar_almacenes():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre, ubicacion FROM almacenes")
    almacenes = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(almacenes)


@almacen_routes.route('/almacen/<int:id>', methods=['GET'])
def obtener_almacen(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre, ubicacion FROM almacenes WHERE id = %s", (id,))
    almacen = cursor.fetchone()
    cursor.close()
    connection.close()

    if almacen:
        return jsonify(almacen)
    else:
        return jsonify({'message': 'Almacén no encontrado'}), 404


@almacen_routes.route('/almacen/<int:id>', methods=['DELETE'])
def eliminar_almacen(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM almacenes WHERE id = %s", (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'Almacén eliminado exitosamente'}), 200
