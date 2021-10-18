from flask import Flask
from flask.globals import g
from flask_cors import CORS, cross_origin
from flask import Flask
from youtube_transcript_api import YouTubeTranscriptApi
import spacy

import re

from flask import Flask, request
from flask.globals import g

import json
app = Flask(__name__)

@app.route('/ammaanaanagurudevayanamaha')
def hello_worlds():
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


@app.route('/entities', methods=['GET', 'POST'])
def entities():
    
    nlp = spacy.load('en_core_web_sm')
    try:

        entity_list = []
        data = json.loads(request.data)
        note = data['note']
        note = re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", note)

        doc = nlp(note)

        res = []
        t = []
        for each in doc.ents:
            entity_list.append(each.text)

        if len(entity_list) == 0:
            res.append({'key': 0, 'label': "None"})
        print("text")
        print("=======>", entity_list)

        for each in range(0, len(entity_list)):
            if entity_list[each] not in t:
                res.append({'key': each, 'label': entity_list[each]})
                t.append(entity_list[each])

        data = {'entities': res}

        return json.dumps(data)
    except Exception as e:
        print(e)

        return {'entities': []}


if __name__ == "__main__":
    app.run(port=5000, debug=True)