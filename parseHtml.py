#Simple script to extrat classrooms from the html dropdown menu
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
      pass

    def handle_endtag(self, tag):
      pass

    def handle_data(self, data):
      data = " ".join(data.split())
      if ( len( data ) == 0 ):
        pass
      else:
        print( data )

f = open( "dropdown.html", 'r' )
contents = f.read()
parser = MyHTMLParser()
parser.feed( contents )
