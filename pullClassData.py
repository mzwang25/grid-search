import requests
import json
from datetime import datetime

# day is a single char ... MTWRF
def filterByDayInWeek( jsonObj, day ):
  return [ x for x in jsonObj if day in x[ 'Days_in_week' ] ]

# dayOfWeek = Something like ... MTWHF
# goalTime = "H:M:S"
# classLink = "Link of whatever is after classroom=

def howLongCanIStayFor( classLink_, roomName ):
  classLink = "https://sa.ucla.edu/ro/Public/SOC/Results/ClassroomDetail?term=22S&classroom=" + classLink_
  r = requests.get( classLink )

  # extract the schedule from the html
  try:
    beginIndex = r.text.index( 'createFullCalendar' )
  except:
    # no calendar found
    return( "class does not have a schedule" )
  classSchedule = r.text[ beginIndex : ]

  beginIndex = classSchedule.index( '[' )
  endIndex = classSchedule.index( '));')

  # turn the text into a standard JSON
  jsonSchedule = json.loads( classSchedule[ beginIndex : endIndex - 1 ] )
  roomName = roomName.replace( " ", "_" )
  with open('classScheduleData/{}.json'.format( roomName ), 'w') as outfile:
    json.dump( jsonSchedule, outfile, indent=1 )

