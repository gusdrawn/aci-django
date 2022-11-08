import os
import requests
import json

s = requests.Session()

def get_droplets():
    url = 'https://api.digitalocean.com/v2/droplets'
    r = requests.get(url, headers={'Authorization':'Bearer %s' % 'access_token'})
    droplets = r.json()
    droplet_list = []
    for i in range(len(droplets['droplets'])):
        droplet_list.append(droplets['droplets'][i])
    return droplet_list

def login_aci():
    payload = '{"aaaUser" : {"attributes": {"name":"admin","pwd":"!v3G@!4@Y"} } }'
    login = s.post("https://sandboxapicdc.cisco.com/api/aaaLogin.json", verify=False, data=payload)
    if login.status_code == 200:
        print("--------------------------------------------------------------------------------------")    
        print("Logged on APIC")
        print("--------------------------------------------------------------------------------------\n\n")
    else:
        print("Error on login")
        exit()  

# https://sandboxapicdc.cisco.com/api/node/class/fabricNode.json?&order-by=fabricNode.modTs|desc

def getnodes():
    url = "https://sandboxapicdc.cisco.com/api/node/class/fabricNode.json?&order-by=fabricNode.modTs|desc"
    response = json.loads(s.get(url, verify=False).text)
    print (response)
    return response


# method: GET
# url: https://sandboxapicdc.cisco.com/api/node/class/faultInfo.json?query-target-filter=and(ne(faultInfo.severity,"cleared"),eq(faultInfo.code,"F0104"))&order-by=faultInfo.severity|desc&page=0&page-size=15
# response: {"totalCount":"1","imdata":[{"faultInst":{"attributes":{"ack":"no","alert":"no","cause":"port-down","changeSet":"adminSt:up, autoNeg:on, bw:0, delay:1, dot1qEtherType:0x8100, fcotChannelNumber:Channel32, id:po1.1, inhBw:unspecified, isReflectiveRelayCfgSupported:Supported, layer:Layer3, linkDebounce:100, linkLog:default, mdix:auto, medium:broadcast, mode:trunk, mtu:0, name:bond1, operSt:down, portT:unknown, prioFlowCtrl:auto, reflectiveRelayEn:off, routerMac:not-applicable, snmpTrapSt:enable, spanMode:not-a-span-dest, speed:inherit, switchingSt:disabled, trunkLog:default, usage:discovery","childAction":"","code":"F0104","created":"2022-11-05T05:51:31.408+00:00","delegated":"no","descr":"Bond Interface po1.1 on node 1 of fabric ACI Fabric1 with hostname apic1 is now down","dn":"topology/pod-1/node-1/sys/caggr-[po1.1]/fault-F0104","domain":"infra","highestSeverity":"critical","lastTransition":"2022-11-05T05:53:44.361+00:00","lc":"raised","occur":"1","origSeverity":"critical","prevSeverity":"critical","rule":"cnw-aggr-if-down","severity":"critical","status":"","subject":"equipment","title":"","type":"operational"}}}]}
# timestamp: 22:31:41 DEBUG 

