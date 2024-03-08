from nextcord.ext import commands
from nextcord import Interaction, slash_command, Member, Embed, Color,SlashOption
from datetime import datetime

from json import load as jsonLoad
from json import dump as jsonDump
from httpx import get, post
from re import match
from Config import Config
from utils.Cybersafeapi import Cybersafeapi
# from config import serverId, ownerIds, apiKey, username

class adminCog(commands.Cog):
    
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @slash_command(name='add-point', description='add point to target user', guild_ids=[Config().Get()["serverId"]])
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

    @slash_command(name='remove-point', description='remove point to target user', guild_ids=[Config().Get()["serverId"]])
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

    @slash_command(name='check-point', description='check point to target user', guild_ids=[Config().Get()["serverId"]])
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

    @slash_command(name='admin-topup', description='topup for admin', guild_ids=[Config().Get()["serverId"]])
    async def adminTopup(self, interaction: Interaction, link: str):
        await interaction.response.defer(ephemeral=True)
        if (interaction.user.id not in Config().Get()["ownerIds"]):
            return await interaction.send(content='No Permiss.', ephemeral=True)
        if (not match(r"https:\/\/gift\.truemoney\.com\/campaign\/\?v=+[a-zA-Z0-9]{18}", link)):
            embed = Embed()
            embed.title = '❌ เติมเงินไม่สำเร็จ'
            embed.description = f'''ลิงค์อั่งเปาไม่ถูกต้อง'''
            embed.color = Color.red()
            return await interaction.send(embed=embed, ephemeral=True)
        response = Cybersafeapi().Angpao(Config().Get()['configweb']['token'],link)
        embed = Embed()
        embed.title = 'ADMIN TOPUP'
        if (response.status_code != 200):
            embed.description = f'''
{response.json()["msg"]}
'''
        else:
            embed.description = f'''
สำเร็จ
'''
        await interaction.send(embed=embed, ephemeral=True)

    @slash_command(name='admin-balance', description='balance for admin', guild_ids=[Config().Get()["serverId"]])
    async def adminBalance(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        if (interaction.user.id not in Config().Get()["ownerIds"]):
            return await interaction.send(content='No Permiss.', ephemeral=True)
        reponse = Cybersafeapi().Me(Config().Get()['configweb']['token'])
        embed = Embed()
        embed.title = 'ADMIN TOPUP'
        embed.description = f'''
ยอดคงเหลือ {reponse.json()["result"]["t_points"]}
'''
        await interaction.send(embed=embed, ephemeral=True)

    @slash_command(name='admin-checklike', description='checklike for admin', guild_ids=[Config().Get()["serverId"]])
    async def checklike(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        if (interaction.user.id not in Config().Get()["ownerIds"]):
            return await interaction.send(content='No Permiss.', ephemeral=True)
        embed=Embed(title="ราคาปั้มไลค์", url="https://store.cyber-safe.pro", color=0x73ff00)
        embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/XLSjy8kLwrsZ2AVfrEWkEvevruLJc2wEckZ0uCuGjZU/https/media2.giphy.com/media/dbNpasmnFjbPv85DU9/giphy.gif")
        x = Cybersafeapi().Dtlike().json()["result"]
        for i in x:
            embed.add_field(name=i["action_emoji"], value=f"1 ต่อ {i['price']} บาท", inline=True)
        embed.set_footer(text="made by cybersafe")
        await interaction.send(embed=embed, ephemeral=True)

    @slash_command(name='admin-checklikeedit', description='checklikeedit for admin', guild_ids=[Config().Get()["serverId"]])
    async def checklikeedit(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        if (interaction.user.id not in Config().Get()["ownerIds"]):
            return await interaction.send(content='No Permiss.', ephemeral=True)
        dtlike = Config().Get()["configweb"]["dtlike"]
        embed=Embed(title="ราคาปั้มไลค์", url="https://store.cyber-safe.pro", color=0x73ff00)
        embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/XLSjy8kLwrsZ2AVfrEWkEvevruLJc2wEckZ0uCuGjZU/https/media2.giphy.com/media/dbNpasmnFjbPv85DU9/giphy.gif")
        for i in dtlike:
            print(i)
            embed.add_field(name=f"id {i}", value=f"name {dtlike[i]['name']} price {dtlike[i]['price']}", inline=True)
        embed.set_footer(text="made by cybersafe")
        await interaction.send(embed=embed, ephemeral=True)

    @slash_command(name='edit-price', description='edit-price for admin', guild_ids=[Config().Get()["serverId"]])
    async def editprice(self, interaction: Interaction,id: str = SlashOption(
        name="option",
        choices={"ไลค์": "1", 
        "ใจ": "2",
        "ว้าว": "3",
        "ขำ": "4",
        "เศร้า": "5",
        "โกรธ": "6"
        }),name: str = SlashOption(required=False),
                        price: float = SlashOption(required=False)):
        await interaction.response.defer(ephemeral=True)
        if (interaction.user.id not in Config().Get()["ownerIds"]):
            return await interaction.send(content='No Permiss.', ephemeral=True)
    
        dtlike = Config().Get()["configweb"]["dtlike"]
        a = dtlike[id]
        print(a)
        if name is not None:
            Config().updateConfig("configweb","dtlike",id,"name",value_to_update=name)
        if price is not None:
            Config().updateConfig("configweb","dtlike",id,"price",value_to_update=price)
        embed=Embed(title="ราคาปั้มไลค์", url="https://store.cyber-safe.pro", color=0x73ff00)
        embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/XLSjy8kLwrsZ2AVfrEWkEvevruLJc2wEckZ0uCuGjZU/https/media2.giphy.com/media/dbNpasmnFjbPv85DU9/giphy.gif")
        dtlike = Config().Get()["configweb"]["dtlike"]
        embed.add_field(name=f"id {id}", value=f"name {dtlike[id]['name']} price {dtlike[id]['price']}", inline=True)
        embed.set_footer(text="made by cybersafe")
        await interaction.send(embed=embed, ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(adminCog(bot=bot))