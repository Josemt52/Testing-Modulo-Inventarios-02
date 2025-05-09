// src/components/Productos.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './Productos.css';

const Productos = () => {
  const [productos, setProductos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/productos')
      .then(response => {
        setProductos(response.data);
        setLoading(false);
      })
      .catch(err => {
        setError('Error al obtener los productos');
        setLoading(false);
      });
  }, []);

  if (loading) return <p className="loading">Cargando productos...</p>;
  if (error) return <p className="error">{error}</p>;

  return (
    <div className="productos-container">
      <h2>Lista de Productos</h2>
      <table className="productos-table">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Cantidad</th>
            <th>Precio</th>
          </tr>
        </thead>
        <tbody>
          {productos.map((producto) => (
            <tr key={producto.id}>
              <td>{producto.nombre}</td>
              <td>{producto.stock_actual}</td>
              <td>${producto.precio}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Productos;
