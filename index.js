const { Client, GatewayIntentBits, PollLayoutType } = require('discord.js');
const cron = require('node-cron');
const express = require('express');

const app = express();
const port = process.env.PORT || 3000;

app.get('/', (_, res) => res.send('Bot Vivo'));
app.listen(port, () => console.log('🌐 Servidor web listo en puerto', port));

// He añadido más Intents para asegurar la conexión
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent
  ]
});

const TOKEN = process.env.TOKEN;
const CANAL_ID = "1488617412763979889";
const ROL_ID = "1491026733447512094";

async function enviarEncuesta() {
  try {
    const channel = await client.channels.fetch(CANAL_ID);
    if (!channel) return console.log("❌ Canal no encontrado");

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
        duration: 1,
        layoutType: PollLayoutType.Default
      }
    });
    console.log("✅ Encuesta enviada");
  } catch (err) {
    console.error("❌ Error enviando:", err.message);
  }
}

client.once('ready', () => {
  console.log(`✅ ¡CONECTADO CON ÉXITO! Usuario: ${client.user.tag}`);
  
  // Prueba cada minuto
  cron.schedule('* * * * *', () => {
    enviarEncuesta();
  }, { timezone: "Europe/Madrid" });
  
  console.log("📅 Cron de 1 min activado");
});

// LOGIN CON CAPTURA DE ERROR
console.log("⏳ Intentando conectar con Discord...");
client.login(TOKEN).catch(err => {
  console.error("🔴 ERROR DE LOGIN DIRECTO:");
  console.error(err);
});
