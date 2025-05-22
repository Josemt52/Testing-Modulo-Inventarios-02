import React, { useState, useEffect } from 'react';
import { 
  obtenerProductos, 
  editarProducto, 
  eliminarProducto, 
  crearProducto, 
  obtenerCategorias,
  eliminarCategoria, 
  obtenerMarcas, 
  crearMarca, 
  eliminarMarca,
  crearCategoria,
  obtenerAlmacenes,
  crearAlmacen,
  eliminarAlmacen,
  obtenerMovimientos,
  crearMovimiento,
  eliminarMovimiento
} from './api';

import './App.css';

function App() {
  // Estados para productos
  const [productos, setProductos] = useState([]);
  const [nuevoProducto, setNuevoProducto] = useState({
    nombre: '',
    categoria_id: '',
    marca_id: '',
    precio: '',
    stock_actual: '',
    stock_minimo: '',
    activo: true
  });
  const [categorias, setCategorias] = useState([]);
  const [marcas, setMarcas] = useState([]);
  const [editandoId, setEditandoId] = useState(null);
  const [productoEditado, setProductoEditado] = useState({
    stock_actual: ''
  });
  
  // Estados para categorías
  const [nuevaCategoria, setNuevaCategoria] = useState('');

  // Estados para marcas
  const [nuevaMarca, setNuevaMarca] = useState('');

  // Cargar datos al inicio
  useEffect(() => {
    async function fetchData() {
      const productosData = await obtenerProductos();
      const categoriasData = await obtenerCategorias();
      const marcasData = await obtenerMarcas();
      setProductos(productosData || []);
      setCategorias(categoriasData || []);
      setMarcas(marcasData || []);
    }
    fetchData();
  }, []);


  const [almacenes, setAlmacenes] = useState([]);
  const [nuevoAlmacen, setNuevoAlmacen] = useState({ nombre: '', ubicacion: '' });

  const [movimientos, setMovimientos] = useState([]);
  const [nuevoMovimiento, setNuevoMovimiento] = useState({
    almacen_id: '',
    tipo: '',
    descripcion: '',
    cantidad: 0,
    fecha: ''
  });

  useEffect(() => {
    cargarAlmacenes();
    cargarMovimientos();
  }, []);

  const cargarAlmacenes = async () => {
    const datos = await obtenerAlmacenes();
    setAlmacenes(datos);
  };

  const cargarMovimientos = async () => {
    const datos = await obtenerMovimientos();
    setMovimientos(datos);
  };

  const handleChangeAlmacen = (e) => {
    setNuevoAlmacen({ ...nuevoAlmacen, [e.target.name]: e.target.value });
  };

  const handleSubmitAlmacen = async (e) => {
    e.preventDefault();
    await crearAlmacen(nuevoAlmacen);
    setNuevoAlmacen({ nombre: '', direccion: '' });
    cargarAlmacenes();
  };

  const handleDeleteAlmacen = async (id) => {
    await eliminarAlmacen(id);
    setAlmacenes(almacenes.filter(a => a.id !== id));
  };

  const handleChangeMovimiento = (e) => {
    setNuevoMovimiento({ ...nuevoMovimiento, [e.target.name]: e.target.value });
  };

  const handleSubmitMovimiento = async (e) => {
    e.preventDefault();
    await crearMovimiento(nuevoMovimiento);
    setNuevoMovimiento({
      almacen_id: '',
      tipo: '',
      descripcion: '',
      cantidad: 0,
      fecha: ''
    });
    cargarMovimientos();
  };

  // Manejar cambios en los formularios de productos
  const handleChangeProducto = (e) => {
    const { name, value } = e.target;
    setNuevoProducto(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmitProducto = async (e) => {
    e.preventDefault();
    const result = await crearProducto(nuevoProducto);
    if (result.message === 'Producto creado exitosamente') {
      const productosData = await obtenerProductos();
      setProductos(productosData);
      setNuevoProducto({
        nombre: '',
        categoria_id: '',
        marca_id: '',
        precio: '',
        stock_actual: '',
        stock_minimo: '',
        activo: true
      });
    }
  };

  const handleDeleteProducto = async (id) => {
    const result = await eliminarProducto(id);
    if (result.message === 'Producto desactivado exitosamente') {
      setProductos(productos.filter(producto => producto.id !== id));
    }
  };

  const handleEditClickProducto = (producto) => {
    setEditandoId(producto.id);
    setProductoEditado({
      stock_actual: producto.stock_actual
    });
  };

  const handleEditChangeProducto = (e) => {
    const { name, value } = e.target;
    setProductoEditado(prev => ({ ...prev, [name]: value }));
  };

  const handleEditSaveProducto = async (id) => {
    const productoActualizado = {
      stock_actual: productoEditado.stock_actual
    };
    const result = await editarProducto(id, productoActualizado);
    if (result.message === 'Producto actualizado exitosamente') {
      const productosData = await obtenerProductos();
      setProductos(productosData);
      setEditandoId(null);
      setProductoEditado({ stock_actual: '' });
    } else {
      console.error("Error al actualizar el producto:", result.message);
    }
  };

  const handleCancelEditProducto = () => {
    setEditandoId(null);
    setProductoEditado({ stock_actual: '' });
  };

  // Manejar cambios en los formularios de categorías
  const handleChangeCategoria = (e) => {
    setNuevaCategoria(e.target.value);
  };

  const handleDeleteCategoria = async (id) => {
  const result = await eliminarCategoria(id);
  if (result.message === 'Categoría desactivada exitosamente') {
    // Actualizar la categoría para marcarla como inactiva en el estado
    setCategorias(categorias.map(categoria =>
      categoria.id === id ? { ...categoria, activo: false } : categoria
    ));

    // Opcional: Desasociar productos que tienen esa categoría (si se desea)
    const productosData = await obtenerProductos();
    setProductos(productosData.map(producto => {
      if (producto.categoria_id === id) {
        // Desasociar el producto de la categoría desactivada
        return { ...producto, categoria_id: null };
      }
      return producto;
    }));
  }
};



  const handleSubmitCategoria = async (e) => {
    e.preventDefault();
    const result = await crearCategoria({ nombre: nuevaCategoria });
    if (result.message === 'Categoría creada exitosamente') {
      const categoriasData = await obtenerCategorias();
      setCategorias(categoriasData);
      setNuevaCategoria('');
    }
  };

  // Manejar cambios en los formularios de marcas
  const handleChangeMarca = (e) => {
    setNuevaMarca(e.target.value);
  };

  const handleSubmitMarca = async (e) => {
    e.preventDefault();
    const result = await crearMarca({ nombre: nuevaMarca });
    if (result.message === 'Marca creada exitosamente') {
      const marcasData = await obtenerMarcas();
      setMarcas(marcasData);
      setNuevaMarca('');
    }
  };

  const handleDeleteMarca = async (id) => {
    const result = await eliminarMarca(id);
    if (result.message === 'Marca eliminada exitosamente') {
      setMarcas(marcas.filter(marca => marca.id !== id));
    }
  };

  return (
    <div className="App">
      <h1>Gestión de Inventario</h1>

      {/* Formulario para ingresar nuevo producto */}
      <form onSubmit={handleSubmitProducto} className="form-container">
        <input type="text" name="nombre" value={nuevoProducto.nombre} onChange={handleChangeProducto} placeholder="Nombre" required />
        <select name="categoria_id" value={nuevoProducto.categoria_id} onChange={handleChangeProducto} required>
          <option value="">Categoría</option>
          {(categorias || []).map(cat => (
            <option key={cat.id} value={cat.id}>{cat.nombre}</option>
          ))}
        </select>
        <select name="marca_id" value={nuevoProducto.marca_id} onChange={handleChangeProducto} required>
          <option value="">Marca</option>
          {(marcas || []).map(m => (
            <option key={m.id} value={m.id}>{m.nombre}</option>
          ))}
        </select>
        <input type="number" name="precio" value={nuevoProducto.precio} onChange={handleChangeProducto} placeholder="Precio" required />
        <input type="number" name="stock_actual" value={nuevoProducto.stock_actual} onChange={handleChangeProducto} placeholder="Stock" required />
        <input type="number" name="stock_minimo" value={nuevoProducto.stock_minimo} onChange={handleChangeProducto} placeholder="Stock mínimo" required />
        <button type="submit">Agregar Producto</button>
      </form>

      {/* Tabla de productos */}
      <table>
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Categoría</th>
            <th>Marca</th>
            <th>Precio</th>
            <th>Stock</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {(productos || []).map(producto => (
            <tr key={producto.id}>
              {editandoId === producto.id ? (
                <>
                  <td>{producto.nombre}</td>
                  <td>{producto.categoria}</td>
                  <td>{producto.marca}</td>
                  <td>{producto.precio}</td>
                  <td>
                    <input
                      type="number"
                      name="stock_actual"
                      value={productoEditado.stock_actual}
                      onChange={handleEditChangeProducto}
                    />
                  </td>
                  <td>
                    <button onClick={() => handleEditSaveProducto(producto.id)}>Guardar</button>
                    <button onClick={handleCancelEditProducto}>Cancelar</button>
                  </td>
                </>
              ) : (
                <>
                  <td>{producto.nombre}</td>
                  <td>{producto.categoria}</td>
                  <td>{producto.marca}</td>
                  <td>{producto.precio}</td>
                  <td>{producto.stock_actual}</td>
                  <td>
                    <button onClick={() => handleEditClickProducto(producto)}>Editar</button>
                    <button onClick={() => handleDeleteProducto(producto.id)}>Eliminar</button>
                  </td>
                </>
              )}
            </tr>
          ))}
        </tbody>
      </table>

      <h1>Gestión de Categorías</h1>

      {/* Formulario para ingresar nueva categoría */}
      <form onSubmit={handleSubmitCategoria} className="form-container">
        <input
          type="text"
          value={nuevaCategoria}
          onChange={handleChangeCategoria}
          placeholder="Nueva Categoría"
          required
        />
        <button type="submit">Agregar Categoría</button>
      </form>

      {/* Tabla de categorías */}
      <table>
        <thead>
          <tr>
            <th>Categoría</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {(categorias || []).map((categoria) => (
            <tr key={categoria.id}>
              <td>{categoria.nombre}</td>
              <td>
                <button onClick={() => handleDeleteCategoria (categoria.id)}>Eliminar</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <h1>Gestión de Marcas</h1>

      {/* Formulario para ingresar nueva marca */}
      <form onSubmit={handleSubmitMarca} className="form-container">
        <input
          type="text"
          value={nuevaMarca}
          onChange={handleChangeMarca}
          placeholder="Nueva Marca"
          required
        />
        <button type="submit">Agregar Marca</button>
      </form>

      {/* Tabla de marcas */}
      <table>
        <thead>
          <tr>
            <th>Marca</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {(marcas || []).map((marca) => (
            <tr key={marca.id}>
              <td>{marca.nombre}</td>
              <td>
                <button onClick={() => handleDeleteMarca(marca.id)}>Eliminar</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <h1>Gestión de Almacenes</h1>

      {/* Formulario para ingresar nuevo almacen */}
      <form onSubmit={handleSubmitAlmacen} className="form-container">
        <input type="text" name="nombre" value={nuevoAlmacen.nombre} onChange={handleChangeAlmacen} placeholder="Nombre" required />
        <input type="text" name="ubicacion" value={nuevoAlmacen.ubicacion} onChange={handleChangeAlmacen} placeholder="Ubicacion" required />
        <button type="submit">Agregar Almacen</button>
      </form>
      {/* Tabla de Almacenes */}
      <table>
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Ubicacion</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {(almacenes || []).map((almacenes) => (
            <tr key={almacenes.id}>
              <td>{almacenes.nombre}</td>
              <td>{almacenes.ubicacion}</td>
              <td>
                <button onClick={() => handleDeleteAlmacen(almacenes.id)}>Eliminar</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
