const { Client, GatewayIntentBits, PollLayoutType } = require('discord.js');
const cron = require('node-cron');
const express = require('express');

// ---------------- SERVER PARA UPTIME ----------------
const app = express();
const port = process.env.PORT || 3000;

app.get('/', (_, res) => {
  res.send('✅ Bot en fase de prueba (cada minuto)');
});

app.listen(port, () => {
  console.log('🌐 Servidor web listo en puerto', port);
});

// ---------------- CONFIGURACIÓN BOT ----------------
const client = new Client({
  intents: [GatewayIntentBits.Guilds] 
});

const TOKEN = process.env.TOKEN;
const CANAL_ID = "1237432307120603227";
const ROL_ID = "1491026733447512094";

// ---------------- FUNCIÓN ENCUESTA ----------------
async function enviarEncuesta() {
  try {
    const channel = await client.channels.fetch(CANAL_ID);
    if (!channel) return console.log("❌ Canal no encontrado");

    await channel.send({
      content: `<@&${ROL_ID}> ¡Es hora de organizar la semana!`,
      poll: {
        question: { text: "¿Qué días podéis jugar?" },
        answers: [
          { text: "Lunes" },
          { text: "Martes" },
          { text: "Miércoles" },
          { text: "Jueves" },
          { text: "Viernes" },
          { text: "Sábado" },
          { text: "Domingo" },
          { text: "Ningún día" }
        ],
        allowMultiselect: true,
        duration: 1, // Duración mínima para pruebas
        layoutType: PollLayoutType.Default
      }
    });

    console.log("✅ Encuesta de prueba enviada (cada minuto)");
  } catch (err) {
    console.error("❌ Error al enviar encuesta:", err);
  }
}

// ---------------- INICIO Y CRON ----------------
client.once('ready', () => {
  console.log(`🤖 Sesión iniciada como ${client.user.tag}`);

  // MODO PRUEBA: Se ejecuta CADA MINUTO
  cron.schedule('* * * * *', () => {
    enviarEncuesta();
  }, {
    timezone: "Europe/Madrid"
  });

  console.log("⚠️ ALERTA: Cron configurado CADA MINUTO para pruebas.");
});

client.login(TOKEN).catch(err => console.error("❌ Fallo en login:", err));
