import json

class Config:
    
    __file = None
    
    def __init__(self, file: str = 'config.json') -> None:
        self.__file = file
        
        
    def Get(self):
        with open(self.__file, 'r',encoding="utf-8") as f:
            return json.load(f)

    def saveConfig(self, data):
        with open(self.__file, 'w', encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    
    def insertConfig(self, *keys, value):
        try:
            data = self.Get()
            current_dict = data
            for key in keys[:-1]:
                current_dict = current_dict.setdefault(key, {})
            oldValue = current_dict[keys[-1]]
            if type(oldValue) == list:
                oldValue.append(value)
            else:
                oldValue = value
            current_dict[keys[-1]] = oldValue
            self.saveConfig(data)
            return [True]
        except Exception as e:
            return [False,e]

    def removeConfig(self, *keys, value_to_remove):
        try:
            data = self.Get()
            current_dict = data
            for key in keys[:-1]:
                current_dict = current_dict.setdefault(key, {})
            list_to_update = current_dict.get(keys[-1], [])

            if value_to_remove in list_to_update:
                list_to_update.remove(value_to_remove)

            current_dict[keys[-1]] = list_to_update
            self.saveConfig(data)
            return [True]
        except Exception as e:
            return [False,e]

    def updateConfig(self, *keys, value_to_update):
        try:
            data = self.Get()
            current_dict = data
            for key in keys[:-1]:
                current_dict = current_dict.setdefault(key, {})
            
            # ตรวจสอบว่าค่าที่ต้องการอัปเดตมีอยู่หรือไม่
            if keys[-1] in current_dict:
                # อัปเดตค่าที่มีอยู่
                current_dict[keys[-1]] = value_to_update
            else:
                # สร้างคีย์และค่าใหม่
                current_dict[keys[-1]] = value_to_update
            
            # บันทึกการเปลี่ยนแปลงลงในไฟล์
            self.saveConfig(data)
            return [True]
        except Exception as e:
            return [False,e]

