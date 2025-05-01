import React, { useEffect, useState } from 'react';

function Productos() {
  const [productos, setProductos] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/productos') // Endpoint para listar productos
      .then((response) => response.json())
      .then((data) => setProductos(data))
      .catch((error) => console.error('Error fetching productos:', error));
  }, []);

  return (
    <div>
      <h1>Lista de Productos</h1>
      <ul>
        {productos.map((producto) => (
          <li key={producto.id}>
            {producto.nombre} - Stock: {producto.stock_actual}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Productos;