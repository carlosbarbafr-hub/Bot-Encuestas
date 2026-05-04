const { Client, GatewayIntentBits, PollLayoutType, ActivityType } = require('discord.js');
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
    GatewayIntentBits.MessageContent,
    GatewayIntentBits.GuildPresences, // <--- Vital para que el estado aparezca Online
    GatewayIntentBits.GuildMembers
  ]
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
  
  // Establecer estado Online explícitamente
  client.user.setPresence({
    activities: [{ name: 'Organizando partidas', type: ActivityType.Playing }],
    status: 'online',
  });

  // Configuración del cron (Ejecución cada minuto para pruebas)
  cron.schedule('* * * * *', () => {
    enviarEncuesta();
  }, { timezone: "Europe/Madrid" });

  console.log("📅 Cron programado (1 min).");
});

// Gestión de errores para evitar que el proceso se caiga
client.on('error', (e) => console.error('🔴 Error de Discord Client:', e.message));

// --- INICIO DE SESIÓN ---
if (!TOKEN) {
  console.error("🔴 ERROR: Variable TOKEN no encontrada en Environment Variables.");
} else {
  client.login(TOKEN).catch(err => {
    console.error("🔴 FALLO AL LOGUEAR:", err.message);
  });
}
