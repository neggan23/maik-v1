function enviarPregunta() {
    const pregunta = document.getElementById('pregunta').value;

    fetch('/preguntar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ mensaje: pregunta }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('respuesta').textContent = data.respuesta;
    });
}
