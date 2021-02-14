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
    varStrGroupName = ""
    varStrGroupId = ""
    varNumChildStrGroups = 0
    varStrMaskingView = ""
    varStrNumVolumes = ""

    # Get Storage Group IDs
    getStorageGrpUrl = "https://10.60.8.184:8443/univmax/restapi/92/sloprovisioning/symmetrix/000297900850/storagegroup/"

    # ServiceNow Credentials
    username = 'smc'
    password = 'smc'
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
        print(storageGroupIdList)


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
            varStrGroupName = storageGroupDetails_data_json.get('storageGroupName')
            varStrSloDetails = storageGroupDetails_data_json.get('slo')
            varNumChildStrGroups = storageGroupDetails_data_json.get('num_of_child_sgs')
            if varNumChildStrGroups > 0:
                varNumChildStrGroups = storageGroupDetails_data_json.get('child_storage_group')
            varStrGrpMaskingView = storageGroupDetails_data_json.get('maskingview')
            varStrGrpType = storageGroupDetails_data_json.get('type')

            # Output Body - Storage Group Details        
            storageGroupBuilder = {"storageGroupId": varStrGroupId, "storageGroupName": varStrGroupName, "storageSlo": varStrSloDetails, "memberStorageGroups": varNumChildStrGroups, "storageGroupType": varStrGrpType, 
            "storageGroupMaskingView": varStrGrpMaskingView}
            jsonConverter_storageGroupBuilder = json.dumps(storageGroupBuilder, indent=2)
            storageGroup_details = '"' + str(each_storageGroupId) + '" ' + jsonConverter_storageGroupBuilder
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
    
    # Get Volume IDs
    getVolumeIDsUrl = "https://10.60.8.184:8443/univmax/restapi/92/sloprovisioning/symmetrix/000297900850/volume"

    # ServiceNow Credentials
    username = 'smc'
    password = 'smc'
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
    print(volumeId, len(volumeId))


    # Get VolumeID Details
    for each_volume_Id in volumeId:
        getVolumeIDDetailsUrl = "https://10.60.8.184:8443/univmax/restapi/92/sloprovisioning/symmetrix/000297900850/volume/" + each_volume_Id
        # Request Headers & Response
        headers = {"Content-Type": "application/json", "Accept": "application/json", "Authorization": basicAuth}
        response = requests.get(getVolumeIDDetailsUrl, headers=headers, verify=False)
        if response.status_code == 200:
            # Printing REST API Results
            volumeInfoDetails_raw_data = response.content

            # JSON Transformation
            volumeInfoDetails_data_json = json.loads(volumeInfoDetails_raw_data)
            varVolumeStorageGroup = volumeInfoDetails_data_json.get('storageGroupId')
            varVolumeEmulation = volumeInfoDetails_data_json.get('emulation')
            varVolumeCapacity = volumeInfoDetails_data_json.get('cap_gb')
            rawVolumeRDFNumber = str(volumeInfoDetails_data_json.get(['rdfGroupId'][0]))
            varVolumeRDFNumber = rawVolumeRDFNumber[22:24]  # ** Need an evaluation **

            # Output Body - Volume Group Details            
            volumeBuilder = {"volumeId": each_volume_Id, "configuredSizeInGb": varVolumeCapacity, "emulation": varVolumeEmulation, "configuration": "thin", "poolId": "SRP_1", "storageGroups": varVolumeStorageGroup, "rdfGroupId": varVolumeRDFNumber}
            jsonConverter_volumeBuilder = json.dumps(volumeBuilder, indent=2)
            volume_details = '"' + str(each_volume_Id) + '" ' + jsonConverter_volumeBuilder
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
            maskingView_details = '"' + str(each_maskingViewId) + '" ' + jsonConverter_maskingViewBuilder
            with open("E:\\Testing\\MaskingViewInfo.json", encoding='utf-8', mode='a') as MaskingViewInfo:
               print(maskingView_details, file=MaskingViewInfo)


def get_portgroup_info():
    
    # MaskingView ID Variables
    portGroupIds = []
    portGroupDetails_data_json = ""
    varPortGroupType = ""
    varPortGroupMaskingView = ""
    varPortGroupId = ""
    varStorageGroupId = ""

    # Get PortGroup IDs
    getPortGroupIdsUrl = "https://10.60.8.184:8443/univmax/restapi/92/sloprovisioning/symmetrix/000297900850/portgroup/"

    # ServiceNow Credentials
    username = 'smc'
    password = 'smc'
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
            portGroup_details = '"' + str(each_portGroupId) + '" ' + jsonConverter_portGroupBuilder
            with open("E:\\Testing\\PortGroupInfo.json", encoding='utf-8', mode='a') as PortGroupInfo:
               print(portGroup_details, file=PortGroupInfo)


def get_hostgroup_info():
    
    # HostGroup ID Variables
    hostGroupIds = []
    hostGroupDetails_data_json = ""
    varHostGroupType = ""
    varHostGroupId = ""
    varHostGroupMembers = ""

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
            varHostGroupMembers = hostGroupDetails_data_json.get(['host'][0:][0])
            varHostGroupMembersWWN = hostGroupDetails_data_json.get(['host'][0])

            # Output Body - MaskingView Details            
            hostGroupBuilder = {"hostGroupId": varHostGroupId, "hostGroupType": varHostGroupType, "memberInitiatorGroups": varHostGroupMembers, "memberInitiators": varHostGroupMembersWWN}
            jsonConverter_hostGroupBuilder = json.dumps(hostGroupBuilder, indent=2)
            hostGroup_details = '"' + str(each_hostGroupId) + '" ' + jsonConverter_hostGroupBuilder
            with open("E:\\Testing\\HostGroupInfo.json", encoding='utf-8', mode='a') as HostGroupInfo:
                print(hostGroup_details, file=HostGroupInfo)


if __name__ == "__main__":
    storageGrp_thread = threading.Thread(target=get_storage_info)
    volumeID_thread = threading.Thread(target=get_volume_info)
    maskingView_thread = threading.Thread(target=get_maskingview_info)
    portGroup_thread = threading.Thread(target=get_portgroup_info)
    hostGroup_thread = threading.Thread(target=get_hostgroup_info)

    storageGrp_thread.start()
    volumeID_thread.start()
    maskingView_thread.start()
    portGroup_thread.start()
    hostGroup_thread.start()
