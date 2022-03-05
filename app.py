from flask import Flask, render_template, request
from getClass import howLongCanIStayFor
from gridSearch import getClassLinks
import os, subprocess, copy

app = Flask( __name__ )

def getClassNmMatches( classNm ):
  matches = []
  grep = subprocess.check_output(['/usr/bin/grep', classNm, 'classrooms.txt'])
  return( grep.decode( 'utf-8' ).split( '\n' )[ 0 : -1 ] )
  

@app.route( "/" )
def index():
  return render_template( "index.html" )

@app.route( "/submit" )
def submit():
  classname = request.args.get( "classname" )
  time = request.args.get( "time" )
  day = request.args.get( "day" )

  names = []
  matches = getClassNmMatches( classname )

  for name in matches:
    names.append( name )
  classLinks = getClassLinks( matches )

  outputstr = ""
  for i in range( 0, len( classLinks ) ):
    outputstr += names[ i ] + " -- "
    outputstr += howLongCanIStayFor( matches[ i ], time, day, True )
    outputstr += "<br>"
  return outputstr

if __name__ == "__main__":
  app.run(port=5000)
