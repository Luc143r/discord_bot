import discord
from discord.ext import commands
import asyncio
from data import db
from config.config import roles


class OnMessageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_voice_times = {}


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel != after.channel:
            if after.channel is not None:
                self.user_voice_times[member.id] = discord.utils.utcnow()
            if before.channel is not None:
                if member.id in self.user_voice_times:
                    total_time = (discord.utils.utcnow() - self.user_voice_times[member.id]).total_seconds()
                    if int(total_time) >= 60:
                        total_time = total_time // 60
                        await member.send(f'Вы провели в голосовом канале {total_time} минут')
                        points_time = total_time // 5
                    else:
                        await member.send(f'Вы провели в голосовом канале {total_time} секунд')
                        total_time = 0
                        points_time = 0
                    # username = member
                    user_id = member.id
                    del self.user_voice_times[member.id]
                    is_instance = db.select_user(int(user_id))
                    if not is_instance:
                        db.insert_user(int(user_id), str(member), 0, 0)
                    user_points = db.select_user(int(user_id))[3]
                    user_times = db.select_user(int(user_id))[4]
                    db.update_points(user_id, user_points+points_time)
                    db.update_time_voice(user_id, user_times+int(total_time))


    @commands.Cog.listener()
    async def on_message(self, message):
        content = message.content
        if message.author.bot:
            return
        elif content[0] == '!':
            return
        else:
            length_message = len(message.content)
            username = message.author
            user_id = message.author.id
            is_instance = db.select_user(int(user_id))
            if not is_instance:
                db.insert_user(int(user_id), str(username), 0, 0, 0)
            user_symbols = db.select_symbols(int(user_id))[5]
            db.update_symbols(user_id, length_message + int(user_symbols))
            print(user_symbols)
            count_points = (length_message + int(user_symbols)) // 10
            print(count_points)
            user_points = db.select_user(user_id)[3]
            db.update_points(user_id, user_points+count_points)
            user_points = user_points+count_points
            print(user_points)
            if user_points >= 50 and user_points <= 250:
                guild = message.guild
                role = discord.utils.get(guild.roles, name=roles[50])
                await message.author.add_roles(role)
            elif user_points >= 250 and user_points <= 500:
                guild = message.guild
                role = discord.utils.get(guild.roles, name=roles[250])
                await message.author.add_roles(role)
            elif user_points >= 500 and user_points <= 1000:
                guild = message.guild
                role = discord.utils.get(guild.roles, name=roles[500])
                await message.author.add_roles(role)
            elif user_points >= 1000 and user_points <= 3000:
                guild = message.guild
                role = discord.utils.get(guild.roles, name=roles[1000])
                await message.author.add_roles(role)
            elif user_points >= 3000 and user_points <= 5000:
                guild = message.guild
                role = discord.utils.get(guild.roles, name=roles[3000])
                await message.author.add_roles(role)
            elif user_points >= 5000:
                guild = message.guild
                role = discord.utils.get(guild.roles, name=roles[5000])
                await message.author.add_roles(role)
            else:
                print('less 50')


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        if str(reaction.emoji) == '<:stonk:1112096772190392320>':
            guild = reaction.message.guild
            role = discord.utils.get(guild.roles, name='Готов')
            if role:
                await user.add_roles(role)
            else:
                print('Такой роли не существует')
        elif str(reaction.emoji) == '<:notstonk:1112096776292413571>':
            guild = reaction.message.guild
            role = discord.utils.get(guild.roles, name='Не готов')
            if role:
                await user.add_roles(role)
            else:
                print('Такой роли не существует')
        elif str(reaction.emoji) == '<:thonk:1112096769648631839>':
            guild = reaction.message.guild
            role = discord.utils.get(guild.roles, name='Сомневающийся')
            if role:
                await user.add_roles(role)
            else:
                print('Такой роли не существует')
        elif str(reaction.emoji) == '🕓':
            guild = reaction.message.guild
            role = discord.utils.get(guild.roles, name='Ждать позже')
            if role:
                await user.add_roles(role)
            else:
                print('Такой роли не существует')
        elif str(reaction.emoji) == '❌':
            guild = reaction.message.guild
            role = discord.utils.get(guild.roles, name='Непригоден для ПБ')
            if role:
                await user.add_roles(role)
            else:
                print('Такой роли не существует')

    
    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if user.bot:
            return
        if str(reaction.emoji) == '<:stonk:1112096772190392320>':
            guild = reaction.message.guild
            role = discord.utils.get(guild.roles, name='Готов')
            if role:
                await user.remove_roles(role)
            else:
                print('Такой роли не существует')
        elif str(reaction.emoji) == '<:notstonk:1112096776292413571>':
            guild = reaction.message.guild
            role = discord.utils.get(guild.roles, name='Не готов')
            if role:
                await user.remove_roles(role)
            else:
                print('Такой роли не существует')
        elif str(reaction.emoji) == '<:thonk:1112096769648631839>':
            guild = reaction.message.guild
            role = discord.utils.get(guild.roles, name='Сомневающийся')
            if role:
                await user.remove_roles(role)
            else:
                print('Такой роли не существует')
        elif str(reaction.emoji) == '🕓':
            guild = reaction.message.guild
            role = discord.utils.get(guild.roles, name='Ждать позже')
            if role:
                await user.remove_roles(role)
            else:
                print('Такой роли не существует')
        elif str(reaction.emoji) == '❌':
            guild = reaction.message.guild
            role = discord.utils.get(guild.roles, name='Непригоден для ПБ')
            if role:
                await user.remove_roles(role)
            else:
                print('Такой роли не существует')


async def setup(bot):
    await bot.add_cog(OnMessageCog(bot))
