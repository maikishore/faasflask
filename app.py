from flask import Flask
from flask.globals import g
from flask_cors import CORS, cross_origin
from flask import Flask
from youtube_transcript_api import YouTubeTranscriptApi
import spacy

import re
from fastpunct import FastPunct

import textwrap
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
       
      
       # #print(transcripts)
        x = {
            
            "captions":transcript,
             "mode":json.dumps(transcripts.is_generated),
            "length":len(srt)         
        
        }
    except Exception as e:
       # #print(e)
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

        for each in doc:
            if each.tag_=="NNP":
                entity_list.append(each.text)

        if len(entity_list) == 0:
            res.append({'key': 0, 'label': "None"})
       
        for each in range(0, len(entity_list)):
            if entity_list[each] not in t:
                res.append({'key': each, 'label': entity_list[each]})
                t.append(entity_list[each])

        data = {'entities': res}

        return json.dumps(data)
    except Exception as e:
        ##print(e)

        return {'entities': []}



@app.route("/grammer", methods=["GET", "POST"])

def VideoNoteGrammer():

    fastpunct = FastPunct()
    data = json.loads(request.data)
    text=""
    #print("==>data",data["note"])

    try:
        note=data["note"]

        if len(note)>=1000:
            text=note[:1000]
        else:
            text=note
        text_wraps=textwrap.wrap(text,200)
        k=fastpunct.punct(
               text_wraps
                 )
     
        s=""
        for each in k:
            s=s+" "+each
        if len(note)>=1000:

            s=s+" "+note[1000:]

    
    
        
     
    
    
        return json.dumps({"note": s})

    except Exception as e:
        
        return str(e)

    return "100"



if __name__ == "__main__":
    app.run(port=8000, debug=False)