"""
Python script to fetch all elements of PowerMax array:

"""
# Import Statements

import requests
import threading
import json
import urllib3
from urllib3.exceptions import NewConnectionError
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_storage_info():

    # StorageGroup Variables
    storageGroupIdList = []
    varStrGroupId = ""
    varNumChildStrGroups = 0
    varStrSloDetails = ""
    varStrGrpType = ""
    storageGroupBuilder = {}

    # Get Storage Group IDs
    getStorageGrpUrl = "https://10.60.8.184:8443/univmax/restapi/92/sloprovisioning/symmetrix/000297900850/storagegroup/"

    # ServiceNow Credentials
    basicAuth = 'Basic c21jOnNtYw=='

    # Request Headers & Response
    headers = {"Content-Type": "application/json", "Accept": "application/json", "Authorization": basicAuth}
    response = requests.get(getStorageGrpUrl, headers=headers, verify=False)
    if response.status_code == 200:
        # Printing REST API Results
        storageGroupId_raw_data = response.content

        # JSON Transformation
        storageGroupId_data_json = json.loads(storageGroupId_raw_data)
        storageGroupIdList = storageGroupId_data_json['storageGroupId']

    # Get Storage Group Details
    for each_storageGroupId in storageGroupIdList:
        getStorageGrpDetailsUrl = "https://10.60.8.184:8443/univmax/restapi/92/sloprovisioning/symmetrix/000297900850/storagegroup/" + each_storageGroupId
        # Request Headers & Response
        headers = {"Content-Type": "application/json", "Accept": "application/json", "Authorization": basicAuth}
        response = requests.get(getStorageGrpDetailsUrl, headers=headers, verify=False)
        if response.status_code == 200:
            # Printing REST API Results
            storageGroupDetails_raw_data = response.content

            # JSON Transformation
            storageGroupDetails_data_json = json.loads(storageGroupDetails_raw_data)
            varStrGroupId = storageGroupDetails_data_json.get('storageGroupId')
            varStrSloDetails = storageGroupDetails_data_json.get('slo')
            varStrGrpMaskingView = storageGroupDetails_data_json.get('maskingview')
            varStrGroupEmulation = storageGroupDetails_data_json.get('device_emulation')
            varStrGroupSRP = storageGroupDetails_data_json.get('srp')
            varStrGrpType = storageGroupDetails_data_json.get('type')
            if varStrGrpType == "Child":
                listParentStrGroups = storageGroupDetails_data_json.get('parent_storage_group')
                varParentStrGroups = listParentStrGroups[:]
                print(varParentStrGroups)
                # Output Body - Storage Group Details        
                storageGroupBuilder = {"storageGroupId": varStrGroupId, "storageSlo": varStrSloDetails, "storageGroupMaskingView": varStrGrpMaskingView, "storageGroupEmulation": varStrGroupEmulation, "storageGroupSRP": varStrGroupSRP, "storageGroupType": varStrGrpType, "storageGroupParent": varParentStrGroups}
            else:
                storageGroupBuilder = {"storageGroupId": varStrGroupId, "storageSlo": varStrSloDetails, "storageGroupMaskingView": varStrGrpMaskingView, "storageGroupEmulation": varStrGroupEmulation, "storageGroupSRP": varStrGroupSRP, "storageGroupType": varStrGrpType}
            
            varNumChildStrGroups = storageGroupDetails_data_json.get('num_of_child_sgs')
            if varNumChildStrGroups > 0:
                varNumChildStrGroups = storageGroupDetails_data_json.get('child_storage_group')
                # Output Body - Storage Group Details        
                storageGroupBuilder = {"storageGroupId": varStrGroupId, "storageSlo": varStrSloDetails, "storageGroupMaskingView": varStrGrpMaskingView, "storageGroupEmulation": varStrGroupEmulation, "storageGroupSRP": varStrGroupSRP, "storageGroupType": varStrGrpType, "memberStorageGroups": varNumChildStrGroups}
            
            jsonConverter_storageGroupBuilder = json.dumps(storageGroupBuilder, indent=2)
            storageGroup_details = '"' + str(each_storageGroupId) + '": ' + jsonConverter_storageGroupBuilder + ','
            with open("E:\\Testing\\StorageGroupInfo.json", encoding='utf-8', mode='a') as StorageGroupInfo:
                print(storageGroup_details, file=StorageGroupInfo)
    

def get_volume_info():
    
    # VolumeID Variables
    volumeId = []
    volumeInfoDetails_data_json = ""
    varVolumeEmulation = ""
    varVolumeStorageGroup = ""
    varVolumeCapacity = 0
    varVolumeRDFNumber = 0
    rdfGroup_Details_Json = ""
    rdfGroupRemoteVolumeDetails_Json = ""
    varVolumeServicePolicy = ""
    volumeServiceLevelDetails_data_json = ""
    varRDFGroupNumber = 0
    varRDFGroupMode = ""
    varLocalVolumeId = ""
    varRemoteVolumeId = ""
    varRemoteRDFGroupNumber = ""
    varRDFGroupLabel = ""
    varRemoteSymmetrixArray = ""

    # Get Volume IDs
    getVolumeIDsUrl = "https://10.60.8.184:8443/univmax/restapi/92/sloprovisioning/symmetrix/000297900850/volume"

    # ServiceNow Credentials
    basicAuth = 'Basic c21jOnNtYw=='

    # Request Headers & Response
    headers = {"Content-Type": "application/json", "Accept": "application/json", "Authorization": basicAuth}
    response = requests.get(getVolumeIDsUrl, headers=headers, verify=False)
    if response.status_code == 200:
        # Printing REST API Results
        volumeId_raw_data = response.content

        # JSON Transformation
        volumeId_data_json = json.loads(volumeId_raw_data)
        volumeIdList = volumeId_data_json['resultList']['result']
        for each_volume_id in volumeIdList:
            volumeId.append(each_volume_id.get('volumeId'))

    # Get VolumeID Details
    for each_volume_Id in volumeId:
        print("Volume ID = ", each_volume_Id)
        getVolumeIDDetailsUrl = "https://10.60.8.184:8443/univmax/restapi/92/sloprovisioning/symmetrix/000297900850/volume/" + each_volume_Id
        # Request Headers & Response
        headers = {"Content-Type": "application/json", "Accept": "application/json", "Authorization": basicAuth}
        response = requests.get(getVolumeIDDetailsUrl, headers=headers, verify=False)
        if response.status_code == 200:
            # Printing REST API Results
            volumeInfoDetails_raw_data = response.content

            # JSON Transformation
            volumeInfoDetails_data_json = json.loads(volumeInfoDetails_raw_data)
            varVolumeEmulation = volumeInfoDetails_data_json.get('emulation')
            varVolumeCapacity = volumeInfoDetails_data_json.get('cap_gb')
            varVolumeStorageGroup = volumeInfoDetails_data_json.get('storageGroupId')

            if varVolumeStorageGroup != None:
                getVolumePolicyUrl = "https://10.60.8.184:8443/univmax/restapi/92/sloprovisioning/symmetrix/000297900850/storagegroup/" + str(varVolumeStorageGroup)
                # Request Headers & Response
                headers = {"Content-Type": "application/json", "Accept": "application/json", "Authorization": basicAuth}
                response = requests.get(getVolumePolicyUrl, headers=headers, verify=False)
                if response.status_code == 200:
                    # Printing REST API Results
                    volumePolicyDetails_raw_data = response.content
                    # JSON Transformation
                    volumeServiceLevelDetails_data_json = json.loads(volumePolicyDetails_raw_data)
                    varVolumeServicePolicy = volumeServiceLevelDetails_data_json.get('service_level')

            rawVolumeRDFNumber = volumeInfoDetails_data_json.get('rdfGroupId')
            if rawVolumeRDFNumber != None:
                varVolumeRDFNumber = rawVolumeRDFNumber[0]['rdf_group_number']  # ** Need an evaluation **
                getRDFGroupDetailsUrl = "https://10.60.8.184:8443/univmax/restapi/92/replication/symmetrix/000297900850/rdf_group/" + str(varVolumeRDFNumber)
                # Request Headers & Response
                headers = {"Content-Type": "application/json", "Accept": "application/json", "Authorization": basicAuth}
                response = requests.get(getRDFGroupDetailsUrl, headers=headers, verify=False)
                if response.status_code == 200:
                    rdfGroupDetails_raw_data = response.content
                    rdfGroup_Details_Json = json.loads(rdfGroupDetails_raw_data)
                    # RDF Group Variables
                    varRDFGroupNumber = rdfGroup_Details_Json.get('rdfgNumber')
                    varRDFGroupLabel = rdfGroup_Details_Json.get('label')
                    varRemoteRDFGroupNumber = rdfGroup_Details_Json.get('remoteRdfgNumber')
                    varRemoteSymmetrixArray = rdfGroup_Details_Json.get('remoteSymmetrix')
                    varRDFGroupMode = rdfGroup_Details_Json.get('modes')

                if int(varVolumeRDFNumber) > 0:
                    getRemoteArrayVolumesUrl = getRDFGroupDetailsUrl + "/volume/" + each_volume_Id
                    # Request Headers & Response
                    headers = {"Content-Type": "application/json", "Accept": "application/json", "Authorization": basicAuth}
                    response = requests.get(getRemoteArrayVolumesUrl, headers=headers, verify=False)
                    if response.status_code == 200:
                        rdfGroupRemoteVolumeDetails_raw_data = response.content
                        rdfGroupRemoteVolumeDetails_Json = json.loads(rdfGroupRemoteVolumeDetails_raw_data)
                        # RDF Group Remote Volume Variables
                        varLocalVolumeId = rdfGroupRemoteVolumeDetails_Json.get('localVolumeName')
                        varRemoteVolumeId = rdfGroupRemoteVolumeDetails_Json.get('remoteVolumeName')

        
            #Output Body - Volume Group Details
            volumeBuilder = {"volumeId": each_volume_Id, "configuredSizeInGb": varVolumeCapacity, "emulation": varVolumeEmulation, "configuration": "thin", "poolId": "SRP_1", "slaPolicyId": varVolumeServicePolicy, "storageGroups": varVolumeStorageGroup, 
            "rdfDetails": {"srdfGroupLocalId": varRDFGroupNumber, "srdfGroupRemoteId": varRemoteRDFGroupNumber, "srdfGroupLabel": varRDFGroupLabel, "srdfRemoteArray": varRemoteSymmetrixArray, "srdfGroupMode": varRDFGroupMode, "srdfLocalVolumeId": varLocalVolumeId, "srdfRemoteVolumeId": varRemoteVolumeId}}
            jsonConverter_volumeBuilder = json.dumps(volumeBuilder, indent=2)
            volume_details = '"' + str(each_volume_Id) + '": ' + jsonConverter_volumeBuilder + ','
            with open("E:\\Testing\\VolumeInfo.json", encoding='utf-8', mode='a') as VolumeInfo:
                print(volume_details, file=VolumeInfo)


def get_maskingview_info():
    
    # MaskingView ID Variables
    maskingViewIds = []
    maskingViewDetails_data_json = ""
    varMaskingViewId = ""
    varHostGroupId = ""
    varPortGroupId = ""
    varStorageGroupId = ""

    # Get Volume IDs
    getMaskingViewsUrl = "https://10.60.8.184:8443/univmax/restapi/92/sloprovisioning/symmetrix/000297900850/maskingview"

    # ServiceNow Credentials
    username = 'smc'
    password = 'smc'
    basicAuth = 'Basic c21jOnNtYw=='

    # Request Headers & Response
    headers = {"Content-Type": "application/json", "Accept": "application/json", "Authorization": basicAuth}
    response = requests.get(getMaskingViewsUrl, headers=headers, verify=False)
    if response.status_code == 200:
        # Printing REST API Results
        maskingView_raw_data = response.content

        # JSON Transformation
        maskingView_data_json = json.loads(maskingView_raw_data)
        maskingViewIds = maskingView_data_json['maskingViewId']
        print(maskingViewIds)


    # Get MaskingView Details
    for each_maskingViewId in maskingViewIds:
        getMaskingViewDetailsUrl = "https://10.60.8.184:8443/univmax/restapi/92/sloprovisioning/symmetrix/000297900850/maskingview/" + each_maskingViewId
        # Request Headers & Response
        headers = {"Content-Type": "application/json", "Accept": "application/json", "Authorization": basicAuth}
        response = requests.get(getMaskingViewDetailsUrl, headers=headers, verify=False)
        if response.status_code == 200:
            # Printing REST API Results
            maskingViewDetails_raw_data = response.content

            # JSON Transformation
            maskingViewDetails_data_json = json.loads(maskingViewDetails_raw_data)
            varMaskingViewId = maskingViewDetails_data_json.get('maskingViewId')
            varHostGroupId = maskingViewDetails_data_json.get('hostGroupId')
            varPortGroupId = maskingViewDetails_data_json.get('portGroupId')
            varStorageGroupId = maskingViewDetails_data_json.get('storageGroupId')

            # Output Body - MaskingView Details            
            maskingViewBuilder = {"maskingViewId": varMaskingViewId, "memberInitiatorGroup": varHostGroupId, "memberPortGroup": varPortGroupId, "memberStorageGroup": varStorageGroupId}
            jsonConverter_maskingViewBuilder = json.dumps(maskingViewBuilder, indent=2)
            maskingView_details = '"' + str(each_maskingViewId) + '": ' + jsonConverter_maskingViewBuilder + ','
            with open("E:\\Testing\\MaskingViewInfo.json", encoding='utf-8', mode='a') as MaskingViewInfo:
               print(maskingView_details, file=MaskingViewInfo)


def get_portgroup_info():
    
    # MaskingView ID Variables
    portGroupIds = []
    portGroupDetails_data_json = ""
    varPortGroupType = ""
    varPortGroupMaskingView = ""
    varPortGroupId = ""

    # Get PortGroup IDs
    getPortGroupIdsUrl = "https://10.60.8.184:8443/univmax/restapi/92/sloprovisioning/symmetrix/000297900850/portgroup/"

    # ServiceNow Credentials
    basicAuth = 'Basic c21jOnNtYw=='

    # Request Headers & Response
    headers = {"Content-Type": "application/json", "Accept": "application/json", "Authorization": basicAuth}
    response = requests.get(getPortGroupIdsUrl, headers=headers, verify=False)
    if response.status_code == 200:
        # Printing REST API Results
        portGroupIds_raw_data = response.content

        # JSON Transformation
        portGroupIds_data_json = json.loads(portGroupIds_raw_data)
        portGroupIds = portGroupIds_data_json['portGroupId']
        print(portGroupIds)


    # Get PortGroup Details
    for each_portGroupId in portGroupIds:
        getPortGroupDetailsUrl = "https://10.60.8.184:8443/univmax/restapi/92/sloprovisioning/symmetrix/000297900850/portgroup/" + each_portGroupId
        # Request Headers & Response
        headers = {"Content-Type": "application/json", "Accept": "application/json", "Authorization": basicAuth}
        response = requests.get(getPortGroupDetailsUrl, headers=headers, verify=False)
        if response.status_code == 200:
            # Printing REST API Results
            portGroupDetails_raw_data = response.content

            # JSON Transformation
            portGroupDetails_data_json = json.loads(portGroupDetails_raw_data)
            varPortGroupId = portGroupDetails_data_json.get('portGroupId')
            varPortGroupType = portGroupDetails_data_json.get('type')
            varPortGroupMaskingView = portGroupDetails_data_json.get('maskingview')
            varPortGroupMembers = portGroupDetails_data_json.get('symmetrixPortKey')

            # Output Body - MaskingView Details            
            portGroupBuilder = {"portGroupId": varPortGroupId, "portGroupType": varPortGroupType, "portGroupMaskingView": varPortGroupMaskingView, "memberPorts": varPortGroupMembers}
            jsonConverter_portGroupBuilder = json.dumps(portGroupBuilder, indent=2)
            print(jsonConverter_portGroupBuilder)
            portGroup_details = '"' + str(each_portGroupId) + '": ' + jsonConverter_portGroupBuilder + ','
            with open("E:\\Testing\\PortGroupInfo.json", encoding='utf-8', mode='a') as PortGroupInfo:
               print(portGroup_details, file=PortGroupInfo)


def get_hostgroup_info():
    
    # HostGroup ID Variables
    hostGroupIds = []
    hostGroupDetails_data_json = ""
    varHostGroupType = ""
    varHostGroupId = ""
    varHostGroupMembers = []

    # Get HostGroup IDs
    getHostGroupsUrl = "https://10.60.8.184:8443/univmax/restapi/92/sloprovisioning/symmetrix/000297900850/hostgroup/"

    # ServiceNow Credentials
    username = 'smc'
    password = 'smc'
    basicAuth = 'Basic c21jOnNtYw=='

    # Request Headers & Response
    headers = {"Content-Type": "application/json", "Accept": "application/json", "Authorization": basicAuth}
    response = requests.get(getHostGroupsUrl, headers=headers, verify=False)
    if response.status_code == 200:
        # Printing REST API Results
        hostGroupIds_raw_data = response.content

        # JSON Transformation
        hostGroupIds_data_json = json.loads(hostGroupIds_raw_data)
        hostGroupIds = hostGroupIds_data_json['hostGroupId']
        print(hostGroupIds)


    # Get HostGroup Details
    for each_hostGroupId in hostGroupIds:
        getHostGroupDetailsUrl = "https://10.60.8.184:8443/univmax/restapi/92/sloprovisioning/symmetrix/000297900850/hostgroup/" + each_hostGroupId
        # Request Headers & Response
        headers = {"Content-Type": "application/json", "Accept": "application/json", "Authorization": basicAuth}
        response = requests.get(getHostGroupDetailsUrl, headers=headers, verify=False)
        if response.status_code == 200:
            # Printing REST API Results
            hostGroupDetails_raw_data = response.content

            # JSON Transformation
            hostGroupDetails_data_json = json.loads(hostGroupDetails_raw_data)
            varHostGroupId = hostGroupDetails_data_json.get('hostGroupId')
            varHostGroupType = hostGroupDetails_data_json.get('type')
            memHosts = hostGroupDetails_data_json.get('host')
            for each_element in memHosts:
                varHostGroupMembers.append(each_element['hostId'])

            # Output Body - MaskingView Details
            hostGroupBuilder = {"hostGroupId": varHostGroupId, "hostGroupType": varHostGroupType, "memberHostGroups": varHostGroupMembers}
            jsonConverter_hostGroupBuilder = json.dumps(hostGroupBuilder, indent=2)
            print(jsonConverter_hostGroupBuilder)
            del varHostGroupMembers[:]
            hostGroup_details = '"' + str(each_hostGroupId) + '": ' + jsonConverter_hostGroupBuilder + ','
            with open("E:\\Testing\\HostGroupInfo.json", encoding='utf-8', mode='a') as HostGroupInfo:
                print(hostGroup_details, file=HostGroupInfo)


def get_initiator_info():
    
    # HostGroup ID Variables
    hostIds = []
    hostDetails_data_json = ""
    varHostGroupId = ""
    varHostId = ""
    varHostInitiators = []
    varWWNAliasInfo = []
    allWWNs = []
    fetchWWNsAlias = []
    
    # Get HostGroup IDs
    getHostsUrl = "https://10.60.8.184:8443/univmax/restapi/92/sloprovisioning/symmetrix/000297900850/host/"

    # ServiceNow Credentials
    basicAuth = 'Basic c21jOnNtYw=='

    # Request Headers & Response
    headers = {"Content-Type": "application/json", "Accept": "application/json", "Authorization": basicAuth}
    response = requests.get(getHostsUrl, headers=headers, verify=False)
    if response.status_code == 200:
        # Printing REST API Results
        hostIds_raw_data = response.content

        # JSON Transformation
        hostIds_data_json = json.loads(hostIds_raw_data)
        hostIds = hostIds_data_json['hostId']
        print(hostIds)


    # Get HostGroup Details
    for each_hostId in hostIds:
        getHostsDetailsUrl = "https://10.60.8.184:8443/univmax/restapi/92/sloprovisioning/symmetrix/000297900850/host/" + each_hostId
        # Request Headers & Response
        headers = {"Content-Type": "application/json", "Accept": "application/json", "Authorization": basicAuth}
        response = requests.get(getHostsDetailsUrl, headers=headers, verify=False)
        if response.status_code == 200:
            # Printing REST API Results
            hostsDetails_raw_data = response.content

            # JSON Transformation
            hostDetails_data_json = json.loads(hostsDetails_raw_data)
            
            getAllWWNs = "https://10.60.8.184:8443/univmax/restapi/92/sloprovisioning/symmetrix/000297900850/initiator/"
            # Request Headers & Response
            headers = {"Content-Type": "application/json", "Accept": "application/json", "Authorization": basicAuth}
            response = requests.get(getAllWWNs, headers=headers, verify=False)
            if response.status_code == 200:
                # Printing REST API Results
                allWWNDetails_raw_data = response.content
                # JSON Transformation
                allWWNs_data_json = json.loads(allWWNDetails_raw_data)
                allWWNs = allWWNs_data_json.get('initiatorId')
            
            varHostId = hostDetails_data_json.get('hostId')
            varHostInitiators = hostDetails_data_json.get('initiator')
            if varHostInitiators != None:
                for each_element in varHostInitiators:
                    for each_WWNs in allWWNs:
                        if each_element in each_WWNs:
                            fetchWWNsAlias.append(each_WWNs)

                    if len(fetchWWNsAlias) > 0:
                        getWWNAliasUrl = "https://10.60.8.184:8443/univmax/restapi/92/sloprovisioning/symmetrix/000297900850/initiator/" + fetchWWNsAlias[0]
                        # Request Headers & Response
                        headers = {"Content-Type": "application/json", "Accept": "application/json", "Authorization": basicAuth}
                        response = requests.get(getWWNAliasUrl, headers=headers, verify=False)
                        if response.status_code == 200:
                            # Printing REST API Results
                            wwnAliasDetails_raw_data = response.content
                            #JSON Modifications
                            wwnAliasInfo_data_json = json.loads(wwnAliasDetails_raw_data)
                            varHostGroupId = wwnAliasInfo_data_json.get('hostGroup')
                            varWWNHostName = wwnAliasInfo_data_json.get('host')
                            if varHostId == varWWNHostName:
                                varWWNAliasValue = wwnAliasInfo_data_json.get('alias')
                                if varWWNAliasValue != None:
                                    wwn_string_builder = each_element + ": " + varWWNAliasValue
                                    varWWNAliasInfo.append(wwn_string_builder)
                                else:
                                    wwn_string_builder = each_element + ": " + "null"
                                    varWWNAliasInfo.append(wwn_string_builder)
                    fetchWWNsAlias.clear()

            # Output Body - MaskingView Details
            hostsBuilder = {"initiatorId": varHostId, "initiatorGroupId": varHostGroupId, "memberHBAInitiators": varWWNAliasInfo}
            jsonConverter_hostsBuilder = json.dumps(hostsBuilder, indent=2)
            hosts_details = '"' + str(each_hostId) + '": ' + jsonConverter_hostsBuilder + ','
            with open("E:\\Testing\\InitiatorInfo.json", encoding='utf-8', mode='a') as InitiatorInfo:
                print(hosts_details, file=InitiatorInfo)
                varWWNAliasInfo.clear()


def get_pool_info():
    
    # SRPool ID Variables
    srpIds = []
    srp_data_json = ""
    arraySRPDetails_data_json = ""
    varSRPId = ""
    varSRPCapacityInfo = ""
    varSRPTotalUsableGB = 0
    varSRPSubscribedGB = 0
    varSRPUsedGB = 0
    varSRPServiceLevels = []

    # Get SRP IDs
    getPoolUrl = "https://10.60.8.184:8443/univmax/restapi/92/sloprovisioning/symmetrix/000297900850/srp/"

    # ServiceNow Credentials
    username = 'smc'
    password = 'smc'
    basicAuth = 'Basic c21jOnNtYw=='

    # Request Headers & Response
    headers = {"Content-Type": "application/json", "Accept": "application/json", "Authorization": basicAuth}
    response = requests.get(getPoolUrl, headers=headers, verify=False)
    if response.status_code == 200:
        # Printing REST API Results
        srp_raw_data = response.content

        # JSON Transformation
        srp_data_json = json.loads(srp_raw_data)
        srpIds = srp_data_json['srpId']
        print(srpIds)


    # Get SRP Details
    for each_srpId in srpIds:
        getSRPDetailsUrl = "https://10.60.8.184:8443/univmax/restapi/92/sloprovisioning/symmetrix/000297900850/srp/" + each_srpId
        # Request Headers & Response
        headers = {"Content-Type": "application/json", "Accept": "application/json", "Authorization": basicAuth}
        response = requests.get(getSRPDetailsUrl, headers=headers, verify=False)
        if response.status_code == 200:
            # Printing REST API Results
            srpDetails_raw_data = response.content

            # JSON Transformation
            arraySRPDetails_data_json = json.loads(srpDetails_raw_data)
            varSRPId = arraySRPDetails_data_json.get('srpId')
            varSRPCapacityInfo = arraySRPDetails_data_json.get('srp_capacity')
            varSRPTotalUsableGB = varSRPCapacityInfo['usable_total_tb'] * 1024
            varSRPSubscribedGB = varSRPCapacityInfo['subscribed_total_tb'] * 1024
            varSRPUsedGB = varSRPCapacityInfo['usable_used_tb'] * 1024
            varSRPServiceLevels = arraySRPDetails_data_json.get('service_levels')

            # Output Body - SRP Details            
            poolInfoBuilder = {"poolId": varSRPId, "poolConfiguredCapacityGB": varSRPTotalUsableGB, "poolSubscribedCapacityGB": varSRPSubscribedGB, "poolUsedCapacityGB": varSRPUsedGB, "poolServiceLevels": varSRPServiceLevels}
            jsonConverter_srpBuilder = json.dumps(poolInfoBuilder, indent=2)
            print(jsonConverter_srpBuilder)
            srp_details = '"' + str(each_srpId) + '": ' + jsonConverter_srpBuilder + ','
            with open("E:\\Testing\\PoolInfo.json", encoding='utf-8', mode='a') as PoolDetailsInfo:
                print(srp_details, file=PoolDetailsInfo)


if __name__ == "__main__":
    storageGrp_thread = threading.Thread(target=get_storage_info)
    volumeID_thread = threading.Thread(target=get_volume_info)
    maskingView_thread = threading.Thread(target=get_maskingview_info)
    portGroup_thread = threading.Thread(target=get_portgroup_info)
    hostGroup_thread = threading.Thread(target=get_hostgroup_info)
    initiator_thread = threading.Thread(target=get_initiator_info)
    srpInfo_thread = threading.Thread(target=get_pool_info)

    storageGrp_thread.start()
    volumeID_thread.start()
    maskingView_thread.start()
    portGroup_thread.start()
    hostGroup_thread.start()
    initiator_thread.start()
    srpInfo_thread.start()
