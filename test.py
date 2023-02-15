from dronekit import connect, VehicleMode, LocationGlobalRelative, Command
import hareketler.genelHareketler as genelHareketler
import time

def hareketiKesVeGeriGit(iha):

    time.sleep(10)
    
    print("Hedefe ulaşıldı")
    # vehicle parametresini buraya import edip taramayı durdur
    genelHareketler.dur(iha)
    time.sleep(3)
    # bir kaç metre geri git
    genelHareketler.geri(iha)

    print("servo calistiriliyor")
    time.sleep(2)

    print("eve donuluyor")
    genelHareketler.eveDon(iha)

