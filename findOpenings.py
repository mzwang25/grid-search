import json
from datetime import datetime
from os import listdir
from makeUrlAndPullClassData import getClassLinks

# day is a single char ... MTWRF
def filterByDayInWeek( jsonObj, day ):
  return [ x for x in jsonObj if day in x[ 'Days_in_week' ] ]

def findOpening( classFileNm, dayOfWeek, goalTime, doNotPrintClassSize=True):
  # turn the text into a standard JSON
  jsonSchedule = None
  with open( classFileNm ) as f:
    jsonSchedule = json.loads( f.read() )

  # focus on the day we are looking for
  jsonSchedule = filterByDayInWeek( jsonSchedule, dayOfWeek )

  numClasses = str( len( jsonSchedule ) )
  if ( len( numClasses ) == 1 ):
    numClasses = "0" + numClasses

  if not doNotPrintClassSize:
    print( numClasses + " class -- ", end="" )

  if len( jsonSchedule ) < 5: # Low use rooms are typically locked
      return "OCCUP"

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
      return( "AVAIL " + str( startTime - goalTime ) )

  # At this point, there are no more classes scheduled.
  return( "AVAIL 12:00:00" )

if __name__ == "__main__":
  dataDir = "classScheduleData/"
  files = listdir( dataDir )
  schedule = { "M" : {},
               "T" : {},
               "W" : {},
               "R" : {},
               "F" : {} }
  schedule[ "M" ] = { 8 : {}, 9 : {}, 10 : {}, 11 : {},
                      12 : {}, 13 : {}, 14 : {}, 15 : {},
                      16 : {}, 17 : {} }
  schedule[ "T" ] = { 8 : {}, 9 : {}, 10 : {}, 11 : {},
                      12 : {}, 13 : {}, 14 : {}, 15 : {},
                      16 : {}, 17 : {} }
  schedule[ "W" ] = { 8 : {}, 9 : {}, 10 : {}, 11 : {},
                      12 : {}, 13 : {}, 14 : {}, 15 : {},
                      16 : {}, 17 : {} }
  schedule[ "R" ] = { 8 : {}, 9 : {}, 10 : {}, 11 : {},
                      12 : {}, 13 : {}, 14 : {}, 15 : {},
                      16 : {}, 17 : {} }
  schedule[ "F" ] = { 8 : {}, 9 : {}, 10 : {}, 11 : {},
                      12 : {}, 13 : {}, 14 : {}, 15 : {},
                      16 : {}, 17 : {} }

  fileFormatted = [ "" ] * len( files )
  for i in range( 0, len( files ) ):
    cp = files[ i ]
    fileFormatted[ i ] = cp[ 0 : -5 ].replace( '_', ' ' )

  classLinks = getClassLinks( fileFormatted ) 
  classLinkPrefix = "https://sa.ucla.edu/ro/Public/SOC/Results/ClassroomDetail?term=22S&classroom="

  for i in range( 0, len( files ) ):
    for day in [ "M", "T", "W", "R", "F" ]:
      for hr in range( 8, 18 ):
        result = findOpening( dataDir + files[ i ],
                              day,
                              str( hr ) + ":00:00" )
        resultArr = result.split( ' ' )
        if ( resultArr[ 0 ] == 'AVAIL' ):
          schedule[ day ][ hr ][ files[ i ][ : -5 ] ] = [ resultArr[ 1 ], classLinkPrefix + classLinks[ i ] ]

  print( json.dumps( schedule, indent=1, sort_keys=True ) )
  
