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


@bot.command(name="player-matches")
async def player_match_history(ctx: commands.Context, player_name: str, count: int = 5):
    smite = SmiteAPI(DEV_ID, AUTH_KEY)
    player = smite.getPlayer(player_name)
    match_history = smite.getMatchHistory(player.playerId)
    if count > len(match_history):
        await ctx.send(
            f"Can't query {count} rounds for player {player_name}. {len(match_history)} rounds available."
        )

    message = f"** Previous {count} rounds of match history for {player_name}:** \n"
    message += "------------------------------------- \n"
    win_totals = 0
    for match in match_history[:count]:
        win_totals += 1 if match.winStatus == "Win" else 0
        win_emoji = ":white_check_mark:" if match.winStatus == "Win" else ":skull:"
        kd_emoji = ":arrow_up:" if match.kills > match.deaths else ":arrow_down:"
        message += f"God Played: {match.godName} \n"
        message += f"Status: {match.winStatus} {win_emoji} \n"
        message += f"Queue: {match.queue}\n"
        message += f"K/D/A: {match.kills}/{match.deaths}/{match.assists} {kd_emoji}\n"
        message += f"Total Time (In Minutes): {match.matchMinutes}\n"
        message += f"-------------------------------------\n"
    message += f"Total Wins/Losses: {win_totals}/{count - win_totals}"
    await ctx.send(message)


def _format_motd(input: str) -> str:
    out = input.replace("<li>", "* ")
    out = out.replace("</li>", "\n ")
    out = out.replace("*", "", 1)
    out = out.replace("Map:", "\n * Map:")
    return out


bot.run(TOKEN)
