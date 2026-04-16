const { Client, GatewayIntentBits, PollLayoutType } = require('discord.js');
const cron = require('node-cron');
const express = require('express');

// --- CONFIGURACIÓN DEL SERVIDOR WEB (Para Render) ---
const app = express();
const port = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.send('✅ Bot de Encuestas funcionando 24/7');
});

app.listen(port, () => {
  console.log(`Servidor web activo en el puerto ${port}`);
});

// --- CONFIGURACIÓN DEL BOT DE DISCORD ---
const client = new Client({ 
  intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages] 
});

// REEMPLAZA ESTOS DATOS CON LOS TUYOS
const TOKEN = "MTQ5MDY2NzA1NzkxNjY3ODM0Ng.GQzFoC.WKEGv8kQeBtvil96b6r-lR-lE1POjd9oP_KSjQ";
const CANAL_ID = "843615420417835049";
const ROL_ID = "1204479002333683732"; // ID del rol @aventureros 

client.once('ready', () => {
  console.log(`✅ Conectado como ${client.user.tag}`);

  // PROGRAMACIÓN: Domingos a las 17:00 (Hora España)
  // Formato: Minuto(0) Hora(17) Día(*) Mes(*) DíaSemana(0=Domingo)
  cron.schedule('0 17 * * 0', async () => {
    try {
      const channel = await client.channels.fetch(CANAL_ID);

      await channel.send({
        content: `<@&${ROL_ID}> ¡Es hora de organizar la semana! 🛡️`,
        poll: {
          question: { text: "¿Qué días podéis jugar?" },
          answers: [
            { text: "Lunes"},
            { text: "Martes"},
            { text: "Miércoles"},
            { text: "Jueves",},
            { text: "Viernes",},
            { text: "Sábado", },
            { text: "Domingo",},
            { text: "Ningún día, soy gay",}
          ],
          allowMultiselect: true, // Como en tu imagen
          duration: 168, // Abierta 7 días
          layoutType: PollLayoutType.Default
        }
      });
      
      console.log("📊 Encuesta dominical enviada con éxito.");
    } catch (error) {
      console.error("❌ Error al enviar la encuesta:", error);
    }
  }, {
    timezone: "Europe/Madrid"
  });
});

client.login(TOKEN);
