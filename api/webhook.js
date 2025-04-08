export default async function handler(req, res) {
  if (req.method === 'POST') {
    const data = req.body;
    console.log("Mensaje recibido:", data);
    return res.status(200).json({ message: 'Mensaje recibido correctamente' });
  } else {
    return res.status(405).json({ error: 'Método no permitido' });
  }
}
