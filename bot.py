# Miku - Discord bot
# by @cxldxice

from discord.ext import commands
import utils


config = utils.get_config()
bot = commands.Bot(command_prefix=config["bot"]["prefix"], help_command=None)
cogs = ["music"]


for cog in cogs:
    bot.load_extension(f"cogs.{cog}")


if __name__ == "__main__":
    bot.run(config["bot"]["token"])