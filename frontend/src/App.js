import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Productos from './pages/Productos';
import Inventarios from './pages/Inventarios';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
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
            </ul>
          </nav>
        </header>
        <main>
          <Routes>
            <Route path="/productos" element={<Productos />} />
            <Route path="/inventarios" element={<Inventarios />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;