"""
Python script performs below actions:
-- Fetches StorageGroup for PowerMax array
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
    varNumChildStrGroups = ""
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
            varNumChildStrGroups = storageGroupDetails_data_json.get('num_of_child_sgs')
            varStrMaskingView = storageGroupDetails_data_json.get('maskingview')
            varStrNumVolumes = storageGroupDetails_data_json.get('num_of_vols')

            # Output Body - Storage Group Details
            with open("E:\\Testing\\StorageGroupInfo.txt", encoding='utf-8', mode='a') as StorageGroupFile:
                print('"' + varStrGroupId + '" {' + '\n',
                ' "storageGroupName": ' + '"' + str(varStrGroupName) + '"''\n',
                ' "storageGroupId": ' +  '"' + str(varStrGroupId) + '"''\n',
                ' "num_of_child_sgs": ' + '"' + str(varNumChildStrGroups) + '"''\n',
                ' "maskingview": ' + '"' + str(varStrMaskingView) + '"''\n',
                ' "num_of_vols": ' + '"' + str(varStrNumVolumes) + '"''\n',
                '},', file=StorageGroupFile)


def get_volume_info():
    
    # VolumeID Variables
    volumeId = []
    varVolumeEmulation = ""
    varVolumeStorageGroup = ""
    varVolumeCapacity = 0
    varVolumeNumStrGroups = 0
    
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
    print(volumeId)

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
            varVolumeNumStrGroups = volumeInfoDetails_data_json.get('num_of_storage_groups')

            # Output Body - Volume Group Details
            with open("E:\\Testing\\VolumeInfo.txt", encoding='utf-8', mode='a') as VolumeInfo:
                print('"volumeId" {' + '\n',
                '  volumeEmulation: ' + str(varVolumeEmulation) + '\n',
                '  volumeCapacity: ' +  str(varVolumeCapacity) + '\n',
                '  volumeNumStorageGroups: ' +  str(varVolumeNumStrGroups) + '\n',
                '},', file=VolumeInfo)


if __name__ == "__main__":
    storageGrp_thread = threading.Thread(target=get_storage_info)
    volumeID_thread = threading.Thread(target=get_volume_info)

    storageGrp_thread.start()
    volumeID_thread.start()
