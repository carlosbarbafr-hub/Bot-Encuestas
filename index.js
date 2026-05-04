const { Client, GatewayIntentBits, PollLayoutType } = require('discord.js');
const cron = require('node-cron');
const express = require('express');

// ---------------- SERVER PARA MANTENERLO VIVO ----------------
const app = express();
const port = process.env.PORT || 3000;

app.get('/', (_, res) => {
  res.send('✅ Bot de Encuestas Online y Operativo');
});

app.listen(port, () => {
  console.log('🌐 Servidor web listo en puerto', port);
});

// ---------------- CONFIGURACIÓN DEL BOT ----------------
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

// ---------------- FUNCIÓN DE ENVÍO ----------------
async function enviarEncuesta() {
  try {
    console.log("⏰ Intentando enviar encuesta...");
    
    const channel = await client.channels.fetch(CANAL_ID);
    if (!channel) {
      console.log("❌ Error: No se encontró el canal. Revisa el CANAL_ID.");
      return;
    }

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
        duration: 168, // 7 días
        layoutType: PollLayoutType.Default
      }
    });

    console.log("✅ Encuesta enviada con éxito.");
  } catch (err) {
    console.error("❌ Error detallado al enviar:");
    console.error(err.message);
  }
}

// ---------------- EVENTOS Y LOGIN ----------------
client.once('ready', () => {
  console.log(`✅ ¡BOT CONECTADO! Identificado como: ${client.user.tag}`);

  // MODO PRUEBA: Cada minuto
  // Para producción (domingos): '0 0 * * 0'
  cron.schedule('* * * * *', () => {
    enviarEncuesta();
  }, {
    timezone: "Europe/Madrid"
  });

  console.log("📅 Cron activado: Ejecutando cada minuto para pruebas.");
});

// Proceso de Login con captura de errores
if (!TOKEN) {
  console.error("🔴 ERROR: La variable 'TOKEN' no está definida en Render.");
} else {
  console.log("⏳ Iniciando sesión en Discord...");
  client.login(TOKEN).catch(err => {
    console.error("🔴 FALLO CRÍTICO DE LOGIN:");
    if (err.message.includes("Privileged intent")) {
      console.error("👉 DEBES ACTIVAR 'MESSAGE CONTENT INTENT' EN EL PORTAL DE DISCORD.");
    } else if (err.message.includes("An invalid token")) {
      console.error("👉 EL TOKEN ES INCORRECTO. Dale a 'Reset Token' en Discord y actualízalo en Render.");
    } else {
      console.error(err.message);
    }
  });
}
