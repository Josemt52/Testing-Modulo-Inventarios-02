// api.js
import axios from 'axios';

const apiUrl = 'http://localhost:8000'; // Asegúrate de que este sea el URL correcto de tu backend

// Función para editar un producto
export const editarProducto = async (id, producto) => {
  try {
    const response = await axios.put(`${apiUrl}/producto/${id}`, producto); // Cambiar a axios.put
    return response.data; // Retorna la respuesta directamente
  } catch (error) {
    console.error("Error al editar el producto:", error);
    return { message: "Error al editar el producto" };
  }
};

// Función para obtener un producto por su ID
export const obtenerProductoPorId = async (id) => {
  try {
    const response = await axios.get(`${apiUrl}/productos/${id}`);
    return response.data;
  } catch (error) {
    console.error('Error al obtener el producto:', error);
    return null;
  }
};

// Función para obtener productos
export const obtenerProductos = async () => {
  try {
    const response = await axios.get(`${apiUrl}/productos`);
    return response.data;
  } catch (error) {
    console.error("Error al obtener productos", error);
  }
};

// Función para obtener categorías
export const obtenerCategorias = async () => {
  try {
    const response = await axios.get(`${apiUrl}/categorias`);
    return response.data;
  } catch (error) {
    console.error("Error al obtener categorías", error);
  }
};

// Función para obtener marcas
export const obtenerMarcas = async () => {
  try {
    const response = await axios.get(`${apiUrl}/marcas`);
    return response.data;
  } catch (error) {
    console.error("Error al obtener marcas", error);
  }
};

// Función para crear una nueva marca
export const crearMarca = async (marca) => {
  try {
    const response = await axios.post(`${apiUrl}/marca`, marca);
    return response.data;
  } catch (error) {
    console.error("Error al crear marca", error);
    throw error.response?.data || { message: 'Error desconocido' };
  }
};

// Función para eliminar una marca
export const eliminarMarca = async (id) => {
  try {
    const response = await fetch(`${apiUrl}/marca/${id}`, {
      method: 'DELETE',
    });
    const result = await response.json();
    return result;
  } catch (error) {
    console.error('Error al eliminar marca:', error);
    return { message: 'Error al eliminar marca' };
  }
};

// Función para crear un nuevo producto
export const crear_producto = async (producto) => {
  try {
    const response = await axios.post(`${apiUrl}/producto`, producto); 
    return response.data;
  } catch (error) {
    console.error("Error al crear producto", error);
    throw error.response?.data || { message: 'Error desconocido' };
  }
};

// Función para eliminar un producto
export const eliminarProducto = async (id) => {
  try {
    const response = await axios.delete(`${apiUrl}/producto/${id}`);
    return response.data;
  } catch (error) {
    console.error('Error al eliminar producto:', error);
    return { message: 'Error al eliminar producto' };
  }
};

// Función para crear una nueva categoría
export const crearCategoria = async (categoria) => {
  try {
    const response = await axios.post(`${apiUrl}/categoria`, categoria); // Agregar categoría con POST
    return response.data;
  } catch (error) {
    console.error("Error al crear categoría", error);
    throw error.response?.data || { message: 'Error desconocido' };
  }
};

// Función para eliminar una categoría
export const eliminarCategoria = async (id) => {
  try {
    const response = await fetch(`/api/categorias/${id}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      throw new Error('Error al eliminar la categoría');
    }

    const result = await response.json();
    return result; // El servidor debe devolver un mensaje de éxito
  } catch (error) {
    console.error(error);
    return { message: 'Error al eliminar la categoría' };
  }
};

export const obtenerAlmacenes = async () => {
  try {
    const response = await axios.get(`${apiUrl}/almacenes`);
    return response.data;
  } catch (error) {
    console.error("Error al obtener almacenes", error);
  }
};

// Crear un nuevo almacén
export const crearAlmacen = async (almacen) => {
  try {
    const response = await axios.post(`${apiUrl}/almacen`, almacen);
    return response.data;
  } catch (error) {
    console.error("Error al crear almacén", error);
    throw error.response?.data || { message: 'Error desconocido' };
  }
};

// Eliminar un almacén
export const eliminarAlmacen = async (id) => {
  try {
    const response = await axios.delete(`${apiUrl}/almacen/${id}`);
    return response.data;
  } catch (error) {
    console.error('Error al eliminar almacén:', error);
    return { message: 'Error al eliminar almacén' };
  }
};

export const obtenerMovimientos = async () => {
  try {
    const response = await axios.get(`${apiUrl}/movimientos`);
    return response.data;
  } catch (error) {
    console.error("Error al obtener movimientos", error);
  }
};

// Crear un nuevo movimiento
export const crearMovimiento = async (movimiento) => {
  try {
    const response = await axios.post(`${apiUrl}/movimiento`, movimiento);
    return response.data;
  } catch (error) {
    console.error("Error al crear movimiento", error);
    throw error.response?.data || { message: 'Error desconocido' };
  }
};

// Eliminar un movimiento
export const eliminarMovimiento = async (id) => {
  try {
    const response = await axios.delete(`${apiUrl}/movimiento/${id}`);
    return response.data;
  } catch (error) {
    console.error('Error al eliminar movimiento:', error);
    return { message: 'Error al eliminar movimiento' };
  }
};

