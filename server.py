from flask import Flask, render_template, request

app = Flask( __name__ )

@app.route( "/" )
def index():
  return render_template( "index.html" )

@app.route( "/submit" )
def submit():
  classname = request.args.get( "classname" )
  time = request.args.get( "time" )
  day = request.args.get( "day" )
  
  return render_template( "loading.html" )

if __name__ == "__main__":
  app.run()
