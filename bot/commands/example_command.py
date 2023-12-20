import discord
from discord.ext import commands
import asyncio


class ExampleCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_embed = None

    @commands.command(name='hello')
    async def hello_command(self, ctx):
        await ctx.send('This is an example command!')

    @commands.command(name='embed')
    async def send_embed(self, ctx, title: str, description: str, time: int):
        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.dark_red()
        )
        await ctx.message.delete()
        self.message_embed = await ctx.send(embed=embed)

        for emoji in ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']:
            await self.message_embed.add_reaction(emoji)

        await asyncio.sleep(time)
        updated_message = await self.message_embed.channel.fetch_message(self.message_embed.id)
        await self.remove_roles_from_all(updated_message)

    async def remove_roles_from_all(self, message_embed):
        reaction_users = await self.get_reaction_users(message_embed)
        guild = message_embed.guild
        role = discord.utils.get(guild.roles, name='Testing role')
        if role:
            for user_id in reaction_users:
                member = guild.get_member(user_id)
                if member:
                    await member.remove_roles(role)
                    print(f'Role {role.name} removed from {member.name}')
                else:
                    print(f'Member not found: {user_id}')
        else:
            print('Role not found')

    async def get_reaction_users(self, message_embed):
        updated_message = await message_embed.channel.fetch_message(message_embed.id)
        reaction_users = set()
        reaction = discord.utils.get(message_embed.reactions, emoji='1️⃣')
        if reaction:
            async for user in reaction.users():
                if user.id != self.bot.user.id:
                    reaction_users.add(user.id)
        return reaction_users
        
    @commands.command(name='edit_embed')
    async def edit_embed(self, ctx, new_title: str, new_description: str):
        updated_message = await self.message_embed.channel.fetch_message(self.message_embed.id)
        await ctx.message.delete()
        embed = updated_message.embeds[0]
        embed.title = new_title
        embed.description = new_description
        await updated_message.edit(embed=embed)

    @commands.command(name='create_voice')
    async def create_voice_channel(self, ctx, channel_name: str, count_users: int):
        guild = ctx.guild
        voice_channel = await guild.create_voice_channel(channel_name, user_limit=count_users)
        print('Voice created')
        await ctx.message.reply('У вас есть 2 минуты, чтобы зайти в канал иначе он удалится')
        await asyncio.sleep(5)
        while voice_channel.members:
            await asyncio.sleep(5)
            print('В канале все еще кто-то есть')
        else:
            await voice_channel.delete()
            print('Канал удален')


async def setup(bot):
    await bot.add_cog(ExampleCommand(bot))
