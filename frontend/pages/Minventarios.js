import React, { useEffect, useState } from 'react';

function Minventarios() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/test') // FastAPI endpoint
      .then((response) => response.json())
      .then((data) => setData(data.message))
      .catch((error) => console.error('Error fetching data:', error));
  }, []);

  return (
    <div>
      <h1>FastAPI Test</h1>
      <p>{data || 'Loading...'}</p>
    </div>
  );
}

export default Minventarios;

