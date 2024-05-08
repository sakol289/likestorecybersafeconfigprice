from nextcord.ext import commands
from nextcord import Interaction, slash_command, Member, Embed, Color,SlashOption
from datetime import datetime

from json import load as jsonLoad
from json import dump as jsonDump
from httpx import get, post
from re import match
from Config import Config
from utils.Newlike import Newlike
import nextcord, json, requests, re
# from config import serverId, ownerIds, apiKey, username

class adminCog(commands.Cog):
    
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @slash_command(name='add-point', description='add point to target user', guild_ids=Config().Get()["serverId"])
    async def addPoint(self, interaction: Interaction, member: Member, amount: int):
        await interaction.response.defer(ephemeral=True)
        if (interaction.user.id not in Config().Get()["ownerIds"]):
            return await interaction.send(content='No Permiss.', ephemeral=True)
        userJSON = jsonLoad(open('./database/users.json', 'r', encoding='utf-8'))
        if (str(member.id) not in userJSON):
            userJSON[str(member.id)] = {
                'userId': member.id,
                'point': amount,
                'all-point': amount,
                'spend': 0,
                'history': [
                    {
                        'type': 'admin-add',
                        'amount': amount,
                        'time': str(datetime.now())
                    }
                ]
            }
        else:
            userJSON[str(member.id)]['point'] += amount
            userJSON[str(member.id)]['all-point'] += amount
            userJSON[str(member.id)]['history'].append({
                'type': 'admin-add',
                'amount': amount,
                'time': str(datetime.now())
            })
        jsonDump(userJSON, open('./database/users.json', 'w', encoding='utf-8'), indent=4, ensure_ascii=False)
        await interaction.send(content='success', ephemeral=True)

    @slash_command(name='remove-point', description='remove point to target user', guild_ids=Config().Get()["serverId"])
    async def removePoint(self, interaction: Interaction, member: Member, amount: int):
        await interaction.response.defer(ephemeral=True)
        if (interaction.user.id not in Config().Get()["ownerIds"]):
            return await interaction.send(content='No Permiss.', ephemeral=True)
        userJSON = jsonLoad(open('./database/users.json', 'r', encoding='utf-8'))
        if (str(member.id) not in userJSON):
            userJSON[str(member.id)] = {
                'userId': member.id,
                'point': 0 - amount,
                'all-point': 0 - amount,
                'spend': 0,
                'history': [
                    {
                        'type': 'admin-add',
                        'amount': amount,
                        'time': str(datetime.now())
                    }
                ]
            }
        else:
            userJSON[str(member.id)]['point'] -= amount
            userJSON[str(member.id)]['all-point'] -= amount
            userJSON[str(member.id)]['history'].append({
                'type': 'admin-remove',
                'amount': amount,
                'time': str(datetime.now())
            })
        jsonDump(userJSON, open('./database/users.json', 'w', encoding='utf-8'), indent=4, ensure_ascii=False)
        await interaction.send(content='success', ephemeral=True)

    @slash_command(name='check-point', description='check point to target user', guild_ids=Config().Get()["serverId"])
    async def checkPoint(self, interaction: Interaction, member: Member):
        await interaction.response.defer(ephemeral=True)
        if (interaction.user.id not in Config().Get()["ownerIds"]):
            return await interaction.send(content='No Permiss.', ephemeral=True)
        userJSON = jsonLoad(open('./database/users.json', 'r', encoding='utf-8'))
        if (str(member.id) not in userJSON):
            embed = Embed()
            embed.title = 'CHECK POINT'
            embed.description = f'''ผู้ใช้ยังไม่ได้เปิดบัญชี'''
        else:
            embed = Embed()
            embed.title = 'CHECK POINT'
            embed.description = f'''
ผู้ใช้: <@{member.id}>
ยอดเงินคงเหลือ: {userJSON[str(member.id)]['point']}
ยอดเติม: {userJSON[str(member.id)]['point']}
'''
        await interaction.send(embed=embed, ephemeral=True)


    @slash_command(name='admin-balance', description='balance for admin', guild_ids=Config().Get()["serverId"])
    async def adminBalance(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        if (interaction.user.id not in Config().Get()["ownerIds"]):
            return await interaction.send(content='No Permiss.', ephemeral=True)
        response = Newlike(Config().Get()['configapi']['apikey']).Balance().json()
        status = response.get("status")
        embed = Embed()
        if status is None:
            if status != "success":
                embed.title = '`❌﹕` error'
                embed.description = f'''
        `{response}`
        '''
            embed.color = nextcord.Color.from_rgb(255, 0, 0)
            await interaction.send(content=None,embed=embed)
        else:
            embed.title = 'ADMIN TOPUP'
            embed.description = f'''
    ยอดคงเหลือ {response["balance"]}
    '''
            await interaction.send(embed=embed, ephemeral=True)

    @slash_command(name='admin-checkservice', description='checkapp for admin', guild_ids=Config().Get()["serverId"])
    async def checklikeedit(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        if (interaction.user.id not in Config().Get()["ownerIds"]):
            return await interaction.send(content='No Permiss.', ephemeral=True)
        # สร้างปุ่มและเพิ่มลงใน embed
        embed = Embed()
        embed.color = nextcord.Color.from_rgb(255, 0, 0)
        embed.title = 'ADMIN checkservice'
        embed.description = f'''
    checkservice ต่างๆใน newlike
    '''
        button = nextcord.ui.Button(style=nextcord.ButtonStyle.link, url="https://new-like.com/services", label="เช็คราคาต่างๆ")
        view = nextcord.ui.View()
        view.add_item(button)

        # ส่ง embed พร้อมกับปุ่มไปยังช่องทางที่ต้องการ
        await interaction.send(embed=embed, view=view, ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(adminCog(bot=bot))