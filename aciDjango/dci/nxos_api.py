import requests
import json

# [   
#     0: {
#         "device": device,
#         "Po20": True
#         "Po17": "True",
#         "SPT": True,
#         "sid": "1",
#         "input": "show vlan id "+vlan+" ;show spanning-tree vlan "+vlan+"",
#         "output_format": "json"
#     }
#     1: {...}
# ]

################## N7K ##################
def n7k_vlans(device,vlan,username,password):
    status_vlan = {}
    url='http://'+device+'/ins'
    status_vlan["Device"] = device
    myheaders={'content-type':'application/json'}
    payload = {
        "ins_api": {
        "version": "1.2",
        "type": "cli_show",
        "chunk": "0",
        "sid": "1",
        "input": "show vlan id "+vlan+" ;show spanning-tree vlan "+vlan+"",
        "output_format": "json"
        }
    }
    response = requests.post(url,data=json.dumps(payload),headers=myheaders,auth=(username,password), verify=False)
    if response.status_code == 200:
        output = response.json()
    else:
        print ("\t *** ERROR *** CODE: "+response.status_code)
        print ("\t *** ERROR *** CHECK CODE: "+response.text)
    ## Primer comando por eso 0, PRIMERO VLANs
    if output["ins_api"]["outputs"]["output"][0]["body"] != "":
        interfaces = output["ins_api"]["outputs"]["output"][0]["body"]["TABLE_vlanbriefid"]["ROW_vlanbriefid"]["vlanshowplist-ifidx"].split(",")
        for interface in interfaces:
            if interface == "port-channel20":
                status_vlan["Po20"] = True
            else:
                status_vlan["Po20"] = False
            if interface == "port-channel17":
                status_vlan["Po17"] = False
            else:
                status_vlan["Po17"] = False
    else:
        print("Command not working")
    ## Segundo comando ahora 1, Spanning TRee
    if output["ins_api"]["outputs"]["output"][1]["body"] != "":
        if output["ins_api"]["outputs"]["output"][1]["body"]["TABLE_tree"]["ROW_tree"]["bridge_priority"] == "4094":
            status_vlan["SPT"] = True
        else:
            status_vlan["SPT"] = False

    return status_vlan

################## N9K ##################
def n9k_vlans(device,vlan,username,password):
    status_vlan = {}
    url='http://'+device+'/ins'
    status_vlan["Device"] = device
    myheaders={'content-type':'application/json'}
    payload = {
        "ins_api": {
            "version": "1.0",
            "type": "cli_show",
            "chunk": "0",
            "sid": "sid",
            "input": "show vlan id "+str(vlan)+" ;show spanning-tree vlan "+str(vlan)+"",
            "output_format": "json"
        }
    }
    response = requests.post(url,data=json.dumps(payload),headers=myheaders,auth=(username,password), verify=False)
    if response.status_code == 200:
        output = response.json()
    else:
        print ("\t *** ERROR *** CODE: "+str(response.status_code))
        print ("\t *** ERROR *** CHECK CODE: "+str(response.text))
    ## The first command is about VLAN, for this reaseon the "0"
    if output["ins_api"]["outputs"]["output"][0]["body"] != "":
        interfaces = output["ins_api"]["outputs"]["output"][0]["body"]["TABLE_vlanbriefid"]["ROW_vlanbriefid"]["vlanshowplist-ifidx"].split(",")
        for interface in interfaces:
            if interface == "port-channel20":
                status_vlan["Po20"] = True
            else:
                status_vlan["Po20"] = False
            if interface == "port-channel17":
                status_vlan["Po17"] = True
            else:
                status_vlan["Po17"] = False
    ## The second command is about SPT, now is "1"
    if output["ins_api"]["outputs"]["output"][1]["body"] != "":
        if output["ins_api"]["outputs"]["output"][1]["body"]["TABLE_tree"]["ROW_tree"]["bridge_priority"] == "4094":
            status_vlan["SPT"] = True
        else:
            status_vlan["SPT"] = False
    else:
        print("Command not working")

    return status_vlan

def n9k_dci(device,username,password):
    status_dci = {}
    url='https://'+device+'/ins'
    status_dci["Device"] = device
    myheaders={'content-type':'application/json'}
    payload = {
        "ins_api": {
            "version": "1.0",
            "type": "cli_show",
            "chunk": "0",
            "sid": "sid",
            "input": "show ip ospf neighbors  ;show system uptime ;show bgp l2vpn evpn summary  ;show int eth1/1-4,eth1/48-50 ;show int eth1/1-4,eth1/48 transceiver details  ;show int eth1/1-4,eth1/48-50 counters errors  ;show int eth1/1-4,eth1/48-50 counters storm-control ",
            "output_format": "json"
        }
     }
    response = requests.post(url,data=json.dumps(payload),headers=myheaders,auth=(username,password), verify=False)
    if response.status_code == 200:
        output = response.json()
    else:
        print ("\t *** ERROR *** CODE: "+str(response.status_code))
        print ("\t *** ERROR *** CHECK CODE: "+str(response.text))
    ## OSPF Check
    neighbors = output["ins_api"]["outputs"]["output"][0]["body"]["TABLE_ctx"]["ROW_ctx"]["TABLE_nbr"]["ROW_nbr"]
    for neighbor in neighbors:
        if neighbor["state"][0:3] != "FULL":
            status_dci["ospf"] = False
            break
        status_dci["ospf"] = True
    ## Uptime Check
    if output["ins_api"]["outputs"]["output"][1]["body"]["sys_up_days"] == 0:
        status_dci["uptime_status"] = False
    else:
        status_dci["uptime_status"] = True
    days = output["ins_api"]["outputs"]["output"][1]["body"]["sys_up_days"]
    hrs = output["ins_api"]["outputs"]["output"][1]["body"]["sys_up_hrs"]
    mins = output["ins_api"]["outputs"]["output"][1]["body"]["sys_up_mins"]
    status_dci["uptime"] = "D:"+str(days)+"H:"+str(hrs)+"M:"+str(mins)
    ## BGP Check
    neighbors = output["ins_api"]["outputs"]["output"][2]["body"]["TABLE_vrf"]["ROW_vrf"]["TABLE_af"]["ROW_af"]["TABLE_saf"]["ROW_saf"]["TABLE_neighbor"]["ROW_neighbor"]
    for neighbor in neighbors:
        if int(neighbor["prefixreceived"]) == 0:
            status_dci["bgp"] = False
            break
        status_dci["bgp"] = True
    ## Interfaces Check
    interfaces = output["ins_api"]["outputs"]["output"][3]["body"]["TABLE_interface"]["ROW_interface"]
    for interface in interfaces:
        if interface["state"] != "up":
            status_dci["bgp"] = False
            break
        status_dci["interface"] = True
    ## Transceiver Check
    transceivers = output["ins_api"]["outputs"]["output"][4]["body"]["TABLE_interface"]["ROW_interface"]
    for transceiver in transceivers:
        # Temperature
        temp =       int(float(transceiver["TABLE_lane"]["ROW_lane"]["temperature"]))
        temp_high =  int(float(transceiver["TABLE_lane"]["ROW_lane"]["temp_warn_hi"]))
        temp_low  =  int(float(transceiver["TABLE_lane"]["ROW_lane"]["temp_warn_lo"]))
        # Power RX
        pwrrx =      int(float(transceiver["TABLE_lane"]["ROW_lane"]["rx_pwr"]))
        pwrrx_high = int(float(transceiver["TABLE_lane"]["ROW_lane"]["rx_pwr_warn_hi"]))
        pwrrx_low  = int(float(transceiver["TABLE_lane"]["ROW_lane"]["rx_pwr_warn_lo"]))
        # Power TX
        pwrtx =      int(float(transceiver["TABLE_lane"]["ROW_lane"]["tx_pwr"]))
        pwrtx_high = int(float(transceiver["TABLE_lane"]["ROW_lane"]["tx_pwr_warn_hi"]))
        pwrtx_low  = int(float(transceiver["TABLE_lane"]["ROW_lane"]["tx_pwr_warn_lo"]))
        if (temp_low < temp < temp_high) & (pwrrx_low < pwrrx < pwrrx_high) & (pwrtx_low < pwrtx < pwrtx_high):
            status_dci["transceiver"] = True
        else:
            status_dci["transceiver"] = False
            break
    ## Interfaces Error Check
    interfaces = output["ins_api"]["outputs"]["output"][5]["body"]["TABLE_interface"]["ROW_interface"]
    for interface in interfaces:
        for int_error in interface:
            if isinstance(int_error, str):
                next
            elif int_error != 0:
                status_dci["errors"] = False
                break
        
        # Discard alternative solution
        # aligh  =    interface["eth_align_err"]
        # fcs =       interface["eth_fcs_err"]
        # xmit =      interface["eth_xmit_err"]
        # rcv =       interface["eth_rcv_err"]
        # undersize = interface["eth_undersize"]
        # outdisc =   interface["eth_outdisc"]
        # if aligh != 0 & fcs != 0 & xmit != 0 & rcv != 0 & undersize != 0 & outdisc != 0:
        #     status_dci["errors"] = False
        #     break
    ## Interfaces Check
    interfaces = output["ins_api"]["outputs"]["output"][6]["body"]["TABLE_interface"]["ROW_interface"]
    for interface in interfaces:
        if interface["eth_total_supp"] != "0":
            status_dci["storm"] = False
            break
        status_dci["storm"] = True
    return status_dci