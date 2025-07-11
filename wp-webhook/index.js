const express = require('express');
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const axios = require('axios');

const app = express();
app.use(express.json());

// WhatsApp client con almacenamiento persistente
const client = new Client({
  authStrategy: new LocalAuth({
    dataPath: './session'
  }),
  puppeteer: {
    headless: true,
    args: ['--no-sandbox']
  }
});

// Mostrar QR una sola vez
client.on('qr', (qr) => {
  console.log('Escaneá este QR con tu WhatsApp:');
  qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
  console.log('✅ WhatsApp listo para usar');
});

client.on('message', async (message) => {
  const from = message.from;
  const text = message.body;

  console.log(text)

  // Ignorar mensajes de grupos
  if (message.isGroupMsg) return;

  try {
    const response = await axios.post('http://localhost:5678/webhook/chat', {
      sessionId: from,
      message: text
    });

    const {output} = response.data;


    if (output) {
      console.log(output)
      await client.sendMessage(from, output);
    }
  } catch (err) {
    console.error('❌ Error al procesar mensaje:', err.message);
    await client.sendMessage(from, '⚠️ Ocurrió un error al responder.');
  }
});

client.initialize();

// Opcional: Servidor Express para test
app.get('/', (req, res) => {
  res.send('WhatsApp bot activo');
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🌐 Express corriendo en http://localhost:${PORT}`);
});
