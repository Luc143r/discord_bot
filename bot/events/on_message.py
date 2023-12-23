import discord
from discord.ext import commands
import asyncio
from data import db


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
                    total_time = total_time // 60
                    points_time = total_time // 5
                    await member.send(f'вы провели в голосовом канале {points_time}')
                    # username = member
                    user_id = member.id
                    del self.user_voice_times[member.id]
                    is_instance = db.select_user(int(user_id))
                    if not is_instance:
                        db.insert_user(int(userid), str(member), 0, 0)
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
                db.insert_user(int(user_id), str(username), 0, 0)
            count_points = len(message.content) // 10
            user_points = db.select_user(user_id)[3]
            db.update_points(user_id, user_points+count_points)


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        if str(reaction.emoji) == '1️⃣':
            guild = reaction.message.guild
            role = discord.utils.get(guild.roles, name='Testing role')
            if role:
                await user.add_roles(role)
            else:
                print('Такой роли не существует')


async def setup(bot):
    await bot.add_cog(OnMessageCog(bot))
