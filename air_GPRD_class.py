# Modified on Nov 2, 2021 to adapt to the new server changes

#-*- encoding: utf-8 -*-
import requests, re, xmltodict, json 
import time
import PRD_stations      # All the stations in the GPRD area



class air_GPRD():
    def __init__(self):
        self.stationList = json.loads(PRD_stations.PRD_stationList_json)
        self.pollutantcode = (101,102,103,104,108,109,110)

    def getResponse(self, action, data):
        d = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><'+action+' xmlns="http://tempuri.org/">'+data+'</'+action+'></s:Body></s:Envelope>' #)

        r = requests.post(url='http://113.108.142.147:20047/GprdWcf/GprdDataService.svc',
            data=d,
            headers={'Content-Type': 'text/xml; charset=utf-8', 
                'SOAPAction': 'http://tempuri.org/IService1/'+action, #'application/msbin1',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'})
        r.encoding = "utf-8"

        res = r.content
        convertedDict = xmltodict.parse(res, xml_attribs=False)['s:Envelope']['s:Body']
        return json.dumps(convertedDict)

    def getAllStations(self,languageId=3):
    # languageID = 1: Simplified Chinese
    #              2: Traditional Chinese
    #              3: English
        return json.loads(self.getResponse("GetAllStations",
            "<languageId>"+str(languageId)+"</languageId>"))['GetAllStationsResponse']["GetAllStationsResult"]["a:StationInfoModel"]

    def getAllSystemConfigs(self, languageId=3):
        return json.loads(self.getResponse("GetAllSystemConfigs", 
               "<languageID>"+str(languageId)+"</languageID>"))['GetAllSystemConfigsResponse']["GetAllSystemConfigsResult"]["a:ConfigModel"]

    def getAllStationsInfo(self):
        return self.stationList
        #return json.loads(PRD_stations.PRD_stationList_json)

    # TODO: make this return the stations belonging to each region (Guangdong, Hong Kong and Macau)
    #def getProvinceAllStationInfo(self, pid):
    #    pjson = json.loads(station_data.stationList_json)
    #    ret = []
    #    for c in pjson[str(pid)]:
    #        for s in pjson[str(pid)][c]:
    #            ret.append(s)
    #
    #    return ret

    def getPublishTime(self):
        return json.loads(self.getResponse("GetPublishTime", ""))['GetPublishTimeResponse']['GetPublishTimeResult']

    def getSinglePollution(self,pollutantcode,stationcode):
        return json.loads(self.getResponse("GetSinglePollution", 
               "<pollutantcode>"+str(pollutantcode)+"</pollutantcode>" +
               "<stationcode>"+str(stationcode)+"</stationcode>"))['GetSinglePollutionResponse']["GetSinglePollutionResult"]
    
    def getAllPollutants(self):
        for key,_ in self.stationList.items():
            with open(key+'_'+time.strftime('%Y%m%d_%H%M%S')+'.dat','w+') as f:
                for pl in self.pollutantcode:
                    f.writelines(self.getPublishTime()+",")
                    data = self.getSinglePollution(pl,key)
                    f.writelines(data['a:PollutantString']+","+data['a:LastHourValue']+"\n")

    def getSingleAirIndex(self,languageId,stationcode):
        # This function has no returned value
        return json.loads(self.getResponse("GetSingleAirIndex",
               "<languageId>"+str(languageId)+"</languageId>" +
               "<stationcode>"+str(stationcode)+"</stationcode>"))['GetSingleAirIndexResponse']["GetSingleAirIndexResult"]

if __name__ == '__main__':
    air = air_GPRD()
    air.getAllPollutants()
