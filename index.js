const { Client, GatewayIntentBits, PollLayoutType } = require('discord.js');
const cron = require('node-cron');
const express = require('express');

// --- SERVIDOR WEB (Obligatorio para Render) ---
const app = express();
const port = process.env.PORT || 3000;

app.get('/', (_, res) => res.send('Bot de Encuestas: Sistema Activo'));
app.listen(port, () => console.log(`🌐 Servidor web en puerto ${port}`));

// --- CONFIGURACIÓN DEL CLIENTE ---
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent
  ],
  // Reintento automático si la conexión falla
  retryLimit: 5 
});

const TOKEN = process.env.TOKEN;
const CANAL_ID = "1488617412763979889";
const ROL_ID = "1491026733447512094";

// --- FUNCIÓN DE LA ENCUESTA ---
async function enviarEncuesta() {
  try {
    const channel = await client.channels.fetch(CANAL_ID);
    if (!channel) return console.log("❌ Error: Canal no encontrado.");

    await channel.send({
      content: `<@&${ROL_ID}> ¡Es hora de organizar la semana!`,
      poll: {
        question: { text: "¿Qué días podéis jugar?" },
        answers: [
          { text: "Lunes" }, { text: "Martes" }, { text: "Miércoles" },
          { text: "Jueves" }, { text: "Viernes" }, { text: "Sábado" },
          { text: "Domingo" }, { text: "Ningún día" }
        ],
        allowMultiselect: true,
        duration: 168,
        layoutType: PollLayoutType.Default
      }
    });
    console.log("✅ Encuesta enviada satisfactoriamente.");
  } catch (err) {
    console.error("❌ Error enviando encuesta:", err.message);
  }
}

// --- EVENTOS ---
client.once('ready', () => {
  console.log(`✅ ¡LOGIN EXITOSO! Bot conectado como: ${client.user.tag}`);

  // Configuración del cron (Cada minuto para probar)
  cron.schedule('* * * * *', () => {
    enviarEncuesta();
  }, { timezone: "Europe/Madrid" });

  console.log("📅 Cron programado (1 min).");
});

// Captura de errores de red/IP
client.on('error', (e) => console.error('🔴 Error de Discord Client:', e.message));
client.on('warn', (e) => console.warn('⚠️ Advertencia:', e));

// --- INICIO DE SESIÓN ---
if (!TOKEN) {
  console.error("🔴 ERROR: No se detecta la variable TOKEN en Render.");
} else {
  console.log("⏳ Iniciando conexión con Discord...");
  
  // Timeout de seguridad: Si en 20s no conecta, es problema de IP o Token
  const timeout = setTimeout(() => {
    if (!client.user) {
      console.error("🚨 TIEMPO DE ESPERA AGOTADO: El bot no logra conectar.");
      console.error("Posible IP baneada por Discord o Token bloqueado.");
      console.error("Prueba a hacer 'Suspend' y 'Resume' en Render para cambiar de IP.");
    }
  }, 20000);

  client.login(TOKEN)
    .then(() => clearTimeout(timeout))
    .catch(err => {
      console.error("🔴 FALLO AL LOGUEAR:");
      console.error(err.message);
    });
}
