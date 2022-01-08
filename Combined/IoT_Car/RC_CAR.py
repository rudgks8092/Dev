from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtSql
import time
import sys
sys.path.append('./Raspi-MotorHAT-python3')
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
from Raspi_PWM_Servo_Driver import PWM
import atexit
from picamera import PiCamera
from sense_hat import SenseHat


db = QtSql.QSqlDatabase.addDatabase('QMYSQL',"TEST")
db.setHostName("ec2-3-34-192-207.ap-northeast-2.compute.amazonaws.com")
db.setDatabaseName("2-3")
db.setUserName("ssafy2_3")
db.setPassword("ssafy1234")

class pollingThread(QThread):
    def __init__(self):
        super().__init__()
        #print("START")
    def run(self):
        
        
        self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL',"TESTTHREAD")
        self.db.setHostName("ec2-3-34-192-207.ap-northeast-2.compute.amazonaws.com")
        self.db.setDatabaseName("2-3")
        self.db.setUserName("ssafy2_3")
        self.db.setPassword("ssafy1234")       
        print(self.db)
        ok = self.db.open()
        self.query = QtSql.QSqlQuery(self.db)
        self.mh = Raspi_MotorHAT(addr=0x6f)
        self.myMotor = self.mh.getMotor(2)
        self.myMotor.setSpeed(100)
        self.pwm = PWM(0x70)
        self.pwm.setPWMFreq(60)
        self.sense = SenseHat()
        
        while True:
            time.sleep(0.1)
            self.getQuery()
            self.setQuery()
        
        
    def getQuery(self):
        result = self.query.exec("select * from command_1 order by time desc limit 1");
        self.query.next()
        cmdTime = self.query.record().value(0)
        cmdType = self.query.record().value(1)
        cmdArg = self.query.record().value(2)
        is_finish = self.query.record().value(3)
        #print("is_finish = " + str(is_finish))
        #record = query.record()
        #str1 = "%s | %10s | %10s | %4d" % (record.value(0).toString(), record.value(1), record.value(2), record.value(3))
        #print(str1)
        if is_finish == 0 :
            #update
            #query = QtSql.QSqlQuery("update command_1 set is_finish=1 where is_finish=0");
            #print(cmdTime, cmdType, cmdArg)
            #detect new command
            print(cmdTime.toString(), cmdType, cmdArg)
            result = self.query.exec("update command_1 set is_finish=1 where is_finish=0");
            if cmdType == "go": self.go()
            if cmdType == "back": self.back()
            if cmdType == "left": self.left()
            if cmdType == "right": self.right()
            if cmdType == "mid": self.mid()
            if cmdType == "front" and cmdArg == "press" :
                self.go()
                self.middle()
            if cmdType == "leftside" and cmdArg == "press" :
                self.go()
                self.left()
            if cmdType == "rightside" and cmdArg == "press" :
                self.go()
                self.right()
            if cmdType == "front" and cmdArg == "release" : self.stop()
            if cmdType == "leftside" and cmdArg == "release" : self.stop()
            if cmdType == "rightside" and cmdArg == "release" : self.stop()
    def setQuery(self):
        pressure = self.sense.get_pressure()
        temp = self.sense.get_temperature()
        humidity = self.sense.get_humidity()
            
        p = round((pressure-1000)/100,3)
        t = round(temp/100, 3)
        h = round(humidity/100,3)
        
        self.query.prepare("insert into sensing_1 (time, num1, num2, num3, meta_string, is_finish) values (time, :num1, :num2, :num3, :meta, :finish)");
        time = QDateTime().currentDateTime()
        self.query.bindValue(":time", time)
        self.query.bindValue(":num1", p)
        self.query.bindValue(":num2", t)
        self.query.bindValue(":num3", h)
        self.query.bindValue(":meta","")
        self.query.bindValue(":finish", 0)
        self.query.exec()
        
        a = int((p * 1271) % 256)
        b = int((t * 1271) % 256)
        c = int((h * 1271) % 256)
        self.sense.clear(a,b,c)
    def stop(self):
        print("MOTOR STOP")
        self.myMotor.run(Raspi_MotorHAT.RELEASE)
    def go(self):
        print("MOTOR GO")
        self.myMotor.setSpeed(100)
        self.myMotor.run(Raspi_MotorHAT.FORWARD)

    def back(self):
        print("MOTOR BACK")
        self.myMotor.setSpeed(100)
        self.myMotor.run(Raspi_MotorHAT.BACKWARD)
        
    def left(self):
        print("MOTOR LEFT")
        self.pwm.setPWM(0, 0, 270)
    def right(self):
        print("MOTOR RIGHT")
        self.pwm.setPWM(0, 0, 430)
    def mid(self):
        print("MOTOR MIDDLE")
        self.pwm.setPWM(0, 0, 350)
        self.myMotor.run(Raspi_MotorHAT.RELEASE)
        
camera = PiCamera()
camera.resolution = (500,500)
def cameraCapture():    
    camera.capture('/home/pi/image.jpg')
ok = db.open()
th = pollingThread()
th.start()

#timer = QTimer()
#timer.setInterval(500)
#timer.timeout.connect(cameraCapture)
#timer.start()

#app = QApplication([])

#infinity loop
mainQuery = QtSql.QSqlQuery(db)
cnt  = 0
while True:
    cameraCapture()
    inByteArray = QByteArray()
    file = QFile()
    QDir.setCurrent("/home/pi")
    file.setFileName("image.jpg")
    file.open(QIODevice.ReadOnly)
    inByteArray = file.readAll()
   # if cnt >= 5:
   #     cnt = 0
   #     mainQuery.exec("truncate test_blob")
    #result = self.query.exec("update command_1 set is_finish=1 where is_finish=0");
    mainQuery.prepare("update test_blob set image=:image")
    #mainQuery.prepare("insert into test_blob (image, time) values(:image, :time)")
    mainQuery.bindValue(":image",inByteArray)
    #time1 = QDateTime().currentDateTime()
    #mainQuery.bindValue(":time",time1)
    
    res = mainQuery.exec()
    if not res:
        print(self.query.lastError().text())
    cnt += 1
    
