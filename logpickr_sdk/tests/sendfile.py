import logpickr_sdk as lpk

ID = "25b385d6-039f-40d2-ae18-cdd676670366"
KEY = "6421c828-c882-45d7-ab9b-372c7ce04297"
API_URL = "https://api.igfx-eastus-demo.logpickr.com"
AUTH_URL = "https://auth.igfx-eastus-demo.logpickr.com"

wg = lpk.Workgroup(ID, KEY, API_URL, AUTH_URL)
project = lpk.Project("8d2d83e1-f244-4094-bdca-7795aabef6b9", wg)

filestructure = lpk.FileStructure(
    charset = "UTF-8",
    delimiter = ";",
    quoteChar = '"',
    escapeChar = '\\',
    eolChar = "\r\n",
    commentChar = "#",
    columnSeparator = "|",
    header = True
)

caseidmapping = lpk.CaseIdOrActivityMapping(0)
activitymapping = lpk.CaseIdOrActivityMapping(3)
startTimeMapping = lpk.TimeMapping(1,"yyyy/MM/dd HH:mm:ss.SSS")
endTimeMapping = lpk.TimeMapping(2,"yyyy/MM/dd HH:mm:ss.SSS")
timemappings = list([startTimeMapping, endTimeMapping])
rolemapping = lpk.DimensionMapping("role", 4, False)
dimensionmappings = list([rolemapping])

columnmapping = lpk.ColumnMapping(caseidmapping=caseidmapping, activitymapping=activitymapping, timemappings=timemappings, dimensionmappings=dimensionmappings, metricmappings=None)

project.create_column_mapping(filestructure=filestructure, columnmapping=columnmapping)

project.add_file("./BankLoanData-EN.csv")