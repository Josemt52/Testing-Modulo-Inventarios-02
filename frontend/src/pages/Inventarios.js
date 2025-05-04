import React, { useEffect, useState } from 'react';

function Inventarios() {
  const [productos, setProductos] = useState([]);
  const [movimientos, setMovimientos] = useState([]);
  const [productoId, setProductoId] = useState('');
  const [cantidad, setCantidad] = useState('');
  const [tipo, setTipo] = useState('entrada');
  const [message, setMessage] = useState('');

  // Fetch productos and movimientos from the backend
  useEffect(() => {
    fetch('http://localhost:8000/inventario/movimientos') // Endpoint para listar movimientos
      .then((response) => response.json())
      .then((data) => {
        console.log('Movimientos:', data); // Verifica si es un array
        setMovimientos(data);
      })
      .catch((error) => console.error('Error fetching movimientos:', error));

    fetch('http://localhost:8000/productos') // Endpoint para listar productos
      .then((response) => response.json())
      .then((data) => setProductos(data))
      .catch((error) => console.error('Error fetching productos:', error));
  }, []);

  // Handle form submission to register a movimiento
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!productoId || !cantidad || !tipo) {
      setMessage('Por favor, complete todos los campos');
      return;
    }

    const movimiento = {
      producto_id: parseInt(productoId),
      cantidad: parseInt(cantidad),
      tipo, 
      almacen_id: null, // Opcional
      origen: '', // Opcional
      observaciones: '', // Opcional
    };
    console.log('Datos enviados:', movimiento);

    // Determinar el endpoint según el tipo de movimiento
    const endpoint =
      tipo === 'entrada'
        ? 'http://localhost:8000/inventario/entrada'
        : 'http://localhost:8000/inventario/salida';

        fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(movimiento),
        })
        
          .then((response) => {
            console.log('Datos enviados:', movimiento);
            if (!response.ok) {
              return response.json().then((error) => {
                // Procesar el error para mostrar un mensaje legible
                const errorMessage =
                  typeof error.detail === 'string'
                    ? error.detail
                    : Array.isArray(error.detail)
                    ? error.detail.map((err) => err.msg || JSON.stringify(err)).join(', ')
                    : 'Error desconocido';
                throw new Error(errorMessage);
              });
            }
            return response.json();
          })
          .then((data) => {
            setMessage('Movimiento registrado con éxito');
            setMovimientos([...movimientos, data]);
          })
          .catch((error) => {
            console.error('Error registrando movimiento:', error);  
            setMessage(error.message);
          });
  };

  return (
    <div>
      <h1>Módulo de Inventarios</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Producto:</label>
          <select
            value={productoId}
            onChange={(e) => setProductoId(e.target.value)}
            required
          >
            <option value="">Seleccione un producto</option>
            {productos.map((producto) => (
              <option key={producto.id} value={producto.id}>
                {producto.nombre}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label>Cantidad:</label>
          <input
            type="number"
            value={cantidad}
            onChange={(e) => setCantidad(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Tipo:</label>
          <select value={tipo} onChange={(e) => setTipo(e.target.value)}>
            <option value="entrada">Entrada</option>
            <option value="salida">Salida</option>
          </select>
        </div>
        <button type="submit">Registrar Movimiento</button>
      </form>
      <p>{message}</p>
      <h2>Movimientos Registrados</h2>
      <ul>
        {Array.isArray(movimientos) &&
          movimientos.map((movimiento) => (
            <li key={movimiento.id}>
              Producto: {movimiento.producto_id}, Cantidad: {movimiento.cantidad}, Tipo: {movimiento.tipo}
            </li>
          ))}
      </ul>
    </div>
  );
}

export default Inventarios;