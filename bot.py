import discord
from discord.ext import commands, tasks
import os
import datetime
from flask import Flask
from threading import Thread

# --- CONFIGURACIÓN DE FLASK PARA RENDER ---
app = Flask('')

@app.route('/')
def health_check():
    return "Bot is running", 200

def run():
    # Render usa la variable de entorno PORT, por defecto 10000
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- CONFIGURACIÓN DEL BOT DE DISCORD ---
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 1237432307120603227 # ID de tu canal

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@tasks.loop(hours=168.0) # Una vez a la semana
async def enviar_encuesta():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        try:
            encuesta = discord.Poll(
                question="¿Qué días puedes jugar?",
                duration=datetime.timedelta(days=7),
                multiple=True
            )
            for opc in ["L", "M", "X", "J", "V", "S", "D", "Ninguno"]:
                encuesta.add_answer(text=opc)
            await channel.send(poll=encuesta)
            print("Encuesta enviada.")
        except Exception as e:
            print(f"Error encuesta: {e}")

@bot.event
async def on_ready():
    print(f'✅ Bot online: {bot.user}')
    if not enviar_encuesta.is_running():
        enviar_encuesta.start()

# --- EJECUCIÓN ---
if __name__ == "__main__":
    if not TOKEN:
        print("❌ Error: No hay TOKEN en las variables de entorno.")
    else:
        # IMPORTANTE: Arrancamos Flask PRIMERO para que Render vea el puerto abierto
        print("🚀 Iniciando servidor web de salud...")
        keep_alive()
        
        print("🤖 Conectando a Discord...")
        try:
            bot.run(TOKEN.strip())
        except Exception as e:
            print(f"❌ Error al ejecutar el bot: {e}")
