from django.shortcuts import render, redirect

from .models import *
from .helpers.customResponse import Custom
from .helpers.constant import Constant
from .helpers.serializer import *
from smartmeeting.settings import *

import json
from datetime import timedelta
from datetime import datetime
import random
import string
import jwt

from django.http.response import JsonResponse
from django.http import HttpResponse
from django.contrib import messages

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import status

from django.contrib.auth.models import User,auth
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required 

from django.contrib.auth import get_user_model
User = get_user_model()


# Model Library
import sumy
import pandas as pd
import numpy as np
import joblib
import os

from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser

import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

# Speech to text data
import speech_recognition as sr

# MP3 to WAP
from os import path
from pydub import AudioSegment

# import model file
from vosk import Model,  KaldiRecognizer
import subprocess
from pydub import AudioSegment
from pydub.playback import play

import sys
sys.path.append('/usr/local/bin/ffmpeg')


# Create your views here.
@api_view(['GET',])
def index(request):
    return HttpResponse("DOne !!!")


# @api_view(['POST',])
@csrf_exempt
def uploadAudio(request):

    # fileName = request.FILES

    print("Req - ", request)


    print("\nPost - ", request.POST)

    print("\nFiles - ", request.FILES)

    # print(fileName)

    # original_text = 'Junk foods taste good that’s why it is mostly liked by everyone of any age group especially kids and school going children.They generally ask for the junk food daily because they have been trend so by their parents from the childhood. They never have been discussed by their parents about the harmful effects of junk foods over health. According to the research by scientists, it has been found that junk foods have negative effects on the health in many ways.They are generally fried food found in the market in the packets. They become high in calories, high in cholesterol, low in healthy nutrients, high in sodium mineral, high in sugar, starch, unhealthy fat, lack of protein and lack of dietary fibers. Processed and junk foods are the means of rapid and unhealthy weight gain and negatively impact the whole body throughout the life. It makes able a person to gain excessive weight which is called as obesity. Junk foods tastes good and looks good however do not fulfil the healthy calorie requirement of the body. Some of the foods like french fries, fried foods, pizza, burgers, candy, soft drinks, baked goods, ice cream, cookies, etc are the example of high-sugar and high-fat containing foods. It is found according to the Centres for Disease Control and Prevention that Kids and children eating junk food are more prone to the type-2 diabetes. In type-2 diabetes our body become unable to regulate blood sugar level. Risk of getting this disease is increasing as one become more obese or overweight. It increases the risk of kidney failure. Eating junk food daily lead us to the nutritional deficiencies in the body because it is lack of essential nutrients, vitamins, iron, minerals and dietary fibers. It increases risk of cardiovascular diseases because it is rich in saturated fat, sodium and bad cholesterol. High sodium and bad cholesterol diet increases blood pressure and overloads the heart functioning. One who like junk food develop more risk to put on extra weight and become fatter and unhealthier. Junk foods contain high level carbohydrate which spike blood sugar level and make person more lethargic, sleepy and less active and alert. Reflexes and senses of the people eating this food become dull day by day thus they live more sedentary life. Junk foods are the source of constipation and other disease like diabetes, heart ailments, clogged arteries, heart attack, strokes, etc because of being poor in nutrition. Junk food is the easiest way to gain unhealthy weight. The amount of fats and sugar in the food makes you gain weight rapidly. However, this is not a healthy weight. It is more of fats and cholesterol which will have a harmful impact on your health. Junk food is also one of the main reasons for the increase in obesity nowadays.This food only looks and tastes good, other than that, it has no positive points. The amount of calorie your body requires to stay fit is not fulfilled by this food. For instance, foods like French fries, burgers, candy, and cookies, all have high amounts of sugar and fats. Therefore, this can result in long-term illnesses like diabetes and high blood pressure. This may also result in kidney failure. Above all, you can get various nutritional deficiencies when you don’t consume the essential nutrients, vitamins, minerals and more. You become prone to cardiovascular diseases due to the consumption of bad cholesterol and fat plus sodium. In other words, all this interferes with the functioning of your heart. Furthermore, junk food contains a higher level of carbohydrates. It will instantly spike your blood sugar levels. This will result in lethargy, inactiveness, and sleepiness. A person reflex becomes dull overtime and they lead an inactive life. To make things worse, junk food also clogs your arteries and increases the risk of a heart attack. Therefore, it must be avoided at the first instance to save your life from becoming ruined.The main problem with junk food is that people don’t realize its ill effects now. When the time comes, it is too late. Most importantly, the issue is that it does not impact you instantly. It works on your overtime; you will face the consequences sooner or later. Thus, it is better to stop now.You can avoid junk food by encouraging your children from an early age to eat green vegetables. Their taste buds must be developed as such that they find healthy food tasty. Moreover, try to mix things up. Do not serve the same green vegetable daily in the same style. Incorporate different types of healthy food in their diet following different recipes. This will help them to try foods at home rather than being attracted to junk food.In short, do not deprive them completely of it as that will not help. Children will find one way or the other to have it. Make sure you give them junk food in limited quantities and at healthy periods of time. '

    # parser=PlaintextParser.from_string(original_text,Tokenizer('english'))

    # pathOfModel = os.path.join(MODEL_PATH, 'lsa.joblib')
    # lsa = joblib.load(pathOfModel)
    # lsa_summary= lsa(parser.document,10)

    # summary = ""

    # # Printing the summary
    # for sentence in lsa_summary:
    #     summary += f'{sentence} '

    return Custom.successResponse([], Constant.varSuccess, status.HTTP_200_OK, "Data Received Successfully.")

    # except:
    #     return Custom.errorResponse([], Constant.varError, status.HTTP_400_BAD_REQUEST, "Something wents wrong.")


def generate_summary(text, summary_length):
    # Split the text into sentences
    sentences = nltk.sent_tokenize(text)
    
    # Create a TF-IDF vectorizer to extract features from the sentences
    vectorizer = TfidfVectorizer()
    sentence_vectors = vectorizer.fit_transform(sentences)
    
    # Apply LSA to reduce the dimensionality of the sentence vectors
    lsa = TruncatedSVD(n_components=100, algorithm='arpack', n_iter=10)
    sentence_vectors = lsa.fit_transform(sentence_vectors)
    
    # Calculate the sentence scores
    sentence_scores = np.sum(sentence_vectors, axis=1)
    
    # Sort the sentences by score and keep the top ones
    num_sentences = int(len(sentences) * summary_length)
    top_sentences_idx = np.argsort(-sentence_scores)[:num_sentences]
    top_sentences = [sentences[i] for i in top_sentences_idx]
    
    # Join the top sentences to form the summary
    summary = ' '.join(top_sentences)
    return summary

def voice_recognition(filename):
    print("Flagb 1")
    FRAME_RATE = 16000
    CHANNELS=1
    model = Model(model_name = "vosk-model-small-en-us-0.15")
    rec = KaldiRecognizer(model,FRAME_RATE)
    rec.SetWords(True)
    print("Flag 2")
    mp3 = AudioSegment.from_file(filename)
    mp3 = mp3.set_channels(CHANNELS)
    mp3 = mp3.set_frame_rate(FRAME_RATE)
    print("flag 3")
    #step = 45000
    transcript = ""
    #for i in range(0,len(mp3)):
    #    print(f"progress: {i/len(mp3)}")
    #    #segment = mp3[i:(i+step)]
        
    rec.AcceptWaveform(mp3.raw_data)
    result = rec.Result()
    print("flag 4")
    text=json.loads(result)['text']
    #transcript += text
    cased = subprocess.check_output("python recasepunc/recasepunc.py predict recasepunc/checkpoint",shell=True,text=True,input=text)
    cased = [cased]
    print("flag 5")
    summary = generate_summary(cased[0], 0.2) #we're generating 20% from the original text
    return summary


@api_view(['POST',])
def uploadAudio1(request):
    print("Postman - ")

    try:
        audio = request.FILES['audio']
    except:
        audio = None
    print(audio)

    audio = os.path.join(BASE_DIR, 'model/test.wav')
    print("Generated Summery - \n", voice_recognition(audio))

    return Custom.successResponse([], Constant.varSuccess, status.HTTP_200_OK, "Data Received Successfully.")


def sendSummary(request):


    return Custom.successResponse([], Constant.varSuccess, status.HTTP_200_OK, "Data Received Successfully.")