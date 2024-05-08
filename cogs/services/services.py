import nextcord, json, requests, re
from nextcord.ext import commands
from bs4 import BeautifulSoup
from datetime import datetime
from Config import Config
from utils.Newlike import Newlike
from bs4 import BeautifulSoup



class services(nextcord.ui.Modal):
    def __init__(self,bot,app,idapp,message: nextcord.Message):
        self.bot = bot
        self.app = app
        self.idapp = idapp
        self.message = message
        self.allservices = Config("database/services.json").Get()
        super().__init__(auto_defer=True, title="Verify")
        self.Input_link = nextcord.ui.TextInput(
            label="ลิ้งที่รับบริการ",
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
                price = (self.app["new_price"] / 1000) * float(self.Input_amount.value)
                await self.message.edit(content=f"ซื้อ {self.app['name']} price {price}")
                Dtservices = self.allservices[self.app["id"]]
                # print(Dtservices.json()["result"][0]["amount"])
                if(Dtservices["min"] < float(self.Input_amount.value) or Dtservices["max"] > float(self.Input_amount.value)):
                    if (userdata[str(interaction.user.id)]['point'] >= price):
                        reponse = Newlike(Config().Get()['configapi']['apikey']).Order(self.app["id"],self.Input_link.value,self.Input_amount.value)
                        e1 = reponse.json()
                        e = e1.get("status")
                        print(e)
                        # ใช้ BeautifulSoup เพื่อลบ HTML tags
                        # print(e)
                        if e is not None:
                            if e == "success":
                                t_detali = f"order {e1['order']}"
                                userdata[str(interaction.user.id)]['point'] -= price
                                userdata[str(interaction.user.id)]['spend'] += price
                                userdata[str(interaction.user.id)]['history'].append({
                                    "type": "buyapp",
                                    "item": f"idapp_{self.app['id']}",
                                    "price": price,
                                    "description": f"auto {self.app['name']} price {price} name {self.app['name']}",
                                    "time": str(datetime.now()),
                                })
                                json.dump(userdata, open('./database/users.json', 'w', encoding='utf-8'), indent=4, ensure_ascii=False)
                                    
                                embed.title = '``✅`` ซื้อสินค้าสำเร็จ'
                                embed.description = f'''บอทได้ส่งข้อมูลไปยังแชทส่วนตัวของคุณแล้ว\nยอดเงินคงเหลือ : `` {userdata[str(interaction.user.id)]["point"]} ``'''
                                embed.color = nextcord.Color.from_rgb(0, 255, 0)

                                embedDM = nextcord.Embed()
                                embedDM.title = f'''ซื้อ {self.app['name']} สำเร็จ'''
                                embedDM.color = nextcord.Color.from_rgb(0, 255, 0)
                                embedDM.set_image(url=Config().Get()["embed"]["imglogo"])
                                embedDM.description = f'''
                > `user`: <@{interaction.user.id}>
                > `app`: {self.app['name']}
                > `price`: {price} บาท
                > `amount`: {self.Input_amount.value}
                > `detali`: {t_detali}
                > `time`: {str(datetime.now())}
                '''
                                await interaction.user.send(embed=embedDM)
                                
                                
                                # ส่งงาน
                                embedSubmit = nextcord.Embed()
                                embedSubmit.title = f'''ซื้อ {self.app['name']} สำเร็จ'''
                                embedSubmit.description = f'''
                :mens: `ซื้อโดย` <@{interaction.user.id}>ㅤㅤ:money_with_wings:  `ราคา` : `{price} บาท`
                '''
                                embedSubmit.color = nextcord.Color.from_rgb(0, 255, 0)
                                embedSubmit.set_image(url=Config().Get()["embed"]["imglogo"])
                                try:
                                    await self.bot.get_channel(int(Config().Get()['submitChannelId'])).send(embed=embedSubmit)
                                except Exception as error:
                                    print('fail send message', str(error))
                                
                                embeAdmin = nextcord.Embed()
                                embeAdmin.title = f'''ซื้อ {self.app['name']} สำเร็จ'''
                                embeAdmin.color = nextcord.Color.from_rgb(0, 255, 0)
                                embeAdmin.description = f'''
                > `user`: <@{interaction.user.id}>
                > `status`: {self.app['name']}
                > `price`: {price} บาท
                > `amount`: {self.Input_amount.value}
                > `detali`: {t_detali}
                > `time`: {str(datetime.now())}
                '''
                                try:
                                    await self.bot.get_channel(int(Config().Get()['channelserviceLog'])).send(embed=embeAdmin)
                                except Exception as error:
                                    print('fail send message', str(error))
                        else:
                            embed.title = '`❌﹕` สั่งซื้อไม่สำเร็จ'
                            embed.description = f'''
                คุณไม่สามารถสั่งซื้อสำเร็จได้
                หากคุณคิดว่านี้คือข้อผิดพลาดโปรดติดต่อผู้ดูเเลร้านค้า `{e1}`
                '''
                            embed.color = nextcord.Color.from_rgb(255, 0, 0)
                        await self.message.edit(content=None,embed=embed)
                    else:
                        need = price - userdata[str(interaction.user.id)]['point']
                        embed.description = f'คุณมียอดคงเหลือ {userdata[str(interaction.user.id)]["point"]} บาท\nต้องการทั้งหมด {price} บาท (ขาดอีก {need} บาท)'
                        embed.color = nextcord.Color.from_rgb(255, 0, 0)
                        await self.message.edit(content=None,embed=embed)
                else:
                    embed.title = '`❌﹕` กรุณาใส่จำนวนให้ถูกต้อง'
                    embed.description = f'''
            คุณไม่สามารถสั่งซื้อสำเร็จได้
            กรุณาใส่จำนวนไม่น้อยกว่า {Dtservices["min"]} และไม่มากกว่า {Dtservices["max"]}
            หากคุณคิดว่านี้คือข้อผิดพลาดโปรดติดต่อผู้ดูเเลร้านค้า
            '''
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

class order(nextcord.ui.Modal):
    def __init__(self,bot):
        self.bot = bot
        super().__init__(auto_defer=True, title="Verify")
        self.order = nextcord.ui.TextInput(
            label="ใส่ id order",
            style=nextcord.TextInputStyle.short,
            required=True,
            placeholder="ใส่ id order",
        )
        self.add_item(self.order)
            
    async def callback(self, interaction: nextcord.Interaction):
        await interaction.send(f"send",delete_after=0)
        reponse = Newlike(Config().Get()['configapi']['apikey']).Status(self.order.value)
        e = reponse.json()
        t_detali = e
        e = e.get("status")
        # print(t_detali)
        # ใช้ BeautifulSoup เพื่อลบ HTML tags
        # print(e)
# > `order`:  {self.order.value}
# > `status`: {t_detali["status"]}
# > `time`: {str(datetime.now())}
        if e is not None:
                embed = nextcord.Embed()
                embed.title = f'''เช็ค status สำเร็จ'''
                embed.color = nextcord.Color.from_rgb(0, 255, 0)
                embed.set_image(url=Config().Get()["embed"]["imglogo"])
                embed.description = f'''
# > `order`:  {self.order.value}
# > `status`: {t_detali["status"]}
# > `time`: {str(datetime.now())}
                '''

                # ส่ง embed ไปยังผู้ใช้
                await interaction.user.send(content=None, embed=embed)
        else:
            embed = nextcord.Embed()
            embed.title = '`❌﹕` เช็คไม่สำเร็จ'
            embed.description = f'''
คุณไม่สามารถเช็คorderได้
หากคุณคิดว่านี้คือข้อผิดพลาดโปรดติดต่อผู้ดูเเลร้านค้า `{e}`
'''
            embed.color = nextcord.Color.from_rgb(255, 0, 0)
            # await self.message.edit(content=None,embed=embed)
            await interaction.user.send(content=None,embed=embed)
            



class appPremiumSellView(nextcord.ui.View):

    def __init__(self,bot, app,idapp, message: nextcord.Message):

        self.bot = bot
        self.app = app
        self.idapp = idapp
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
        await interaction.response.send_modal(services(self.bot,self.app,self.idapp,message=self.message))



    @nextcord.ui.button(
        label='ยกเลิก',
        custom_id='appcancel',
        style=nextcord.ButtonStyle.red,
        emoji='❌'
    )
    async def appcancel(self, button: nextcord.Button, interaction: nextcord.Interaction):
        return await self.message.edit(embed=None,view=None,content='ยกเลิกสำเร็จ')

class ServicesSelect(nextcord.ui.Select):

    def __init__(self, bot):
        self.bot = bot
        self.allservices = Config("database/services.json").Get()

        options = []

        for app in self.allservices:
            options.append(nextcord.SelectOption(
                label=self.allservices[app]["name"],
                value=app,
                description=f'{self.allservices[app]["name"]} ({self.allservices[app]["new_price"]} บาท  ต่อ 1000)',
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
        app = self.allservices[(self.values[0])]
        embed = nextcord.Embed()
        embed.title = app['name']
        embed.description = f'''
คำอธิบาย : ```{app['msg']}```
จำนวนต่ำสุด : ``{app['min']}``
จำนวนมากสุด : ``{app['max']}``
ราคาต่อ1000 : ``{app['new_price']} บาท``

'''
        await interaction.message.edit(view=ServicesView(bot=self.bot))
        embed.color = nextcord.Color.from_rgb(100, 255, 255)
        # print(app["img"])
        # embed.set_image(url=app["img"])
        await message.edit(embed=embed,view=appPremiumSellView(bot=self.bot,app=app,idapp=id,message=message), content=None)



class ServicesView(nextcord.ui.View):

    def __init__(self, bot):
        super().__init__(timeout=None)
        self.add_item(ServicesSelect(bot=bot))
        self.add_item(nextcord.ui.Button(style=nextcord.ButtonStyle.link, url=Config().Get()["contectlink"], label="Contect Me"))
        self.bot = bot
        


    @nextcord.ui.button(
        label='🏧เช็ค status order',
        custom_id='order',
        style=nextcord.ButtonStyle.blurple,
        row=1
    )
    async def order(
        self,
        button: nextcord.Button,
        interaction: nextcord.Interaction
    ):
        await interaction.response.send_modal(order(self.bot))


class appPremiumCog(commands.Cog):

    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @nextcord.slash_command(
        name='setservices',
        description='📌 | ติดตั้งระบบซื้อ new like',
        guild_ids=Config().Get()['serverId']
    )
    async def apppremium(
        self,
        interaction: nextcord.Interaction
    ):
        if (interaction.user.id not in Config().Get()['ownerIds']):
            return await interaction.response.send_message(content='[ERROR] No Permission For Use This Command.', ephemeral=True)
        embed = nextcord.Embed()
        embed.title = 'บริการปั้มต่างๆ new like'
        embed.description = f'>  บริการขาย เพิ่มยอดติดตาม ไลค์ วิว ราคาถูกที่สุดในไทย\n> อ่านรายละเอียดเพิ่มเติมได้ที่ {Config().Get()["contectlink"]}\n\n# กดเลือกสินค้าที่คุณต้องการได้เลย'
        embed.color = nextcord.Color.from_rgb(255, 0, 0)
        embed.set_image(url=Config().Get()["embed"]["imglogo"])
        try:
            await interaction.channel.send(embed=embed, view=ServicesView(bot=self.bot))
            await interaction.response.send_message(content='[SUCCESS] Done.', ephemeral=True)
        except Exception as error:
            print(error)
            await interaction.response.send_message(content='[ERROR] Fail To Send Message.', ephemeral=True)
            



def setup(bot: commands.Bot):
    bot.add_cog(appPremiumCog(bot=bot))
    bot.add_view(ServicesView(bot=bot))
