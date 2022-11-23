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
