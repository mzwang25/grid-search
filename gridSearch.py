import sys
from getClass import howLongCanIStayFor

# classesToSearch is an array of class names ... will format it
def getClassLinks( classesToSearch ):
  # format the classes to match the grid search format
  i = 0
  for room in classesToSearch:
    formattedStr = ""
    roomName = room.split( ' ' )[ 0 ]
    roomNum = room.split( ' ' )[ 1 ]

    # room name is 8 chars. If not enough, '+' are added
    formattedStr += roomName
    while ( len( formattedStr ) != 8 ):
      formattedStr += '+'

    formattedStr += "%7C"

    # now we replace the last two "+" with room letters (up to two)

    if ( roomNum[ 0 : 2 ].isalpha() ):
      # first two chars alpha
      formattedStr += roomNum[ 0 ] + roomNum[ 1 ]
      roomNum = roomNum[ 2 : ]

    elif ( roomNum[ 0 ].isalpha() ):
      # first char is alpha
      formattedStr += roomNum[ 0 ] + "+"
      roomNum = roomNum[ 1 : ]

    else:
      formattedStr += "+" + "+"

    # remove any letters at the end of the roomnum
    suffix = ""
    if ( roomNum[ -2 : ].isalpha() ):
      suffix = roomNum[ -2 : ]
      roomNum = roomNum[ 0 : -2 ]

    elif ( roomNum[ -1 : ].isalpha() ):
      suffix = roomNum[ -1 : ]
      roomNum = roomNum[ 0 : -1 ]

    # add other numbers ... add 0s if not enough (5 digits)
    while ( len( roomNum ) != 5 ):
      roomNum = "0" + roomNum

    formattedStr += roomNum

    # finally let's add the suffix
    formattedStr += suffix

    while ( len( formattedStr ) != 20 ):
      formattedStr += "+"

    classesToSearch[ i ] = formattedStr
    i += 1

  return classesToSearch

def main():
  # grab all classes from stdin, and turn it into links
  if ( len( sys.argv ) != 3 ):
    print( "Must have two arguments" )
    print( "ex. ./thisfile 12:00:00 w" )
    exit( 1 )

  sys.argv[ 2 ] = sys.argv[ 2 ].capitalize()

  if ( len( sys.argv[ 2 ] ) != 1 or ( not sys.argv[ 2 ] in "MTWRF" ) ):
    print( sys.argv[ 2 ] + " is not a valid day of week" )
    exit( 1 )

  classesToSearch = []
  names = []
  for line in sys.stdin:
    classesToSearch.append( line.strip( '\n' ) )
    names.append( line.strip( '\n' ) )

  classLinks = getClassLinks( classesToSearch )
  goalTime = sys.argv[ 1 ]
  dayOfWeek = sys.argv[ 2 ]

  for i in range( 0, len( classLinks ) ):
    print( names[ i ] )
    print( "  -- ", end="" )
    howLongCanIStayFor( classLinks[ i ], goalTime, dayOfWeek )

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    exit( 0 )
