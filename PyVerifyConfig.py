from netmiko import ConnectHandler
import pandas as pd
import getpass, re
from datetime import datetime

start_timeall = datetime.now()

#################################################################
#Adds vlans to L2 Switches
#Including: vlan 40,vlan 50,vlan 66,vlan 70
#Will locate tagged ports on Vlan 999 and apply to all vlans
#Rename vlan 999 to iOT-Trust
#################################################################

def AddVerifyConfig():

    df = pd.read_csv('inventory.csv')

    site = input("Enter site: ")

    layer = input("Enter layer (L2/L3): ")

    iplist = (site.lower()+layer.upper())

    x = (df[iplist])

    usr = input("Enter Username: ")

    PassWD = getpass.getpass()

    for n in (x):

        try:

            if '10' in n:

                ip=n

                start_time = datetime.now()

                net_connect = ConnectHandler(device_type='hp_procurve', ip=ip, username='nsttech', password=PassWD, fast_cli=True, session_log = 'output.txt')
            
                taggedStaff = net_connect.send_command("show run vlan 701 | inc tagged | ex untagged")
            
                taggedIoT = net_connect.send_command("show run vlan 707 | inc tagged | ex untagged")

                taggedBYOD = net_connect.send_command("show run vlan 708 | inc tagged | ex untagged")

                prompt = net_connect.find_prompt()

                if 'tagged' in taggedIoT:
                    IoT = ("Vlan 707 - Confirmed")
                else:
                    dhcpPool = ["vlan 707", "name WiFi-iOT", taggedStaff, "ip igmp"]
                    net_connect.send_config_set(dhcpPool)
                    IoT = ("Vlan 707 - Updated")

                if 'tagged' in taggedBYOD:
                    BYOD = ("Vlan 708 - Confirmed")
                else:
                    dhcpPool = ["vlan 708", "name WiFi-BYOD-Staff", taggedStaff, "ip igmp"]
                    net_connect.send_config_set(dhcpPool)
                    BYOD = ("Vlan 708 - Updated")

                net_connect.save_config()
                net_connect.disconnect()

                end_time = datetime.now()
                    
                #Prints output of switch
                #with open('output.txt', 'r') as output:
                #    print(output.read())

                #Notifies user of completion
                hostname = prompt[:-1]
                print("\n")
                print("#" * 30)
                print (hostname + " " + "-" + " " + "Complete")
                print('Duration: {}'.format(end_time - start_time))
                print(IoT)
                print(BYOD)
                print("#" * 30)
                
        except TypeError:
            continue
        except:
            print("\n")
            print("#" * 30)
            print ('Failed to connect to ' + ip)
            print("#" * 30)

AddVerifyConfig()

end_timeall = datetime.now()

#Prints overall time of script
print("\n")
print("#" * 30)
print ("Script" + " " + "Complete")
print('Duration: {}'.format(end_timeall - start_timeall))
print("#" * 30)