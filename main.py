import discord
from openai import OpenAI
from dotenv import load_dotenv
from discord.ext import commands
import os

load_dotenv()
DISCORD_BOT_TOKEN= os.getenv("DISCORD_BOT_TOKEN")
OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="\\",intents=intents)
client = OpenAI(api_key = OPENAI_API_KEY)

async def buscar_historico_canal(canal, limit=10):
    messages_list = []
    async for message in canal.history(limit=limit, oldest_first=True):
        messages_list.append(
            {"role": "user" if message.author.id != bot.user.id else "system", "content": message.content}
        )
    return messages_list

def ask_gpt(mensagens):
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": mensagem}],
        model="gpt-4o-mini",
        temperature=1,
        max_tokens=200
    )
    return response.choices[0].message.content

@bot.event
async def on_ready():
    """Evento chamado quando o bot está online."""
    try:
        synced = await bot.tree.sync()
        print(f"Comandos sincronizados: {len(synced)} comandos disponíveis.")
    except Exception as e:
        print(f"Erro ao sincronizar comandos: {e}")
    print(f"Bot {bot.user.name} está online!")

@bot.tree.command(name="chat", description="Digite alguma coisa!")
async def gpt(interaction:discord.Interaction,*, mensagem:str):
    await interaction.response.defer()
    resposta = ask_gpt(mensagem)
    await interaction.followup.send(resposta)

bot.run(DISCORD_BOT_TOKEN)
