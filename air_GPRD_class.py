#-*- encoding: utf-8 -*-
import requests, xmltodict, json # re, base64, zlib, 
import time
from io import BytesIO,StringIO
from wcf.records import *
from wcf.xml2records import XMLParser
import PRD_stations      # All the stations in the GPRD area

# https://github.com/ernw/python-wcfbin

class air_GPRD():
    def __init__(self):
        self.stationList = json.loads(PRD_stations.PRD_stationList_json)
        self.pollutantcode = (101,102,103,104,108,109,110)

    def getResponse(self, service, action, data):
        output = StringIO()
        output.write('<'+action+' xmlns="http://tempuri.org/">'+data+'</'+action+'>')
        output.seek(0)

        r = XMLParser.parse(output)
        req = dump_records(r)

        r = requests.post(url='http://113.108.142.147:20047/ClientBin/Env-GPRD-BLL-Services-' 
                            + service + '.svc/binary/' + action,
            data=req,
            headers={'Content-Type': 'application/msbin1',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'})
        r.encoding = "utf-8"
        res = r.content

        buf = BytesIO(res)
        r = Record.parse(buf)

        print_records(r, fp=output)
        output.seek(0)
        #print(output.getvalue())
        output = output.readlines()[1:-1]
        output = ''.join(output)

        convertedDict = xmltodict.parse(output.replace('&',''), xml_attribs=False)
        return json.dumps(convertedDict)

    def getAllStations(self,languageId=3):
    # languageID = 1: Simplified Chinese
    #              2: Traditional Chinese
    #              3: English
        return json.loads(self.getResponse("StationService", "GetAllStations",
               "<languageId>"+str(languageId)+"</languageId>"))["GetAllStationsResult"]["a:StationInfoModel"]

    def getAllSystemConfigs(self, languageId=3):
        return json.loads(self.getResponse("SystemService", "GetAllSystemConfigs", 
               "<languageID>"+str(languageId)+"</languageID>"))["GetAllSystemConfigsResult"]["a:ConfigModel"]

    def getAllStationsInfo(self):
        return self.stationList
        #return json.loads(PRD_stations.PRD_stationList_json)

    # TODO: make this return the stations belonging to each region (Guangdong, Hong Kong and Macau)
    #def getProvinceAllStationInfo(self, AreaId):

    def getPublishTime(self):
        return json.loads(self.getResponse("SystemService", "GetPublishTime", ""))['GetPublishTimeResult']

    def getSinglePollution(self,pollutantcode,stationcode):
        return json.loads(self.getResponse("PollutationService", "GetSinglePollution", 
               "<pollutantcode>"+str(pollutantcode)+"</pollutantcode>" +
               "<stationcode>"+str(stationcode)+"</stationcode>"))["GetSinglePollutionResult"]
    
    def getAllPollutants(self):
        for key,_ in self.stationList.items():
            with open(key+'_'+time.strftime('%Y%m%d_%H%M%S')+'.dat','w+') as f:
                for pl in self.pollutantcode:
                    f.writelines(self.getPublishTime()+",")
                    data = self.getSinglePollution(pl,key)
                    f.writelines(data['a:PollutantString']+","+data['a:LastHourValue']+"\n")

    def getSingleAirIndex(self,stationcode,languageId=3):
        return json.loads(self.getResponse("InfomationService","GetSingleAirIndex",
               "<languageId>"+str(languageId)+"</languageId>" +
               "<stationcode>"+str(stationcode)+"</stationcode>"))["GetSingleAirIndexResult"]

if __name__ == '__main__':
    air = air_GPRD()
    air.getAllPollutants()