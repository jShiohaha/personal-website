SECRETS_FILE = "client_secret.json"

# CONSTANTS FOR READING AND PARSING GSHEETS
DATE_IDX = 0
EVENT_TYPE_IDX = 1
EVENT_IDX = 2
LINK_IDX = 3

PERSONAL_TRACKING_SPREADSHEET_NAME = "Personal Tracking"
LIFE_LOG_WORKSHEET_NAME = "Life Log"
G_SHEETS_SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
G_SHEETS_DATE_FORMAT = '%m/%d/%Y'
ISO_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

# CONSTANTS FOR UPDATING LIFELOG HTML CONTENT
LIFE_LOG_FILENAME = "../html/lifeLog.html"
BIG_ENERGY_CIRCLE_CLASSNAME = "big-energy-circle"
NORMAL_ENERGY_CIRCLE_CLASSNAME = "normal-energy-circle"

# the first two are actual year values. the third is the list-of-entries ul element.
YEAR_CONTAINER_COMPONENT = '''
<div id="{}" class="year-container">
    <div>
        <div class="year-circle"></div>
        <div class="year-value">
            <p class="year-value-text">{}</p>
        </div>
        <div class="visibility-toggle">
            <p class="visibility-toggle-text">Hide</p>
        </div>
    </div>
    <ul class="list-of-entries">
        <!-- month entry -->
        <li>
            {}
        </li>
    </ul>
</div>
'''

# the first is the circle type, second is formatted month and value text, third is event text
ENTRY_COMPONENT = '''
<div class="entry">
    <div class="{}"></div>
    <div class="month-and-year">
        <p class="month-value-text">{}</p>
    </div>
    <div class="event">
        <p class="event-text">
            {}
        </p>
    </div>
</div>
'''
