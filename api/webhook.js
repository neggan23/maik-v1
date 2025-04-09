// pages/api/webhook.js
import axios from 'axios';

export default async function handler(req, res) {
  if (req.method === 'POST') {
    const data = req.body;
    console.log("Mensaje recibido:", data);

    const mensaje = data?.message?.body?.toLowerCase() || '';
    const numero = data?.message?.from || '';

    // Respuesta automática
    if (mensaje.includes('maik')) {
      await axios.post('https://api.ultramsg.com/INSTANCE_ID/messages/chat', {
        token: 'TU_TOKEN',
        to: numero,
        body: 'Hola, soy Maik. Estoy activo y operativo, señor Yeis.',
      });
    }

    return res.status(200).json({ message: 'Mensaje recibido correctamente' });
  } else {
    return res.status(405).json({ error: 'Método no permitido' });
  }
}
