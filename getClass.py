import requests
import json
from datetime import datetime

# day is a single char ... MTWRF
def filterByDayInWeek( jsonObj, day ):
  return [ x for x in jsonObj if day in x[ 'Days_in_week' ] ]

# dayOfWeek = Something like ... MTWHF
# goalTime = "H:M:S"
# classLink = "Link of whatever is after classroom=

def howLongCanIStayFor( classLink_, goalTime, dayOfWeek, doNotPrintClassSize = False ):
  classLink = "https://sa.ucla.edu/ro/Public/SOC/Results/ClassroomDetail?term=22W&classroom=" + classLink_
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

  # focus on the day we are looking for
  jsonSchedule = filterByDayInWeek( jsonSchedule, dayOfWeek )

  numClasses = str( len( jsonSchedule ) )
  if ( len( numClasses ) == 1 ):
    numClasses = "0" + numClasses

  if not doNotPrintClassSize:
    print( numClasses + " class -- ", end="" )

  # making the assumption that each day's classes are orderd by strt_time

  timefmt = "%H:%M:%S"
  goalTime = datetime.strptime( goalTime, timefmt )

  for cl in jsonSchedule:
    startTime = datetime.strptime( cl[ 'strt_time' ], timefmt )
    endTime = datetime.strptime( cl[ 'stop_time' ], timefmt )

    if ( goalTime >= startTime and goalTime < endTime ):
      # class is not available
      return( "OCCUP" )

  # At this point, the class is avaible. Let's see how long you can stay.

  lastTime = None
  for cl in jsonSchedule:
    startTime = datetime.strptime( cl[ 'strt_time' ], timefmt )

    if ( goalTime < startTime ):
      return( "AVAIL for " + str( startTime - goalTime ) )

  # At this point, there are no more classes scheduled.
  return( "AVAIL 12:00:00" )

