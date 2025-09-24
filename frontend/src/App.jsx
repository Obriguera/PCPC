import { useState } from "react";

const API_BASE_URL = "http://127.0.0.1:8000";

function App() {
  const [necesidades, setNecesidades] = useState("");
  const [presupuesto, setPresupuesto] = useState("");
  const [recomendacion, setRecomendacion] = useState(null);
  const [notebooks, setNotebooks] = useState([]);
  const [loading, setLoading] = useState(false);

  // --- Enviar necesidades a la IA ---
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setRecomendacion(null);

    const body = {
      necesidades,
      presupuesto_max: presupuesto ? parseInt(presupuesto) : null,
    };

    try {
      const response = await fetch(`${API_BASE_URL}/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      if (!response.ok) throw new Error(`Error: ${response.status}`);
      const data = await response.json();
      setRecomendacion(data);
    } catch (err) {
      setRecomendacion({ recomendacion: `⚠️ Error: ${err.message}` });
    } finally {
      setLoading(false);
    }
  };

  // --- Cargar notebooks ---
  const loadNotebooks = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/productos`);
      if (!response.ok) throw new Error(`Error: ${response.status}`);
      const data = await response.json();
      setNotebooks(data);
    } catch (err) {
      setNotebooks([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Recomendador de Notebooks 💻</h1>

      {/* --- Formulario para la IA --- */}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="¿Para qué necesitas la notebook?"
          value={necesidades}
          onChange={(e) => setNecesidades(e.target.value)}
          required
        />
        <input
          type="number"
          placeholder="Presupuesto máximo (opcional)"
          value={presupuesto}
          onChange={(e) => setPresupuesto(e.target.value)}
        />
        <button type="submit" disabled={loading}>
          {loading ? "Buscando..." : "Obtener recomendación"}
        </button>
      </form>

      {/* --- Respuesta de la IA --- */}
      {recomendacion && (
        <div style={{ marginTop: "1rem" }}>
          <p><strong>IA dice:</strong> {recomendacion.recomendacion}</p>
          {recomendacion.producto_sugerido && (
            <div style={{ border: "1px solid #ccc", padding: "1rem", marginTop: "0.5rem" }}>
              <h3>{recomendacion.producto_sugerido.nombre}</h3>
              <p>💲 {recomendacion.producto_sugerido.precio}</p>
              <p>Fuente: {recomendacion.producto_sugerido.fuente || "Desconocida"}</p>
            </div>
          )}
        </div>
      )}

      {/* --- Lista de Notebooks --- */}
      <div style={{ marginTop: "2rem" }}>
        <button onClick={loadNotebooks} disabled={loading}>
          {loading ? "Cargando..." : "Ver todas las notebooks"}
        </button>

        {notebooks.length > 0 && (
          <div style={{ marginTop: "1rem" }}>
            {notebooks.map((nb, i) => (
              <div key={i} style={{ border: "1px solid #eee", padding: "1rem", margin: "0.5rem 0" }}>
                <h3>{nb.nombre}</h3>
                <p>💲 {nb.precio}</p>
                <p>Fuente: {nb.fuente || "Desconocida"}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
