import discord
from discord.ext import commands, tasks
import os
import datetime
from flask import Flask
from threading import Thread

# --- SERVIDOR WEB PARA ENGAÑAR A RENDER ---
app = Flask('')

@app.route('/')
def home():
    return "Bot esta vivo!"

def run():
    # Render usa el puerto 10000 por defecto
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- CONFIGURACIÓN DEL BOT ---
CHANNEL_ID = 1237432307120603227  # REEMPLAZA CON TU ID
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como: {bot.user.name}')
    if not enviar_encuesta.is_running():
        enviar_encuesta.start()

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
            for opc in ["L", "M", "X", "J", "V", "S", "D", "Ningun dia"]:
                encuesta.add_answer(text=opc)
            
            await channel.send(poll=encuesta)
            print("📊 Encuesta enviada.")
        except Exception as e:
            print(f"❌ Error: {e}")

# --- INICIO ---
if TOKEN:
    keep_alive() # Esto arranca el servidor web en segundo plano
    bot.run(TOKEN.strip())
else:
    print("❌ Falta el TOKEN en Environment Variables")
