import nextcord, httpx, certifi, json, datetime, re
from nextcord.ext.commands import Bot, Cog
from Config import Config

class topupModal(nextcord.ui.Modal):

    def __init__(self, bot: Bot):

        super().__init__(
            title='เติมเงิน ( ไม่มีการคืนเงิน )',
            timeout=None,
            custom_id='topup-page-modal'
        )

        self.link = nextcord.ui.TextInput(
            label='ลิ้งค์ซองอังเปา',
            custom_id='link',
            style=nextcord.TextInputStyle.short,
            placeholder='https://gift.truemoney.com/campaign/?v=xxxxxxxxxxxxxxxxxxxxxxxxxxx'
        )

        self.add_item(self.link)

        self.bot = bot

    async def callback(self, interaction: nextcord.Interaction) -> None:
        
        await interaction.response.defer(ephemeral=True)

        link = str(self.link.value)

        if (not re.match(r"https:\/\/gift\.truemoney\.com\/campaign\/\?v=+[a-zA-Z0-9]{18}", link)):
            embed = nextcord.Embed()
            embed.title = '❌ เติมเงินไม่สำเร็จ'
            embed.description = f'''ลิงค์อั่งเปาไม่ถูกต้อง'''
            embed.color = nextcord.Color.red()
            return await interaction.send(embed=embed, ephemeral=True)

        voucher_hash = link.split('?v=')[1]

        response = httpx.post(
            url = f'https://gift.truemoney.com/campaign/vouchers/{voucher_hash}/redeem',
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/8a0.0.3987.149 Safari/537.36'},
            json = {'mobile': Config().Get()["phoneNumber"],'voucher_hash': f'{voucher_hash}'},
            verify=certifi.where(),
        )
        if (response.status_code == 200 and response.json()['status']['code'] == 'SUCCESS'):
            data = response.json()
            amount = int(float(data['data']['my_ticket']['amount_baht']))

            userJSON = json.load(open('./database/users.json', 'r', encoding='utf-8'))
            if (str(interaction.user.id) not in userJSON):
                userJSON[str(interaction.user.id)] = {
                    'userId': interaction.user.id,
                    'point': amount,
                    'all-point': amount,
                    'spend': 0,
                    'history': [
                        {
                            'type': 'user-topup',
                            'link': link,
                            'amount': amount,
                            'time': str(datetime.datetime.now())
                        }
                    ]
                }
            else:
                userJSON[str(interaction.user.id)]['point'] += amount
                userJSON[str(interaction.user.id)]['all-point'] += amount
                userJSON[str(interaction.user.id)]['history'].append({
                    'type': 'user-topup',
                    'link': link,
                    'amount': amount,
                    'time': str(datetime.datetime.now())
                })
            json.dump(userJSON, open('./database/users.json', 'w', encoding='utf-8'), indent=4, ensure_ascii=False)

            channel = self.bot.get_channel(int(Config().Get()['channelTopupLog']))
            if (channel):
                embed = nextcord.Embed(
                    title='เติมเงิน',
                    description=f'''
ผุ้ใช้ : <@{interaction.user.id}> ได้เติมเงินจำนวน ``{amount}`` บาท
ลิ้งค์ซอง 🧧 : {link}\n
เวลา : `{datetime.datetime.now()}`
''',
                    color=nextcord.Color.green()
                )
                await channel.send(embed=embed)
            if (Config().Get()['roleAddEnable'] == True):
                role = nextcord.utils.get(interaction.user.guild.roles, id = int(Config().Get()['roleAddRoleId']))
                if (role):
                    await interaction.user.add_roles(role)
            embed = nextcord.Embed(
                title='✅ เติมเงินสำเร็จ',
                description=f'''คุณเติมเงินจํานวน {amount} บาท สำเร็จ''',
                color=nextcord.Color.green()
            )
            return await interaction.send(embed=embed, ephemeral=True)
        else:
            embed = nextcord.Embed(
                title='❌ เติมเงินไม่สำเร็จ',
                description='บอทไม่สามารถรับอั่งเปาซองนี้ได้หากคุณคิดว่านี้คือข้อผิดพลาดโปรดติดต่อผู้ดูเเลร้านค้า',
                color=nextcord.Color.red()
            )
            return await interaction.send(embed=embed, ephemeral=True)
        
class topupView(nextcord.ui.View):

    def __init__(self, bot: Bot) -> None:

        super().__init__(timeout=None, auto_defer=True)
        self.bot = bot

    @nextcord.ui.button(
        label='🏧เช็คเงินคงเหลือ',
        custom_id='balance',
        style=nextcord.ButtonStyle.blurple,
        row=1
    )
    async def balance(
        self,
        button: nextcord.Button,
        interaction: nextcord.Interaction
    ):
        userJSON = json.load(open('./database/users.json', 'r', encoding='utf-8'))
        if (str(interaction.user.id) in userJSON):
            embed = nextcord.Embed(
                description=f'ยอดเงินคงเหลือ {userJSON[str(interaction.user.id)]["point"]} บาท',
                color=nextcord.Color.from_rgb(50, 215, 255)
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = nextcord.Embed(
                description='โปรดเติมเงินเพื่อเปิดบัญชี',
                color=nextcord.Color.from_rgb(50, 215, 255)
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @nextcord.ui.button(
        label='[ 🧧 ] เติมเงิน',
        custom_id='topup',
        style=nextcord.ButtonStyle.green,
        row=1
    )
    async def topup(
        self,
        button: nextcord.Button,
        interaction: nextcord.Interaction
    ):
        return await interaction.response.send_modal(topupModal(bot=self.bot))
    
class topupCog(Cog):

    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot = bot

    @nextcord.slash_command(
        name='topup-setup',
        description='setup topup embed',
        guild_ids=Config().Get()['serverId']
    )
    async def setup(
        self,
        interaction: nextcord.Interaction
    ):
        if (interaction.user.id in Config().Get()['ownerIds']):
            embed = nextcord.Embed(
                title='ระบบเติมเงินรวม',
                description='กดปุ่มด้านล่างเพื่อ เติมเงินเข้าระบบ',
                color=nextcord.Color.from_rgb(50, 215, 255)
            )
            embed.set_image(url='https://media.discordapp.net/attachments/970624157966540851/1030754839602397264/unknown_3.jpg')
            await interaction.channel.send(embed=embed, view=topupView(self.bot))
            await interaction.response.send_message(content='success', ephemeral=True)
        else:
            await interaction.response.send_message(content='fail', ephemeral=True)
           

def setup(bot: Bot):
    bot.add_cog(topupCog(bot=bot))
    bot.add_view(topupView(bot=bot))
    # pass