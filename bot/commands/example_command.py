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
    async def send_embed(self, ctx, title: str, description: str):
        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.dark_red()
        )
        await ctx.message.delete()
        self.message_embed = await ctx.send(embed=embed)

        for emoji in ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']:
            await self.message_embed.add_reaction(emoji)

        await asyncio.sleep(10)
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
        embed = updated_message.embeds[0]
        embed.title = new_title
        embed.description = new_description
        await updated_message.edit(embed=embed)


async def setup(bot):
    await bot.add_cog(ExampleCommand(bot))
