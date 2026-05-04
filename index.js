const { Client, GatewayIntentBits, PollLayoutType } = require('discord.js');
const cron = require('node-cron');
const express = require('express');

// ---------------- WEB SERVER ----------------
const app = express();
const port = process.env.PORT || 3000;

app.get('/', (_, res) => {
  res.send('Bot activo');
});

app.listen(port, () => {
  console.log('🌐 Web activa en puerto', port);
});

// ---------------- BOT ----------------
const client = new Client({
  intents: [GatewayIntentBits.Guilds]
});

const TOKEN = process.env.TOKEN;
const CANAL_ID = "1488617412763979889";
const ROL_ID = "1491026733447512094";

// 🔴 DEBUG REAL
console.log("TOKEN existe:", !!TOKEN);

// ---------------- FUNCIÓN ----------------
async function enviarEncuesta() {
  try {
    console.log("⏰ Ejecutando encuesta");

    const channel = await client.channels.fetch(CANAL_ID);

    if (!channel) {
      console.log("❌ Canal no encontrado");
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
          { text: "Ningún día, soy gay" }
        ],
        allowMultiselect: true,
        duration: 168,
        layoutType: PollLayoutType.Default
      }
    });

    console.log("✅ Encuesta enviada");
  } catch (err) {
    console.error("❌ Error encuesta:", err);
  }
}

// ---------------- LOGIN SEGURO ----------------
async function startBot() {
  try {
    await client.login(TOKEN);
    console.log("🔑 Login correcto");

    console.log(`🤖 Conectado como ${client.user.tag}`);

    // cron SOLO cuando está logueado
    cron.schedule('* * * * *', enviarEncuesta, {
      timezone: "Europe/Madrid"
    });

  } catch (err) {
    console.error("❌ ERROR LOGIN:", err);
  }
}

client.once('ready', () => {
  console.log("🟢 Bot listo");
});

startBot();
