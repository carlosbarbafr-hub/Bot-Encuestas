import discord
from discord.ext import commands, tasks
import os

# Configuración de intents para que el bot funcione correctamente
intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=intents)

# ID del canal donde se enviará la encuesta (Cámbialo por el tuyo)
# Puedes obtenerlo con click derecho sobre el canal en Discord -> Copiar ID
CHANNEL_ID = 1237432307120603227  

@bot.event
async def on_ready():
    print(f'Logueado como {bot.user.name}')
    # Inicia el bucle de la encuesta si no está corriendo
    if not enviar_encuesta.is_running():
        enviar_encuesta.start()

@tasks.loop(minutes=1.0)
async def enviar_encuesta():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        # Creamos la encuesta (Poll)
        # duration: timedelta de una semana
        encuesta = discord.Poll(
            question="ROL?",
            duration=discord.utils.utcnow() + discord.utils.datetime.timedelta(weeks=1),
            multiple=True
        )
        
        # Añadimos las opciones
        opciones = ["L", "M", "X", "J", "V", "S", "D", "Ningun dia"]
        for opcion in opciones:
            encuesta.add_answer(text=opcion)
        
        await channel.send(poll=encuesta)

# Token del bot (Configúralo en las Variables de Entorno de Render como DISCORD_TOKEN)
token = os.getenv("DISCORD_TOKEN")
bot.run(token)
