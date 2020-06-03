import os

def reconnect(adress):
    command = "sudo dhclient -r"
    os.system(command)
    command = "sudo killall wpa_supplicant"
    os.system(command)
    command = "sudo ifconfig wlan0 up"
    os.system(command)
    command = "sudo wpa_supplicant -B -i wlan0 -c " + adress
    os.system(command)
    command = "sudo dhclient -v wlan0"
    os.system(command)

if __name__ == '__main__':
    reconnect()
