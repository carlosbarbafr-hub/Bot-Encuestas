import discord
from discord.ext import commands, tasks
import os
import datetime

# --- CONFIGURACIÓN ---
# Asegúrate de poner aquí el ID de tu canal (sin comillas, solo números)
CHANNEL_ID = 1237432307120603227 
TOKEN = os.getenv("DISCORD_TOKEN")

# --- BOT SETUP ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como: {bot.user.name}')
    if not enviar_encuesta.is_running():
        enviar_encuesta.start()
        print("⏰ Tarea programada iniciada (cada 1 minuto)")

@tasks.loop(minutes=1.0)
async def enviar_encuesta():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        try:
            encuesta = discord.Poll(
                question="ROL?",
                duration=datetime.timedelta(weeks=1),
                multiple=True
            )
            
            opciones = ["L", "M", "X", "J", "V", "S", "D", "Ningun dia"]
            for opcion in opciones:
                encuesta.add_answer(text=opcion)
            
            await channel.send(poll=encuesta)
            print(f"📊 Encuesta enviada correctamente a las {datetime.datetime.now()}")
        except Exception as e:
            print(f"❌ Error al enviar la encuesta: {e}")
    else:
        print(f"⚠️ No se encontró el canal con ID: {CHANNEL_ID}")

# --- VALIDACIÓN DE TOKEN ---
if TOKEN is None or TOKEN == "":
    print("❌ ERROR CRÍTICO: No se encontró la variable 'DISCORD_TOKEN'.")
    print("Revisa en Render: Settings -> Environment -> Add Environment Variable")
else:
    # Eliminamos espacios en blanco accidentales que a veces se cuelan al copiar
    bot.run(TOKEN.strip())
