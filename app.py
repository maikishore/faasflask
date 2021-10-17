from flask import Flask
from flask.globals import g
from flask_cors import CORS, cross_origin
from flask import Flask
from youtube_transcript_api import YouTubeTranscriptApi




from flask import Flask, request
from flask.globals import g

import json
app = Flask(__name__)

@app.route('/ammaanaanagurudevayanamaha')
def hello_world():
    return 'Hello Sammy Ammaa!'

@app.route('/')
def hello_world():
    return 'Hello Sammy Ammaa!'

@app.route('/getsubtitles', methods=['POST'])
def videotranscript():
    request_json = request.get_json()
    video_url = request_json.get('video_url')
    mode=""
    srt=[]

    try:
        url = video_url.split("=", 1)[1]
    
        transcript = YouTubeTranscriptApi.get_transcript(url)

        transcript_list = YouTubeTranscriptApi.list_transcripts(url)
        transcripts = transcript_list.find_transcript(['de', 'en'])
       
      
       # print(transcripts)
        x = {
            
            "captions":transcript,
             "mode":json.dumps(transcripts.is_generated),
            "length":len(srt)         
        
        }
    except Exception as e:
       # print(e)
        x = {
            "captions": ["Subtitles other than youtube videos comming soon!"],
          
        }
    return json.dumps(x)