import os
import datetime

from discord.ext import commands
from dotenv import load_dotenv
from pyrez.api import SmiteAPI

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
DEV_ID = int(os.getenv("HI_REZ_DEV_ID"))
AUTH_KEY = os.getenv("HI_REZ_AUTH_KEY")

bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


@bot.command(name="motd")
async def motd(ctx: commands.Context):
    smite = SmiteAPI(DEV_ID, AUTH_KEY)
    motds = smite.getMotd()
    today = datetime.date.today()
    for motd in motds:
        start_date = datetime.datetime.strptime(
            motd.startDateTime, "%m/%d/%Y %H:%M:%S %p"
        )
        if start_date.date() == today:
            await ctx.send(f"**{motd.title}:**\n {_format_motd(motd.description)}")


def _format_motd(input: str) -> str:
    out = input.replace("<li>", "* ")
    out = out.replace("</li>", "\n ")
    out = out.replace("*", "", 1)
    out = out.replace("*", "\n *", 1)
    return out


bot.run(TOKEN)
