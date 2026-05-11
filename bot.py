import os
import datetime
import logging
from threading import Thread

from flask import Flask
import discord
from discord.ext import commands, tasks

# =========================================================
# LOGS
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# =========================================================
# FLASK (Render Health Check)
# =========================================================

app = Flask(__name__)

@app.route("/")
def health_check():
    return "Bot is running", 200

def run_web():
    port = int(os.environ.get("PORT", 10000))

    logging.info(f"🌐 Iniciando servidor Flask en puerto {port}")

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
        use_reloader=False
    )

def keep_alive():
    thread = Thread(target=run_web)
    thread.daemon = True
    thread.start()

# =========================================================
# DISCORD BOT
# =========================================================

TOKEN = os.getenv("DISCORD_TOKEN")

# CAMBIA ESTO POR TU CANAL
CHANNEL_ID = 1237432307120603227

if not TOKEN:
    raise ValueError("❌ No existe DISCORD_TOKEN en variables de entorno.")

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

# Bot
bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# =========================================================
# EVENTOS
# =========================================================

@bot.event
async def on_ready():
    logging.info(f"✅ Bot conectado como: {bot.user}")
    logging.info(f"🆔 Bot ID: {bot.user.id}")

    if not enviar_encuesta.is_running():
        enviar_encuesta.start()
        logging.info("📅 Loop de encuestas iniciado.")

@bot.event
async def on_disconnect():
    logging.warning("⚠️ Bot desconectado de Discord.")

@bot.event
async def on_resumed():
    logging.info("🔄 Conexión reanudada correctamente.")

# =========================================================
# LOOP DE ENCUESTA
# =========================================================

@tasks.loop(hours=168)  # 7 días
async def enviar_encuesta():

    logging.info("⏳ Intentando enviar encuesta semanal...")

    channel = bot.get_channel(CHANNEL_ID)

    # Si no está en cache, buscarlo
    if channel is None:
        try:
            channel = await bot.fetch_channel(CHANNEL_ID)
        except Exception as e:
            logging.error(f"❌ No se pudo obtener el canal: {e}")
            return

    try:
        encuesta = discord.Poll(
            question="¿Qué días puedes jugar?",
            duration=datetime.timedelta(days=7),
            multiple=True
        )

        opciones = [
            "Lunes",
            "Martes",
            "Miércoles",
            "Jueves",
            "Viernes",
            "Sábado",
            "Domingo",
            "Ninguno"
        ]

        for opcion in opciones:
            encuesta.add_answer(text=opcion)

        await channel.send(poll=encuesta)

        logging.info("✅ Encuesta enviada correctamente.")

    except Exception as e:
        logging.error(f"❌ Error enviando encuesta: {e}")

# =========================================================
# COMANDO TEST
# =========================================================

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    logging.info("🚀 Iniciando servidor web...")
    keep_alive()

    logging.info("🤖 Conectando a Discord...")

    try:
        bot.run(TOKEN.strip(), log_handler=None)

    except discord.LoginFailure:
        logging.error("❌ Token inválido.")

    except discord.HTTPException as e:
        logging.error(f"❌ Error HTTP Discord: {e}")

    except Exception as e:
        logging.exception(f"❌ Error inesperado: {e}")
