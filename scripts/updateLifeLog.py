from datetime import datetime

# pip imports
from AdvancedHTMLParser import AdvancedHTMLParser, AdvancedHTMLFormatter
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# project imports
from constants import *


class GSheetClient:
    def __init__(self, spreadSheetname=None):
        # use creds to create a client to interact with the Google Drive API
        self.scope = G_SHEETS_SCOPE
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(SECRETS_FILE, self.scope)
        self.client = gspread.authorize(self.credentials)
        self.speadsheetName = None
        if spreadSheetname is not None:
            self.speadsheetName = spreadSheetname
        self.spreadsheet = None
    
    def isSpreadsheetNameSet(self):
        return self.speadsheetName is not None

    def getSpreadSheetName(self):
        if not self.isSpreadsheetNameSet():
            raise Exception("No sheet name specified.")
        return self.speadsheetName
    
    def setSpreadsheetName(self, speadsheetName):
        self.speadsheetName = speadsheetName

    def getOrOpenSpreadsheet(self):
        if not self.isSpreadsheetNameSet():
            raise Exception("No sheet name specified.")
        if self.spreadsheet is None:
            self.spreadsheet = self.client.open(self.speadsheetName)
        return self.spreadsheet

    def openWorksheetByIndex(self, index):
        return self.getOrOpenSpreadsheet().get_worksheet(index)
    
    def openWorksheetByTitle(self, title):
        return self.getOrOpenSpreadsheet().worksheet(title)

    def openAllWorksheets(self):
        return self.getOrOpenSpreadsheet().worksheets()


class Event:
    def __init__(self, kwargs):
        self.date = kwargs["date"]
        self.eventType = kwargs["eventType"]
        self.text = kwargs["text"]

    def __repr__(self):
        return "<Event: Date: {}, eventType: {}, Text: {}>".format(self.date, self.eventType, self.text)


def getAllLifeLogEvents(gSheetClient):
    lifeLogWorksheet = gSheetClient.openWorksheetByTitle(LIFE_LOG_WORKSHEET_NAME)

    # Extract and print all of the values
    allRows = lifeLogWorksheet.get_all_values()
    listOfEvents = []
    for row in allRows:
        event = Event({
            "date": datetime.strptime(row[DATE_IDX], G_SHEETS_DATE_FORMAT).isoformat(),
            "eventType": row[EVENT_TYPE_IDX],
            "text": row[EVENT_IDX], 
            "url": row[LINK_IDX]
        })

        listOfEvents.append(event)
    return listOfEvents


gSheetClient = GSheetClient(PERSONAL_TRACKING_SPREADSHEET_NAME)

# get all events as Event objects from Google Sheets, already sorted
listOfEvents = getAllLifeLogEvents(gSheetClient)

# create parser and parse life log html file
parser = AdvancedHTMLParser()
parser.parseFile(LIFE_LOG_FILENAME)

lifeLogList, lifeLogYearList = [], []
yearValue, yearContainer = None, None
for event in listOfEvents:
    date = datetime.strptime(event.date, ISO_DATE_FORMAT)
    eventType = event.eventType    

    if yearValue is None:
        yearValue = str(date.year)
    # set new year value because it changed
    if yearValue != str(date.year):
        lifeLogListHtml = "".join(lifeLogYearList)

        yearContainer = YEAR_CONTAINER_COMPONENT.format(yearValue, yearValue, lifeLogListHtml)
        
        lifeLogList.append(yearContainer)
        yearValue = str(date.year)

        lifeLogYearList.clear()

    circlyeType = BIG_ENERGY_CIRCLE_CLASSNAME if eventType == "B" else NORMAL_ENERGY_CIRCLE_CLASSNAME
    monthDayText = "{:02d}.{:02d}".format(date.month, date.day)
    singleEntry = ENTRY_COMPONENT.format(circlyeType, monthDayText, event.text)
    lifeLogYearList.append(singleEntry)


lifeLogListContainer = parser.getElementsByClassName("life-log-list-element")[0]
lifeLogListContainer.appendInnerHTML("".join(lifeLogList))

formatter = AdvancedHTMLFormatter()
formatter.parseStr(parser.toHTML())

outFile = open(LIFE_LOG_FILENAME, "w")
outFile.write(formatter.getHTML())
outFile.close()
