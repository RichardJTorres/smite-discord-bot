import os
import datetime

from discord import Embed
from discord.ext import commands
from dotenv import load_dotenv
from pyrez.api import SmiteAPI
from pyrez.exceptions import ServiceUnavailable

from utils import parse_motd, parse_timestamp, datetime_to_preferred_tz, DATE_FORMAT

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
DEV_ID = int(os.getenv("HI_REZ_DEV_ID"))
AUTH_KEY = os.getenv("HI_REZ_AUTH_KEY")
PREFERRED_TZ = os.getenv("PREFERRED_TZ") or "UTC"

bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


@bot.command(name="motd")
async def motd(ctx: commands.Context):
    smite = SmiteAPI(DEV_ID, AUTH_KEY)
    try:
        motds = smite.getMotd()
    except ServiceUnavailable as e:
        return await ctx.send(str(e))

    today = datetime.date.today()
    for motd in motds:
        parsed = parse_motd(motd.description)
        start_date = parse_timestamp(motd.startDateTime)
        if start_date.date() == today:
            embed = Embed(title=f"{motd.title}", description=parsed.pop("description"))
            for k, v in parsed.items():
                embed.add_field(name=k, value=v, inline=False)
            await ctx.send(embed=embed)


@bot.command(name="player-matches")
async def player_match_history(ctx: commands.Context, player_name: str, count: int = 6):
    smite = SmiteAPI(DEV_ID, AUTH_KEY)
    player = smite.getPlayer(player_name)
    match_history = smite.getMatchHistory(player.playerId)
    embed = Embed(title=f"Previous {count} rounds of match history for {player_name}")
    win_totals = 0
    for i, match in enumerate(match_history[:count]):
        win_totals += 1 if match.winStatus == "Win" else 0
        win_emoji = ":white_check_mark:" if match.winStatus == "Win" else ":skull:"
        kd_emoji = ":arrow_up:" if match.kills > match.deaths else ":arrow_down:"
        message = f"God Played: {match.godName} \n"
        message += f"Status: {match.winStatus} {win_emoji} \n"
        message += f"Queue: {match.queue}\n"
        message += f"K/D/A: {match.kills}/{match.deaths}/{match.assists} {kd_emoji}\n"
        message += f"Total Time (In Minutes): {match.matchMinutes}\n"
        preferred_time = datetime_to_preferred_tz(parse_timestamp(match.matchTime), PREFERRED_TZ)
        message += f"Match Time: {preferred_time.strftime(DATE_FORMAT)}"
        embed.add_field(name=f"Match {i+1}", value=message, inline=False)

    embed.set_footer(text=f"Total Wins/Losses: {win_totals}/{count - win_totals}")

    await ctx.send(embed=embed)


bot.run(TOKEN)
