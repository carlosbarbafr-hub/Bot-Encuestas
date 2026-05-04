const { Client, GatewayIntentBits, PollLayoutType } = require('discord.js');
const cron = require('node-cron');
const express = require('express');

// --- SERVIDOR WEB ---
const app = express();
const port = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.send('✅ Bot de encuestas activo');
});

app.listen(port, () => {
  console.log(`🌐 Web activa en puerto ${port}`);
});

// --- BOT DISCORD ---
const client = new Client({
  intents: [GatewayIntentBits.Guilds]
});

const TOKEN = process.env.TOKEN;
const CANAL_ID = "1488617412763979889";
const ROL_ID = "1491026733447512094";

// --- FUNCIÓN ENCUESTA ---
async function enviarEncuesta() {
  try {
    console.log("⏰ Ejecutando encuesta:", new Date().toLocaleString("es-ES", { timeZone: "Europe/Madrid" }));

    const channel = await client.channels.fetch(CANAL_ID);

    if (!channel) {
      console.error("❌ Canal no encontrado");
      return;
    }

    await channel.send({
      content: `<@&${ROL_ID}> ¡Es hora de organizar la semana! 🛡️`,
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
          { text: "Ningún día, soy gay" } // 👈 tu broma vuelve aquí
        ],
        allowMultiselect: true,
        duration: 168,
        layoutType: PollLayoutType.Default
      }
    });

    console.log("✅ Encuesta enviada correctamente");
  } catch (error) {
    console.error("❌ Error al enviar encuesta:", error);
  }
}

// --- ARRANQUE ---
client.once('ready', () => {
  console.log(`🤖 Conectado como ${client.user.tag}`);

  // 🔹 TEST (cada minuto)
  cron.schedule('* * * * *', enviarEncuesta, {
    timezone: "Europe/Madrid"
  });

  // 🔹 PRODUCCIÓN (activar cuando confirmes que funciona)
  /*
  cron.schedule('0 17 * * 0', enviarEncuesta, {
    timezone: "Europe/Madrid"
  });
  */
});

client.login(TOKEN);
