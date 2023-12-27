import discord
from discord.ext import commands
import asyncio
from data import db


class ExampleCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_embed = None
        self.user_voice_times = {}


    @commands.command(name='embed')
    async def send_embed(self, ctx, title: str, description: str, time: int):
        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.dark_red()
        )
        await ctx.message.delete()
        self.message_embed = await ctx.send(embed=embed)

        for emoji in ['<:stonk:1112096772190392320>', '<:notstonk:1112096776292413571>', '<:thonk:1112096769648631839>', '🕓', '❌']:
            await self.message_embed.add_reaction(emoji)

        await asyncio.sleep(time)
        updated_message = await self.message_embed.channel.fetch_message(self.message_embed.id)
        await self.remove_roles_from_all(updated_message)


    async def remove_roles_from_all(self, message_embed):
        roles = ['Готов', 'Не готов', 'Сомневающийся', 'Ждать позже']
        reaction_emoji = ['<:stonk:1112096772190392320>', '<:notstonk:1112096776292413571>', '<:thonk:1112096769648631839>', '🕓']
        for name_role in range(len(roles)):
            reaction_users = await self.get_reaction_users(message_embed, message_embed.reactions[name_role].emoji)
            print(reaction_users)
            guild = message_embed.guild
            role = discord.utils.get(guild.roles, name=roles[name_role])
            if role:
                print(f"role after remove: {role}")
                for user_id in reaction_users:
                    member = guild.get_member(user_id)
                    if member:
                        print(member)
                        await member.remove_roles(role)
                        print(f'Role {role.name} removed from {member.name}')
                    else:
                        print(f'Member not found: {user_id}')
            else:
                print('Role not found')


    async def get_reaction_users(self, message_embed, reaction_emoji: str):
        updated_message = await message_embed.channel.fetch_message(message_embed.id)
        reaction_users = set()
        reaction = discord.utils.get(updated_message.reactions, emoji=reaction_emoji)
        print(reaction)
        #print(updated_message.reactions)
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


    '''@commands.command(name='create_voice')
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
            print('Канал удален')'''


    @commands.command(name='top')
    async def send_top_users(self, ctx):
        top_users = db.select_top_users()
        user_id = ctx.message.author.id
        top_list = []
        for user in range(len(top_users)):
            top_list.append(f'{user+1}. {top_users[user][0]} - {top_users[user][1]} points')
        #print('\n'.join(top_list))
        top_list = '\n'.join(top_list)
        await ctx.message.reply(top_list)


    @commands.command(name='edit_points')
    async def edit_points_user(self, ctx, username: str, points: int):
        db.edit_user_points(username, points)
        print(f'Points {username} edited')


    '''@commands.command(name='test')
    async def add_usr(self, ctx):
        db.insert_user(123, 'lucifer', 20, 65)
        db.insert_user(455, 'sanya', 100, 1)
        db.insert_user(666, 'satan', 3, 0)'''


async def setup(bot):
    await bot.add_cog(ExampleCommand(bot))
