import React, {useState, useEffect} from 'react';
import { BrowserRouter as Router, Route, Routes, Link, Navigate } from 'react-router-dom';
import Productos from './pages/Productos';
import Inventarios from './pages/Inventarios';
import Login from './pages/Login.js';
import './App.css';

function App() {

  const [usuario, setUsuario] = useState(null);

  useEffect(() => {
    const usuarioGuardado = localStorage.getItem('usuario');
    if (usuarioGuardado) {
      setUsuario(JSON.parse(usuarioGuardado));
    }
  }, []);

  const handleLogin = (usuario) => {
    setUsuario(usuario);
    localStorage.setItem('usuario', JSON.stringify(usuario));
  };

  const handleLogout = () => {
    setUsuario(null);
    localStorage.removeItem('usuario');
  };

  const RutaProtegida = ({ children }) => {
    return usuario ? children : <Navigate to="/login" />;
  };

  return (
    <Router>
      <div className="App">
        {usuario && (
          <header className="App-header">
            <h1>Gestión de Inventarios</h1>
            <nav>
              <ul style={{ listStyle: 'none', padding: 0 }}>
                <li>
                  <Link to="/productos" style={{ color: 'white', textDecoration: 'none' }}>
                    Productos
                  </Link>
                </li>
                <li>
                  <Link to="/inventarios" style={{ color: 'white', textDecoration: 'none' }}>
                    Inventarios
                  </Link>
                </li>
                <li>
                  <button onClick={handleLogout}>Cerrar sesión</button>
                </li>
              </ul>
            </nav>
          </header>
        )}

        <main>
          <Routes>
            <Route
              path="/productos"
              element={
                <RutaProtegida>
                  <Productos />
                </RutaProtegida>
              }
            />
            <Route
              path="/inventarios"
              element={
                <RutaProtegida>
                  <Inventarios />
                </RutaProtegida>
              }
            />
            <Route path="/login" element={<Login onLogin={handleLogin} />} />
            <Route path="*" element={<Navigate to={usuario ? "/productos" : "/login"} />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;