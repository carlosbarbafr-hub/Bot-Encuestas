import os
import discord
from discord.ext import commands, tasks
import datetime

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 1237432307120603227

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@tasks.loop(hours=168)
async def enviar_encuesta():
    channel = bot.get_channel(CHANNEL_ID)

    if channel:
        encuesta = discord.Poll(
            question="¿Qué días puedes jugar?",
            duration=datetime.timedelta(days=7),
            multiple=True
        )

        for opcion in [
            "Lunes",
            "Martes",
            "Miércoles",
            "Jueves",
            "Viernes",
            "Sábado",
            "Domingo",
            "Ninguno"
        ]:
            encuesta.add_answer(text=opcion)

        await channel.send(poll=encuesta)

@bot.event
async def on_ready():
    print(f"✅ Conectado como {bot.user}")

    if not enviar_encuesta.is_running():
        enviar_encuesta.start()

bot.run(TOKEN)
