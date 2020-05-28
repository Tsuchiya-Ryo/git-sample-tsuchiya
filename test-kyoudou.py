class Car:
    def__init(self, color="white", maker="toyota"):
        self.color = color
        self.maker =maker
    
    def drive(self, km):
        self.mileage += km
        msg = f"{km}kmドライブしました。総距離は{self.mileage}kmです。"
        print(msg)

