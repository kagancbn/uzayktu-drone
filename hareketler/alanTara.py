import time
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command
from math import sin, cos, radians, degrees, asin,atan2
from pymavlink import mavutil

bigMove = 0.00009 # 10 metre
smallMove = 0.000045 # 5 metre

movementConstant = 0.00001 # 1.1 metre
# *todo gcs için değişkenler eklenmeli
def alanTaraKare(uzunluk, iha, ilkKonum):
    
    komut = iha.commands

    komut.clear()
    time.sleep(1)

    komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 0, 3))

    komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, ilkKonum.lat, ilkKonum.lon, 3))


    uzunlukDunya = uzunluk*movementConstant
    iterasyon=uzunluk/5
    i=0
    lat = iha.location.global_relative_frame.lat
    lon = iha.location.global_relative_frame.lon
    
    while(i<iterasyon):
        # enlem hareket
        lat = lat + uzunlukDunya
        komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, lat, lon, 3))
        
        # boylam hareket
        lon= lon + smallMove
        komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, lat, lon, 3))

        # hareket yönü çevrimi
        uzunlukDunya=-uzunlukDunya
        i=i+1
        

    komut.upload()
    print("Komutlar yukleniyor")
    iha.parameters['WPNAV_SPEED'] = 500       
    iha.mode=VehicleMode("AUTO")
    # while (iha.mode==VehicleMode("AUTO")):
    #     next_waypoint = komut.next
    #     print("Next command : %s " % next_waypoint)
    #     time.sleep(2)

def getSiradakiKonum(original_location, bearing, distance):
    """
    Returns a LocationGlobal object containing the latitude/longitude `distance` meters from the 
    specified `original_location` at the specified `bearing` (in degrees).
    """
    earth_radius = 6378137.0  # radius of the earth in meters
    d = distance/earth_radius  # angular distance in radians
    bearing = radians(bearing)
    lat1 = radians(original_location.lat)
    lon1 = radians(original_location.lon)

    lat2 = asin(sin(lat1) * cos(d) + cos(lat1) * sin(d) * cos(bearing))
    lon2 = lon1 + atan2(sin(bearing) * sin(d) * cos(lat1), cos(d) - sin(lat1) * sin(lat2))

    return LocationGlobalRelative(degrees(lat2), degrees(lon2), original_location.alt)

def yuvarlakTara(radius, iha):
    center_point = LocationGlobalRelative(iha.location.global_relative_frame.lat, iha.location.global_relative_frame.lon, 15)
    print(center_point)
    # Define the radius of the circle
    #radius = 10 # in meters
    #vehicle.simple_takeoff(15)
    # Fly in a circular pattern around the center point
    
    for i in range(36):
        #print(i)
        # Calculate the next point on the circle
        theta = i * 10
        new_point = getSiradakiKonum(center_point, theta, radius)
        print(new_point)
        new_point.alt=15
        # Move the drone to the new point
        #drone.simple_goto(new_point)
        #komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, new_point.lat, new_point.lon, 15))
        iha.simple_goto(new_point)
        time.sleep(2)

        #time.sleep(10)
        # Wait for the drone to reach the new point
        #while drone.mode.name=="GUIDED":
        #    time.sleep(1)
    #komut.upload()
    print("Komutlar yukleniyor")
    # # Disconnect from the drone
    # vehicle.close()