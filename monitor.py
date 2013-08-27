#!/usr/bin/python

from subprocess import Popen, PIPE
from bottle import route, run, default_app
import io
import re
import os


@route('/tools/monitor')
def monitor():
    template = """
    <html>
    <head> <title> Twitter Monitor </title>   </head>
    <style media="screen" type="text/css">

        div {{font-size:200%}}

    </style>
    <body>
        <div>  
            <p>File size: {0:.2f}MB</p> 
            <p>Disk used: {1}</p> 
            <p>Latest tweet: {2}</p> 
        </div>  
    </body>
    </html>


    """
    #Get the amount of disk space used
    process = Popen(["df"], stdout=PIPE)
    output = process.communicate()[0]
    disk_used = output.split()[11]

    file_name = 'brickLaneStream.log'

    #get file size
    file_size = os.stat(file_name)[6]

    #get the latest tweet's time stamp
    BLOCK_SIZE = 4096
    f = io.open(file_name,'rb')
    file_size = os.stat(file_name)[6]
    print file_size
    rgx = '.*"created_at": "(.*?)"'
    counter = 10
    latest_tweet = "Could not get latest tweet date"
    buffer = ""
    while counter * BLOCK_SIZE < file_size:
        print 'inside of while'
        try:
            f.seek( -BLOCK_SIZE * counter   ,2)
            data = f.read( BLOCK_SIZE * counter  )
            print 'Looking at content'
            if 'created_at' in data  and re.match(rgx, data):
                latest_tweet = re.match(rgx, data).group(1)
                break
        except IOError:
            pass
            break
        counter += 10
    f.close()
    return template.format(file_size / 1024 /1024.0, disk_used, latest_tweet)

if __name__=='__main__':
    run(host='localhost', port=8080)

app = default_app()

