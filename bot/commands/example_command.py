import discord
from discord.ext import commands


class ExampleCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hello')
    async def hello_command(self, ctx):
        await ctx.send('This is an example command!')

    @commands.command(name='embed')
    async def send_embed(self, ctx):
        embed = discord.Embed(
            title='ВАЖНОЕ ОБЪЯВЛЕНИЕ',
            description='Нихуя себе я важный конечно. Но тут реал будет объявление потом',
            color=discord.Color.dark_red()
        )
        await ctx.message.delete()
        message_embed = await ctx.send(embed=embed)

        for emoji in ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']:
            await message_embed.add_reaction(emoji)
        


async def setup(bot):
    await bot.add_cog(ExampleCommand(bot))
