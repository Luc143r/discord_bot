import discord
from discord.ext import commands
import asyncio


class OnMessageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        content = message.content
        if message.author.bot:
            return
        elif content[0] == '!':
            return
        else:
            print(message.content)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        if str(reaction.emoji) == '1️⃣':
            guild = reaction.message.guild
            role = discord.utils.get(guild.roles, name='Testing role')
            if role:
                await user.add_roles(role)
                print('Роль выдана')
                await asyncio.sleep(60)
                await user.remove_roles(role)
                print('Роль спиздили')
            else:
                print('Такой роли не существует')


async def setup(bot):
    await bot.add_cog(OnMessageCog(bot))
