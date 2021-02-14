import requests
import threading
import json
import urllib3
from urllib3.exceptions import NewConnectionError
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
        getVolumeIDDetailsUrl = "https://10.60.8.184:8443/univmax/restapi/92/sloprovisioning/symmetrix/000297900850/volume/000C4"
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
            varVolumeRDFNumber = rawVolumeRDFNumber[22:23]  # ** Need an evaluation **
            if int(varVolumeRDFNumber) > 0:
                getRDFGroupDetailsUrl = "https://10.60.8.184:8443/univmax/restapi/92/replication/symmetrix/000297900850/rdf_group/" + varVolumeRDFNumber
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
                getRemoteArrayVolumesUrl = getRDFGroupDetailsUrl + "/volume/000C4"
                # Request Headers & Response
                headers = {"Content-Type": "application/json", "Accept": "application/json", "Authorization": basicAuth}
                response = requests.get(getRemoteArrayVolumesUrl, headers=headers, verify=False)
                if response.status_code == 200:
                    rdfGroupRemoteVolumeDetails_raw_data = response.content
            
            rdfGroupRemoteVolumeDetails_Json = json.loads(rdfGroupRemoteVolumeDetails_raw_data)
            # RDF Group Remote Volume Variables
            varLocalVolumeId = rdfGroupRemoteVolumeDetails_Json.get('localVolumeName')
            varRemoteVolumeId = rdfGroupRemoteVolumeDetails_Json.get('remoteVolumeName')
            
            # Output Body - Volume Group Details
            volumeBuilder = {"volumeId": each_volume_Id, "configuredSizeInGb": varVolumeCapacity, "emulation": varVolumeEmulation, "configuration": "thin", "poolId": "SRP_1", 
            "storageGroups": varVolumeStorageGroup, "rdfDetails": {"srdfGroupLocalId": varRDFGroupNumber, "srdfGroupRemoteId": varRemoteRDFGroupNumber, "srdfGroupLabel": varRDFGroupLabel, "srdfRemoteArray": varRemoteSymmetrixArray, 
            "srdfGroupMode": varRDFGroupMode, "srdfLocalVolumeId": varLocalVolumeId, "srdfRemoteVolumeId": varRemoteVolumeId} }
            jsonConverter_volumeBuilder = json.dumps(volumeBuilder, indent=2)
            print(jsonConverter_volumeBuilder)


get_volume_info()
