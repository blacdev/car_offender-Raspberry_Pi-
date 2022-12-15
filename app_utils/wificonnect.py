import os
import platform
import getpass
import subprocess as sp

#  Create new connection with a new wifi
def createNewConnection(SSID, key):
    config = (
        """<?xml version=\"1.0\"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>name</name>
    <SSIDConfig>
        <SSID>
            <name>"""
        + SSID
        + """</name>
        </SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>auto</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>"""
        + key
        + """</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
</WLANProfile>"""
    )

    if platform.system() == "Linux":

        #  To connect to the new specified ssid
        command = "nmcli dev wifi connect '" + SSID + "' password '" + key + "'"

    # run command
    os.system(command)


def connect(name, SSID):
    if platform.system() == "Linux":

        #  To connect to an existing specified ssid
        command = "nmcli con up " + SSID
    os.system(command)


def displayAvailableNetworks():
    if platform.system() == "Linux":

        #  To list all active wifi network available
        command = "nmcli dev wifi list"

        #  To write all active wifi network available into ava.txt file
        activenet = "nmcli -f SSID dev wifi list> availablenetworks.txt"

        # write all ssids that have been added to the network to wifiname
        c = "nmcli -t -f name connection show > wifiname.txt"

    # run command
    os.system(command)

    # run command
    os.system(activenet)

    #  run command in c
    os.system(c)


# try:
#     displayAvailableNetworks()
#     # option = input("New connection (y/N)? ")
#     option = open("wifiname.txt", "r")
#     availablenetworks = open("availablenetworks.txt", "r")
#     for x in availablenetworks:
#         for y in option:
#             print(len(x))
#             print(x)
#             print(y)
#             if x == y:

#                 name = x

#                 connect(name, name)

#                 output = sp.getoutput("nmcli -t -f name connection show -a")
#                 if output:
#                     quit("closing...")
#                 print(
#                     "If you aren't connected to this network, try connecting with correct credentials"
#                 )

#             else:
#                 name = x
#                 key = getpass.getpass("Password: ")
#                 createNewConnection(name, key)
#                 connect(name, name)
#                 print(
#                     "If you aren't connected to this network, try connecting with correct credentials"
#                 )
#     # elif option == "y":
#     #     name = input("Name: ")
#     #     key = getpass.getpass("Password: ")
#     #     createNewConnection(name, key)
#     #     connect(name, name)
#     #     print(
#     #         "If you aren't connected to this network, try connecting with correct credentials"
#     #     )
# except KeyboardInterrupt as e:
#     print("\nExiting...")


