import discord
from discord.ext import commands, tasks
import os
import datetime
import asyncio
from flask import Flask
from threading import Thread

# --- SERVIDOR WEB ---
app = Flask('')
@app.route('/')
def home(): return "Bot esta vivo!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- CONFIGURACIÓN ---
CHANNEL_ID = 1237432307120603227 
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Conectado como {bot.user.name}')
    # Esperamos 5 segundos antes de iniciar tareas para evitar el rate limit inicial
    await asyncio.sleep(5)
    if not enviar_encuesta.is_running():
        enviar_encuesta.start()

# CAMBIO CRÍTICO: Se ejecuta cada 168 horas (1 semana)
@tasks.loop(hours=1.0)
async def enviar_encuesta():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        try:
            encuesta = discord.Poll(
                question="¿Qué días puedes jugar (ROL)?",
                duration=datetime.timedelta(days=7),
                multiple=True
            )
            for opc in ["L", "M", "X", "J", "V", "S", "D", "Ninguno"]:
                encuesta.add_answer(text=opc)
            
            await channel.send(poll=encuesta)
            print("📊 Encuesta enviada con éxito.")
        except Exception as e:
            print(f"❌ Error: {e}")

if TOKEN:
    keep_alive()
    try:
        bot.run(TOKEN.strip())
    except Exception as e:
        print(f"❌ Error de conexión: {e}. Probablemente sigues bajo Rate Limit.")
