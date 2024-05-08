# ส่วนสำคัญเกี่ยวกับบอท ขายไลค์ปั้มไลค์
บอทปั้มไลค์แฮกไลค์เฟสบุ๊คบวกกำไรตั้งขายได้ของcybersafe ไลค์ไทยล้วนโครตถูก https://store.cyber-safe.pro/
## Installation
```bash
pip install -r requirements.txt
```
## สามารถสมัครเพื่อเอารหัสมาใส่ได้ที่ [https://store.cyber-safe.pro/](https://store.cyber-safe.pro/)
## ตั้งค่าส่วนต่างๆ
```json
{
    "botToken": "token โทเคนบอทของเราจากดิสคอร์ด",
    "commnadPrefix": "!",
    "serverId": "ไอดีเซิฟเวอร์ของเรา",
    "ownerIds": [
        "ไอดีแอดมินที่จะใช้บอทได้",
		"99999999999999"
    ],
    "channelTopupLog": "ไอดีห้องที่ไว้แจ้งเตือนเมื่อคนเติมเงิน",
    "channelLikeLog": "ไอดีห้องที่ไว้แจ้งเตือนให้แอดมินรู้ว่าใครซื้ออะไร",
    "submitChannelId": "ไอดีห้องที่ไว้แจ้งเตือนให้คนอื่นรู้ว่าใครซื้ออะไร",
    "roleAddEnable": false or true ถ้าต้องการให้ยศเขาเมื่อซื้อใส่ให้้ใส่ true,
    "roleAddRoleId": ถ้าใส่trueส่วนนี้จะใส่ไอดียศ,
    "phoneNumber": "เบอร์ที่ไว้รับเงินอังเปา",
    "embed": {
        "imglogo": "โลโก้ไว้โชว์ตอนใช้คำสั่ง"
    },
    "configweb": {
        "username": "ชื่อในเว็บcybersafe",
        "password": "รหัสจากเว็บcybersafe",
        "token": "ส่วนนี้ไม่ต้องแก้ไข",
		"dtlike": {
            "1": {
                "name": "ไลค์",
                "price": 0.2
            },
            "2": {
                "name": "ใจ",
                "price": 0.3
            },
            "3": {
                "name": "ว้าว",
                "price": 0.3
            },
            "4": {
                "name": "ขำ",
                "price": 0.3
            },
            "5": {
                "name": "เศร้า",
                "price": 0.3
            },
            "6": {
                "name": "โกรธ",
                "price": 0.3
            }
        } 
	}
}

```


## วิธีการตั้งค่าราคา
### ราคาสามารถแก้ไขเพิ่มเติมจากส่วนนี้ได้
price สามารถแก้ไขราคาเพิ่มเติมได้เรทต่อ1ไลค์

![ราคาจากหน้าเว็บ](https://i.ibb.co/MVH38Fm/2024-03-08-172456.png)


## วิธีการทำงาน
```bash
python main.py
```
# หรือหากต้องการใช้งานบน replit สามารถใช้งานได้ที่
https://replit.com/@sakol289/likestorecybersafeconfigprice?v=1

# หากมีปัญหาติดต่อช่องทางได้ตามนี้

## FB : [cybersafe](https://fb.me/cybersafe01)

## DISCORD : [cybersafe](https://cyber-safe.pro/discord)

##  WEB : [cybersafe](https://cyber-safe.pro)

