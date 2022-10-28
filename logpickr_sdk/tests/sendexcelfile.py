import logpickr_sdk as lpk

ID = "a216d7c6-98b8-4b5c-b10e-9918999d9e2a"
KEY = "aeee8d05-ce11-4017-b565-1d46286337b8"
API_URL = "https://dev-360-api.igrafxcloud.com"
AUTH_URL = "https://dev-360-auth.igrafxcloud.com"

wg = lpk.Workgroup(ID, KEY, API_URL, AUTH_URL)
project = lpk.Project("640d8b94-87bf-4c73-b8f7-ac5d8ac85773", wg)

filestructure = lpk.FileStructure(
    charset = "UTF-8",
    delimiter = ";",
    quoteChar = '"',
    escapeChar = '\\',
    eolChar = "\\r\\n",
    commentChar = "#",
    header = True,
    fileType = lpk.FileType.xlsx,
    sheetName = "Sheet1"
)

caseidmapping = lpk.CaseIdOrActivityMapping(0)
activitymapping = lpk.CaseIdOrActivityMapping(3)
startTimeMapping = lpk.TimeMapping(1,"yyyy/MM/dd HH:mm:ss.SSS")
endTimeMapping = lpk.TimeMapping(2,"yyyy/MM/dd HH:mm:ss.SSS")
timemappings = list([startTimeMapping, endTimeMapping])
rolemapping = lpk.DimensionMapping("role", 5, False)
dimensionmappings = list([rolemapping])

columnmapping = lpk.ColumnMapping(caseidmapping=caseidmapping, activitymapping=activitymapping, timemappings=timemappings, dimensionmappings=dimensionmappings, metricmappings=None)

project.create_column_mapping(filestructure=filestructure, columnmapping=columnmapping)

project.add_file("p2pShortExcel.xlsx")