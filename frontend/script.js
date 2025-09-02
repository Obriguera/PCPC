document.addEventListener('DOMContentLoaded', () => {
    const aiForm = document.getElementById('ai-form');
    const submitButton = document.getElementById('submit-button');
    const aiResponseContainer = document.getElementById('ai-response-container');
    
    const notebookListContainer = document.getElementById('notebook-list');
    const loadNotebooksBtn = document.getElementById('load-notebooks-btn');

    const API_BASE_URL = 'http://127.0.0.1:8000';

    // Función para mostrar un loader
    const showLoader = (container) => {
        container.innerHTML = '<div class="loader"></div>';
    };

    // --- Lógica para el formulario de la IA ---
    aiForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        submitButton.disabled = true;
        showLoader(aiResponseContainer);

        const necesidades = document.getElementById('necesidades').value;
        const presupuesto = document.getElementById('presupuesto').value;

        const requestBody = {
            necesidades: necesidades,
            presupuesto_max: presupuesto ? parseInt(presupuesto, 10) : null,
        };

        try {
            const response = await fetch(`${API_BASE_URL}/search`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody),
            });

            if (!response.ok) {
                throw new Error(`Error del servidor: ${response.status}`);
            }

            const data = await response.json();
            displayAIResponse(data);

        } catch (error) {
            aiResponseContainer.innerHTML = `<p style="color: red;"><strong>Error:</strong> No se pudo obtener la recomendación. ¿Está el servidor corriendo? Detalles: ${error.message}</p>`;
        } finally {
            submitButton.disabled = false;
        }
    });

    const displayAIResponse = (data) => {
        aiResponseContainer.innerHTML = ''; // Limpiar loader

        const reasoning = document.createElement('p');
        reasoning.innerHTML = `<strong>Recomendación de la IA:</strong> ${data.recomendacion}`;
        aiResponseContainer.appendChild(reasoning);

        if (data.producto_sugerido) {
            aiResponseContainer.appendChild(createNotebookCard(data.producto_sugerido));
        }
    };
    
    // --- Lógica para cargar las notebooks de la DB ---
    loadNotebooksBtn.addEventListener('click', async () => {
        showLoader(notebookListContainer);
        loadNotebooksBtn.style.display = 'none';

        try {
            const response = await fetch(`${API_BASE_URL}/productos`);
            if (!response.ok) {
                throw new Error(`Error del servidor: ${response.status}`);
            }
            const notebooks = await response.json();
            displayNotebooks(notebooks);
        } catch (error) {
            notebookListContainer.innerHTML = `<p style="color: red;"><strong>Error:</strong> No se pudieron cargar las notebooks. Detalles: ${error.message}</p>`;
        }
    });

    const displayNotebooks = (notebooks) => {
        notebookListContainer.innerHTML = ''; // Limpiar loader
        if (notebooks.length === 0) {
            notebookListContainer.innerHTML = '<p>No hay notebooks en la base de datos.</p>';
            return;
        }
        notebooks.forEach(notebook => {
            notebookListContainer.appendChild(createNotebookCard(notebook));
        });
    };

    // Función para crear una tarjeta de notebook (reutilizable)
    const createNotebookCard = (notebook) => {
        const card = document.createElement('div');
        card.className = 'notebook-card';
        card.innerHTML = `
            <h3>${notebook.nombre}</h3>
            <p class="price">${notebook.precio}</p>
            <p class="source">Fuente: ${notebook.fuente || 'Desconocida'}</p>
        `;
        return card;
    };
});