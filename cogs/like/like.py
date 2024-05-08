import nextcord, json, httpx, re
from nextcord.ext import commands
from bs4 import BeautifulSoup
from datetime import datetime
from Config import Config
from utils.Cybersafeapi import Cybersafeapi

dtlike = Config().Get()["configweb"]["dtlike"]


class likeautofree(nextcord.ui.Modal):
    def __init__(self,bot,app,idlike,message: nextcord.Message):
        self.bot = bot
        self.app = app
        self.idlike = idlike
        self.message = message
        super().__init__(auto_defer=True, title="Verify")
        self.Input_link = nextcord.ui.TextInput(
            label="Link",
            style=nextcord.TextInputStyle.short,
            required=True,
            placeholder="ใส่ link",
        )
        self.add_item(self.Input_link)
        self.Input_amount = nextcord.ui.TextInput(
            label="amount",
            style=nextcord.TextInputStyle.short,
            required=True,
            placeholder="ใส่ amount",
        )
        self.add_item(self.Input_amount)
    async def callback(self, interaction: nextcord.Interaction):
        await interaction.send("send",delete_after=0)
        # await self.message.edit(f"{self.app} {self.idlike} {self.Input_link.value} {self.Input_amount.value}",embed=None,view=None)
        await self.message.edit(content='[SELECT] กำลังตรวจสอบ',embed=None,view=None)
        userdata = json.load(open('./database/users.json', 'r', encoding='utf-8'))
        embed = nextcord.Embed()
        if (self.Input_amount.value.isnumeric()):
            if (str(interaction.user.id) in userdata):
                price = float(self.app["price"]) * float(self.Input_amount.value)
                await self.message.edit(content=f"ปั้ม {self.app['name']} price {price}")
                if (userdata[str(interaction.user.id)]['point'] >= price):
                    reponse = Cybersafeapi().Buylike(Config().Get()['configweb']['token'],self.Input_link.value,self.Input_amount.value,self.idlike)
                    e = reponse.json()
                    if e["status"] == "succeed":

                        userdata[str(interaction.user.id)]['point'] -= price
                        userdata[str(interaction.user.id)]['spend'] += price
                        userdata[str(interaction.user.id)]['history'].append({
                            "type": "buylike",
                            "item": f"idlike_{self.idlike}",
                            "price": price,
                            "description": f"auto {self.app['name']} price {price} link {self.Input_link.value}",
                            "time": str(datetime.now()),
                        })
                        json.dump(userdata, open('./database/users.json', 'w', encoding='utf-8'), indent=4, ensure_ascii=False)
                            
                        embed.title = '``✅`` ซื้อสินค้าสำเร็จ'
                        embed.description = f'''บอทได้ส่งข้อมูลไปยังแชทส่วนตัวของคุณแล้ว\nยอดเงินคงเหลือ : `` {userdata[str(interaction.user.id)]["point"]} ``'''
                        embed.color = nextcord.Color.from_rgb(0, 255, 0)

                        embedDM = nextcord.Embed()
                        embedDM.title = f'''ปั้ม {self.app['name']} สำเร็จ'''
                        embedDM.color = nextcord.Color.from_rgb(0, 255, 0)
                        embedDM.set_image(url=Config().Get()["embed"]["imglogo"])
                        embedDM.description = f'''
        > `user`: <@{interaction.user.id}>
        > `status`: {self.app['name']}
        > `price`: {price} บาท
        > `amount`: {self.Input_amount.value}
        > `link`: {self.Input_link.value}
        > `time`: {str(datetime.now())}
        '''
                        await interaction.user.send(embed=embedDM)
                        
                        
                        # ส่งงาน
                        embedSubmit = nextcord.Embed()
                        embedSubmit.title = f'''ปั้ม {self.app['name']} สำเร็จ'''
                        embedSubmit.description = f'''
        :white_check_mark: `รายละเอียด `

        :mens: `ซื้อโดย` <@{interaction.user.id}>ㅤㅤ:money_with_wings:  `ราคา` : `{price} บาท`
        '''
                        embedSubmit.color = nextcord.Color.from_rgb(0, 255, 0)
                        embedSubmit.set_image(url=Config().Get()["embed"]["imglogo"])
                        try:
                            await self.bot.get_channel(int(Config().Get()['submitChannelId'])).send(embed=embedSubmit)
                        except Exception as error:
                            print('fail send message', str(error))
                        
                        embeAdmin = nextcord.Embed()
                        embeAdmin.title = f'''ปั้ม {self.app['name']} สำเร็จ'''
                        embeAdmin.color = nextcord.Color.from_rgb(0, 255, 0)
                        embeAdmin.description = f'''
        > `user`: <@{interaction.user.id}>
        > `status`: {self.app['name']}
        > `price`: {price} บาท
        > `amount`: {self.Input_amount.value}
        > `link`: {self.Input_link.value}
        > `time`: {str(datetime.now())}
        '''
                        try:
                            await self.bot.get_channel(int(Config().Get()['channelLikeLog'])).send(embed=embeAdmin)
                        except Exception as error:
                            print('fail send message', str(error))

                    else:
                        embed.title = '`❌﹕` สั่งซื้อไม่สำเร็จ'
                        embed.description = f'''
            คุณไม่สามารถสั่งซื้อสำเร็จได้
            หากคุณคิดว่านี้คือข้อผิดพลาดโปรดติดต่อผู้ดูเเลร้านค้า `{e['msg']}`
            '''
                        embed.color = nextcord.Color.from_rgb(255, 0, 0)
                    await self.message.edit(content=None,embed=embed)
                else:
                    need = price - userdata[str(interaction.user.id)]['point']
                    embed.description = f'คุณมียอดคงเหลือ {userdata[str(interaction.user.id)]["point"]} บาท\nต้องการทั้งหมด {price} บาท (ขาดอีก {need} บาท)'
                    embed.color = nextcord.Color.from_rgb(255, 0, 0)
                    await self.message.edit(content=None,embed=embed)
            else:
                embed.title = '`❌﹕` ไม่พบบัญชีในระบบ'
                embed.description = f'''
                คุณสามารถเปิดบัญชีด้วยการเติมเงินเท่าไหร่ก็ได้โดยใช้คําสั่ง ``/topup``
                หากคุณคิดว่านี้คือข้อผิดพลาดโปรดติดต่อผู้ดูเเลร้านค้า
                '''
                embed.color = nextcord.Color.from_rgb(255, 0, 0)
                await self.message.edit(content=None,embed=embed)
        else:
            embed.title = '`❌﹕` กรุณากรอกตัวเลข'
            embed.description = f'''
            คุณสามารถใช้งานได้แค่ตัวเลขเท่านั้น
            '''
            embed.color = nextcord.Color.from_rgb(255, 0, 0)
            await self.message.edit(content=None,embed=embed)



class appPremiumSellView(nextcord.ui.View):

    def __init__(self,bot, app,idlike, message: nextcord.Message):

        self.bot = bot
        self.app = app
        self.idlike = idlike
        self.message = message
        
        super().__init__(timeout=None)
        self.is_persistent()
    @nextcord.ui.button(
        label='ซื้อสินค้า',
        custom_id='buyproduct',
        style=nextcord.ButtonStyle.green,
        emoji='🛒'
    )
    async def buyproduct(self,button: nextcord.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(likeautofree(self.bot,self.app,self.idlike,message=self.message))



    @nextcord.ui.button(
        label='ยกเลิก',
        custom_id='appcancel',
        style=nextcord.ButtonStyle.red,
        emoji='❌'
    )
    async def appcancel(self, button: nextcord.Button, interaction: nextcord.Interaction):
        return await self.message.edit(embed=None,view=None,content='ยกเลิกสำเร็จ')

class appPremiumSelect(nextcord.ui.Select):

    def __init__(self, bot):
        self.bot = bot

        options = []

        for app in dtlike:
            options.append(nextcord.SelectOption(
                label=dtlike[app]["name"],
                value=app,
                description=f'{dtlike[app]["name"]} ({dtlike[app]["price"]} บาท  ต่อ 1 ไลค์)',
            ))

        super().__init__(
            custom_id='select-app-premium',
            placeholder='เลือกสินค้าที่คุณต้องการจะซื้อ',
            min_values=1,
            max_values=1,
            options=options
        )
        
        
        
    async def callback(self, interaction: nextcord.Interaction):
        message = await interaction.response.send_message(content='[SELECT] กำลังตรวจสอบ',ephemeral=True)
        id = self.values[0]
        app = dtlike[(self.values[0])]
        embed = nextcord.Embed()
        embed.title = app['name']
        embed.description = f'''
ราคา : ``{app['price']} บาท ต่อ 1ไลค์``
'''
        await interaction.message.edit(view=appPremiumView(bot=self.bot))
        embed.color = nextcord.Color.from_rgb(100, 255, 255)
        embed.set_image(url=Config().Get()["embed"]["imglogo"])
        await message.edit(embed=embed,view=appPremiumSellView(bot=self.bot,app=app,idlike=id,message=message), content=None)



class appPremiumView(nextcord.ui.View):

    def __init__(self, bot):
        super().__init__(timeout=None)
        self.add_item(appPremiumSelect(bot=bot))
        self.add_item(nextcord.ui.Button(style=nextcord.ButtonStyle.link, url="https://store.cyber-safe.pro/", label="Contect Me"))
        

class appPremiumCog(commands.Cog):

    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @nextcord.slash_command(
        name='setlikepremium',
        description='📌 | ติดตั้งระบบซื้อไลค์พรีเมี่ยม',
        guild_ids=[Config().Get()['serverId']]
    )
    async def apppremium(
        self,
        interaction: nextcord.Interaction
    ):
        if (interaction.user.id not in Config().Get()['ownerIds']):
            return await interaction.response.send_message(content='[ERROR] No Permission For Use This Command.', ephemeral=True)
        embed = nextcord.Embed()
        embed.title = 'BOT LIKE PREMIUM'
        embed.description = '>  บริการขาย LIKE PREMIUM ราคาถูกที่สุดในไทย\n> อ่านรายละเอียดเพิ่มเติมได้ที่ https://store.cyber-safe.pro/like\n\n# กดเลือกสินค้าที่คุณต้องการได้เลย'
        embed.color = nextcord.Color.from_rgb(255, 0, 0)
        embed.set_image(url=Config().Get()["embed"]["imglogo"])
        try:
            await interaction.channel.send(embed=embed, view=appPremiumView(bot=self.bot))
            await interaction.response.send_message(content='[SUCCESS] Done.', ephemeral=True)
        except Exception as error:
            await interaction.response.send_message(content='[ERROR] Fail To Send Message.', ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(appPremiumCog(bot=bot))
    bot.add_view(appPremiumView(bot=bot))