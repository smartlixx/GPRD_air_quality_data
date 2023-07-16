# GPRD_air_quality_data
This tool scapes the Guangdong-Hong Kong-Macau PRD air quality monitoring system (http://113.108.142.147:20047/) to get the real time air quality 
data in Pearl River Delta. The system uses Microsoft Silverlight to render the data, and this tool relies on the package wcf (https://github.com/ernw/python-wcfbin)
to decode the POST requests. 

***Update*** Nov 2, 2021: the website has been changed and get rid of Silverlight. 

## Dependencies
 - wcf (https://github.com/ernw/python-wcfbin
 - requests
 - xmltodict
 - json
 
This tool was inspired by air-in-China (https://github.com/hebingchang/air-in-china). 
