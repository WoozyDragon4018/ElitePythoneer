import discord
from discord.ext import commands


class CustomHelpCommand(commands.HelpCommand):
	async def send_bot_help(self, mapping):
		emb = discord.Embed(
			title="PyBot Help",
			description=f"Use `{self.clean_prefix}help [command]` for more info on a command.",
			colour=0xffa500
		)
		commands_to_show = []
		for command in self.context.bot.commands:
			commands_to_show.append(command.qualified_name)
		available_commands = f"```\n{', '.join(commands_to_show)}\n```"
		emb.add_field(name="Available Commands", value=available_commands)
		await self.context.send(embed=emb)

	async def send_command_help(self, command):
		emb = discord.Embed(title="PyBot Help", description=f"```{self.get_command_signature(command)}```", colour=0xffa500)
		emb.add_field(name="Details", value=command.help or "No details available.", inline=False)
		await self.context.send(embed=emb)

	def get_command_signature(self, command):
		return '{0.clean_prefix}{1.qualified_name} {1.signature}'.format(self, command)

class Help(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._original_help_command = bot.help_command
		bot.help_command = CustomHelpCommand()
		bot.help_command.cog = self

	def cog_unload(self):
		self.bot.help_command = self._original_help_command


def setup(bot):
	bot.add_cog(Help(bot))
