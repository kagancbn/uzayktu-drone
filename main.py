from dronekit import connect, VehicleMode, LocationGlobalRelative,Command
import hareketler.alanTara as alanTarama
import hareketler.genelHareketler as genelHareketler
#import insanTespit.insanTespit as insanTespit
import threading
import test
import time
import re
import multiprocessing
from pymavlink import mavutil

def connectToVehicle():
	iha = connect('127.0.0.1:14550', wait_ready=True) # 127.0.0.1:14550 -> değiştirilecek
	return iha

# def komutDinle(iha):
# 	# Listen for `STATUSTEXT` messages
# 	@iha.on_message('STATUSTEXT')
# 	def handle_statustext_message(self, name, message):
#     	text = message.text
#     	if text.startswith("commandGCS:"):
#         	print("Received command:", text)
# 			print("2")
#     # Wait for messages
#     while True:
#         time.sleep(1)

# def komutDinle2(iha):
# 	@iha.on_message('STATUSTEXT')
# 	def handle_statustext_messages(self,name,message):
# 		text = message.text
# 		if text.startswith("commandGCS:"):
# 			print("Received Command:", text)
# 			if("alanTaraKare" in text):
# 				alanTaramaThread.start()
# 				tespitThread.start()
# 			elif("yuvarlakTara" in text):
# 				alan




# ihaya bağlan
iha = connectToVehicle()

################################### YER İSTASYONU İLETİŞİM KODU ##################################
# @iha.on_message('STATUSTEXT')
# def handle_statustext_message(self, name, message):
# 	text = message.text
# 	if text.startswith("commandGCS:"):
# 		# Process the message
# 		print("Received command:", text)
# 		if("alanTaraKare" in text):
# 			# değişkenleri topla
# 			text = re.findall(r"\,(.*?),", text)
# 			# eğer zaten istenen yükseklikteyse direkt istenen konuma git
# 			if(iha.location.global_relative_frame.alt >= float(text[2]) * 0.90):
# 				genelHareketler.konumaGit(iha,konum)
# 			else:
# 				genelHareketler.takeoff(15,iha)
# 				konum = LocationGlobalRelative(text[0],text[1],10)
# 				genelHareketler.konumaGit(iha,konum)

# 			konum = LocationGlobalRelative(text[0],text[1], 10) # enlem, boylam, yükseklik
# 			# threadleri tanımla
# 			tespitThread = threading.Thread(target=insanTespit.main,args=iha)
# 			alanTaramaThread = threading.Thread(target=alanTarama.alanTaraKare,args=(text[2], iha, konum)) # uzunluk, iha, konum

# 			# threadleri başlat
# 			tespitThread.start()
# 			time.sleep(5) # kamera açılana kadar bekle
# 			alanTaramaThread.start()

# 		elif("RTL" in text):
# 			if tespitThread.is_alive():
# 				tespitThread.stopped = True
# 				tespitThread.join()
# 			if alanTaramaThread.is_alive():
# 				alanTaramaThread.stopped = True
# 				alanTaramaThread.join()
# 			iha.mode = VehicleMode("RTL")
# 		elif("BRAKE" in text):
# 			if tespitThread.is_alive():
# 				tespitThread.stopped = True
# 				tespitThread.join()
# 			if alanTaramaThread.is_alive():
# 				alanTaramaThread.stopped = True
# 				alanTaramaThread.join()
# 			iha.mode = VehicleMode("BRAKE")
# 		elif("LAND" in text):
# 			if tespitThread.is_alive():
# 				tespitThread.stopped = True
# 				tespitThread.join()
# 			if alanTaramaThread.is_alive():
# 				alanTaramaThread.stopped = True
# 				alanTaramaThread.join()
# 			iha.mode = VehicleMode("LAND")


# while True:
# 	time.sleep(1)
########################################################################################


#kalkış yap
genelHareketler.takeoff(3,iha)

#konumu tanımla
konum = iha.location.global_relative_frame # -> güncel konum

#threadleri tanımla
#alanTaramaThread = threading.Thread(target=alanTarama.alanTaraKare,args=(10,iha,konum)) # kare -> çevre, yuvarlak -> çap veya yarıçap
#tespitThread = threading.Thread(target=insanTespit.main,args=iha)


# konuma git
#genelHareketler.konumaGit(iha,konum)

# alanı taramaya başla.
#tespitThread.start()
#time.sleep(5) # kameranın açılmasını bekle
#alanTaramaThread.start()
alanTarama.alanTaraKare(20,iha,konum)


smallMove = 0.000009

konum.alt = 3
while True:
	if(iha.mode == "BRAKE"):
		#iha.simple_goto(konum)
		
		time.sleep(5)
		komut = iha.commands
		komut.clear()
		time.sleep(1)
		komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, konum.lat, konum.lon, 3))
		#komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, konum.lat, konum.lon, 0))
		time.sleep(1)
		komut.upload()
		print("Komutlar yukleniyor")
		iha.mode=VehicleMode("AUTO")
		print("gidiyom bn")
		break
		

while((iha.location.global_relative_frame.lat < konum.lat + smallMove and iha.location.global_relative_frame.lat > konum.lat - smallMove 
      and iha.location.global_relative_frame.lon < konum.lon + smallMove and iha.location.global_relative_frame.lon > konum.lon - smallMove)) is not True:
	time.sleep(1)
	print("bekleniyor.")

iha.mode = VehicleMode("LAND")

exit()
