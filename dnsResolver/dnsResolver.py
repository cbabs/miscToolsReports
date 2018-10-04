import socket
import time
import xlsxwriter

#This file is where all output is logged
timestamp = time.ctime().replace(':', '.')

#Open file with hosts
hostList = open("hosts.txt").read().splitlines()


def resolveByName(hostName):
    
    
    try:
        dnsResults = socket.gethostbyname_ex(hostName)
        cnames = socket.getfqdn(hostName)
        
    except:
        dnsResults = "Could not resolve"
        return [hostName, dnsResults]
    
    
    return [hostName, dnsResults, cnames]


def resolveByIp(ipAddr):
    
    try:
        reslvedIp = socket.gethostbyaddr(ipAddr)
    except:
        dnsResults = "Could not resolve"
        return [ipAddr, dnsResults]
        
    primaryName = reslvedIp[0] # Get hostname
    
    return resolveByName(primaryName) # Process hostname
    
    

def checkIPv4Valid(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False
    
    return True
    
def checkList(hostlist):
    
    retrnList = []
    
    for host in hostlist:
    
        if checkIPv4Valid(host) is True:
            ipReslt = resolveByIp(host)
            retrnList.append(ipReslt)
            #resolveByIp(host)
        else:
            hostReslt = resolveByName(host)
            retrnList.append(hostReslt)
            
            #resolveByName(host)
          
    return retrnList
            
#Function to create excel report
def createXls():
    
    #Get the dns list
    resltList = checkList(hostList)  # Process list


    
    
    ##Create switch file and sheet
    #Create file
    xlsFile = xlsxwriter.Workbook('host-report-' + timestamp + '.xlsx')
    #Add sheet in workbook
    xlsSheet = xlsFile.add_worksheet(timestamp)
    
    #Styling for title if applicable 
    bold = xlsFile.add_format({'bold': True})
    boldRed = xlsFile.add_format({'bold': True, 'font_color': 'red'})
    
    #Create category roles from 'switchCols' list
    intRow = 0

    categoryList = ['Name Passed', 'Machine Name',
                     'Ip Address(es)', 'Aliases']
    
    #Set beginning column
    colSwi = 0
    
    for categItem in categoryList:
        xlsSheet.write(0, colSwi, categItem, bold)
        
        colSwi += 1 #Go to the next column
    
    #Make sure a list exist.  Not tested
    if resltList == None:
        print('Yeah, empty list')
        xlsSheet.write(0, 2, 'No Errors detected', bold)
        xlsFile.close() 
        exit()
    
    #Set beginning column
    colSwi = 0
        
    #Set beginning row
    rowSwi = 3

    
    #Loop overs lists in list and put into xlsx file
    for item in resltList:
        
        #Go back to the first column
        if colSwi != 0: colSwi = 0
        
        print(item)
        
        dnsHostName = item[0]
        machineName = item[1][0]
        ipAddrReslv = str(item[1][2]).strip("[']")
        
        if len(item) == 3:
            dnsAlias = str(item[2])
        
        #If unable to resolve add to all vars in list
        if item[1] == 'Could not resolve':
            dnsAlias = "Could not resolve"
            
            machineName = "Could not resolve"
            ipAddrReslv = "Could not resolve"
            
        
        

            
        
        tempList = [dnsHostName, machineName, ipAddrReslv, dnsAlias]
        
        for infoItem in tempList:
            
        
            #Add interface info before ARP.  Add then incre column
            xlsSheet.write(rowSwi, colSwi, infoItem)
            colSwi += 1 #Go to the next column
        
        
        
        rowSwi += 1 #Go to the next row before loop ends

        
        xlsSheet.write  # Not really sure I need this....
        #loop goes back to the top
    
    xlsFile.close()  # Close file
    
def main():
    
    print("Reading this list: {}\n\n".format(str(hostList)))
    createXls()
    
    

    
        
if __name__ == '__main__':
    main()