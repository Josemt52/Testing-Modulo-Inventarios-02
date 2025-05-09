// src/components/AddProduct.js
import React, { useState } from 'react';
import { addProducto } from '../api';

const AddProduct = () => {
  const [nombre, setNombre] = useState('');
  const [cantidad, setCantidad] = useState('');
  const [precio, setPrecio] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newProduct = { nombre, cantidad, precio };

    try {
      await addProducto(newProduct);
      alert('Producto agregado correctamente');
      setNombre('');
      setCantidad('');
      setPrecio('');
    } catch (error) {
      console.error("Error al agregar el producto:", error);
      alert('Error al agregar el producto');
    }
  };

  return (
    <div className="add-product">
      <h2>Agregar Producto</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Nombre:</label>
          <input
            type="text"
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
            required
          />
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
          <label>Precio:</label>
          <input
            type="number"
            value={precio}
            onChange={(e) => setPrecio(e.target.value)}
            required
          />
        </div>
        <button type="submit">Agregar Producto</button>
      </form>
    </div>
  );
};

export default AddProduct;
