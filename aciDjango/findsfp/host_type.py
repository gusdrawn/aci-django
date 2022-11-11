import os, requests, json, time, datetime, re

def aciHost(ip,username, password,site):
    s = requests.Session()
    #payload = '{"aaaUser" : {"attributes": {"name":"apic#TACACS\\\\'+user+'","pwd":"'+password+'"} } }'
    payload = '{"aaaUser" : {"attributes": {"name":"'+username+'","pwd":"'+password+'"} } }'
    requests.packages.urllib3.disable_warnings()
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
    login = s.post(ip+"/api/aaaLogin.json", verify=False, data=payload)
    if login.status_code == 200:
        print("Logged on APIC - "+ip)
    else:
        print("Error on login - "+ip)
        exit()

    localtime = time.localtime(time.time())
    now_year = int(localtime[0])
    now_month = int(localtime[1])
    now_day= int(localtime[2])
    now_hh = int(localtime[3])
    now_mm =  int(localtime[4])
    flapped_string = ""

    nodeResponse = s.get(ip+"/api/node/class/fabricNode.json", verify=False)
    nodes = json.loads(nodeResponse.content)
    for node in nodes['imdata']:
        leaf = re.search("node-(\w\w?\w?)", node['fabricNode']['attributes']['dn'])
        interfacesResponse = s.get(ip+"/api/node/class/topology/pod-1/node-"+leaf.group(1)+"/ethpmPhysIf.json?target-subtree-class=ethpmFcot", verify=False)
        if interfacesResponse.status_code == 200:
            interfaces = json.loads(interfacesResponse.content)
            if int(interfaces['totalCount']) > 0:
                for interface in interfaces['imdata']:
                    #dn = interface['ethpmPhysIf']['attributes']['dn']
                    if not interface['ethpmPhysIf']['attributes']['operStQual'] == "sfp-missing":
                        if interface['ethpmPhysIf']['attributes']['operStQual'] == "none" and (interface['ethpmPhysIf']['attributes']['usage'] == "epg" or interface['ethpmPhysIf']['attributes']['usage'] == "fabric" or interface['ethpmPhysIf']['attributes']['usage'] == "controller,epg,infra"):
                            next
                        else:
                            leaf = re.search("node-(\w\w?\w?)", interface['ethpmPhysIf']['attributes']['dn'])
                            name = re.search("(eth\w\/\w\w?)", interface['ethpmPhysIf']['attributes']['dn'])
                            sfpResponse = s.get(ip+"/api/node/mo/topology/pod-1/node-"+leaf.group(1)+"/sys/phys-["+name.group(1)+"]/phys.json?query-target=children&target-subtree-class=ethpmFcot", verify=False)
                            sfp = json.loads(sfpResponse.content)
                            #print ("Interfaz: "+name.group(1).replace("e","E")+" en el leaf: "+leaf.group(1)+" tiene: "+sfp['imdata'][1]["ethpmFcot"]["attributes"]["typeName"]+" esta: "+interface['ethpmPhysIf']['attributes']['operStQual']+" ("+interface['ethpmPhysIf']['attributes']['usage']+")")
                            eth_time = re.search("(\d\d\d\d)-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d).(\d\d\d)-(\d\d):(\d\d)", interface['ethpmPhysIf']['attributes']['lastLinkStChg'])
                            """
                            eth_year = int(eth_time.group(0))
                            eth_month = int(eth_time.group(1))
                            eth_day = int(eth_time.group(2))
                            eth_hh = int(eth_time.group(3))
                            eth_mm = int(eth_time.group(4))
                            """
                            eth_year = int(eth_time.group(1))
                            eth_month = int(eth_time.group(2))
                            eth_day = int(eth_time.group(3))
                            eth_hh = int(eth_time.group(4))
                            eth_mm = int(eth_time.group(5))

                            start_time = datetime.time(now_hh, now_mm, 0)
                            stop_time = datetime.time(eth_hh, eth_mm, 0)
                            start_date = datetime.date(now_year, now_month, now_day)
                            stop_date = datetime.date(eth_year, eth_month, eth_day)
                            datetime1 = datetime.datetime.combine(start_date, start_time)
                            datetime2 = datetime.datetime.combine(stop_date, stop_time)
                            time_elapsed = datetime1 - datetime2

                            #print(time_elapsed)
                            print ("Generando fila de: "+site+"-"+leaf.group(1)+"- "+name.group(1).replace("e","E"))
                            devlist = []
                            devlist.append({
                                'device'    :   "LEAF"+leaf.group(1),
                                'interface' :   name.group(1).replace("e","E"),
                                'sfp'       :   sfp['imdata'][0]["ethpmFcot"]["attributes"]["typeName"],
                                'link'      :   str(time_elapsed),
                                'status'    :   interface['ethpmPhysIf']['attributes']['operStQual']+" ("+interface['ethpmPhysIf']['attributes']['usage']
                            })

                            return devlist
                            #html_list + "<tr><td>"+site+"-"+leaf.group(1)+"</td><td>"+name.group(1).replace("e","E")+"</td><td>"+sfp['imdata'][0]["ethpmFcot"]["attributes"]["typeName"]+"</td><td>"+str(time_elapsed)+"</td><td>"+interface['ethpmPhysIf']['attributes']['operStQual']+" ("+interface['ethpmPhysIf']['attributes']['usage']+")"+"</td></tr>"
                            """
                            if (now_year - eth_year) > 0 : flapped_string =+ now_year - eth_year+" years"
                            if (now_month - eth_month) > 0 : flapped_string =+ now_month - eth_month+" months"
                            if (now_day - eth_day) > 0 : flapped_string =+ now_day - eth_day+" days"
                            if (now_hh - eth_hh) > 0 : flapped_string =+ now_hh - eth_hh+"h"
                            if (now_mm - eth_mm) > 0 : flapped_string =+ now_mm - eth_mm+"m"""
                            #print (name.group(1).replace("e","E"))
                            #print (sfp['imdata'][1]["ethpmFcot"]["attributes"]["typeName"])
                            #print (leaf.group(1))
                            #print (interface['ethpmPhysIf']['attributes']['operStQual']+" ("+interface['ethpmPhysIf']['attributes']['usage']+")")