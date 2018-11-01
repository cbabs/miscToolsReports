

'''
wr net 10.170.67.50:/dv-136-fw01- oirwangroup-fl05-20181030-1302.txt

wr net <<10.170.67.50>>:/<<hostname>><<timestamp>>.txt
'''
import netmiko
import time
import getpass

# This file is where all output is logged
timestamp = time.ctime().replace(':', '.')

# Open file with hosts
hostList = open("hosts.txt").read().splitlines()

# Open file with hosts
#cmdsList = open("sshCmds.txt").read().splitlines()

# Check files for data
if not hostList[0]: raise("No hosts in hosts.txt file or unable to read")

def getCreds():

    while True:
        sshUser = input('\n\nEnter username: ')
        sshPass = getpass.getpass('Enter password: ')
        tftpSrv = input('\n\nEnter TFTP Server: ')
        devType = input('''Device Type? (Enter "?" for list.  Hit enter for generic termserver)
SSH Device Type: ''')
        
        
        if devType == '': devType = 'generic_termserver'
        if devType == '?': devType = ''
        if devType == 'cisco_asa':
            secret = getpass.getpass('Enter Enable pass: ')
                
                
        sshConf = {
        'device_type': devType,
        'ip': hostList[0],
        'username': sshUser,
        'password': sshPass}
        
        print("Testing creds on first host in list: " + hostList[0])
        
        try:
            netmiko.ConnectHandler(**sshConf)
            print("Login success")
            retrnDict = {'uid': sshUser, 'password': sshPass, 
                    'devType': devType, "tftpSrv": tftpSrv}
            if secret:
            retrnDict['secret'] = secret
            
            return retrnDict
            break
    
        except Exception as e:
            print(e)

        else:
            print('Access denied')
    
def runCommands(uid, password, devType, tftpSrv, secret=None):
    
    # Log File
    f = open("sshLog-{}.txt".format(timestamp), "a")
    
    for host in hostList:
        
        sshConf = {
            'device_type': devType,
            'ip': host,
            'username': uid,
            'password': password}
        if secret:
            sshConf['secret'] = secret
            
        
        try:
            net_connect = netmiko.ConnectHandler(**sshConf)
        except Exception as e:
            failLog = open("failedLog-{}.txt".format(timestamp), "a")
            failLog.write("The {} failed: \n {}".format(host, e))
            failLog.close()
            
        
        f.write("\n" + host)     
        cmdsList = ('wr net {}:/{}--{}.txt' .format(tftpSrv, host, timestamp))
        
        sshOutput = net_connect.send_config_set(cmdsList)
        f.write(sshOutput)
        
        f.write("\n")
    
    f.close()
    


def main():
    
    credsDict = getCreds()
    
    runCommands(credsDict['uid'], credsDict['password'],
                 credsDict["devType"], credsDict['tftpSrv'])
    
     

  
if __name__ == "__main__":
    main()