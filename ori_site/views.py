from django.shortcuts import render
from django.http import JsonResponse
from random import randint
import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from .models import Profile, Question
import math

@csrf_exempt
def RegisterView(request):
    if(request.method == 'POST'):
        data = json.loads(request.body.decode("utf-8"))
        try:
            player = Profile.objects.get(Phone_Number=data['phone'])
            return JsonResponse({"detail":"exists", "uid":player.uid, "lives":player.Lives}, safe=False)
        except:
            player = None
        profile = Profile.objects.create(Name=data['name'], Phone_Number=data['phone'], Email = data['email'])
        profile.SolvedQns = json.dumps([])
        profile.save()
        return JsonResponse({"detail":"Registered", "uid":profile.uid, "lives":3}, safe=False)
    return JsonResponse({"detail":"error"}, status=400, safe=False)

@csrf_exempt
def NextQnView(request):
    data = json.loads(request.body.decode("utf-8"))
    print(data)
    if('uid' not in data):
        return JsonResponse({"detail":"error"}, status=400, safe=False)
    player = Profile.objects.get(uid=data['uid'])
    done_qns = json.loads(player.SolvedQns)
    qs = list(Question.objects.all())
    if(len(qs)==len(done_qns)):
        player.Played = True
        player.save()
        return JsonResponse({"completed":True}, safe=False);
    i = randint(0,len(qs)-1)
    while str(qs[i].uid) in done_qns:
        i = randint(0,len(qs)-1)
    done_qns.append(str(qs[i].uid))
    player.SolvedQns = json.dumps(done_qns)
    player.save()
    return JsonResponse({"completed":False, "question_num":str(qs[i].uid),"question_text":qs[i].Question,"question_options":[qs[i].Option_1,qs[i].Option_2,qs[i].Option_3,qs[i].Option_4]}, safe=False)
    
"""q_uid, p_uid, answer, time_taken"""
@csrf_exempt
def CorrectAnsView(request): 
    data = json.loads(request.body.decode("utf-8"))
    print(data)
    if('q_uid' not in data):
        return JsonResponse({"detail":"error"}, status=400, safe=False)
    if('p_uid' not in data):
        return JsonResponse({"detail":"error"}, status=400, safe=False)
    question = Question.objects.get(uid=data['q_uid'])
    player = Profile.objects.get(uid=data['p_uid'])
    if(int(data['answer']) != question.Correct_Answer):
        player.Lives -= 1;
        return JsonResponse({"correct":False}, safe=False)
    player.Score += 500*question.Difficulty/(1+int(data['time_taken']))
    if(not player.Played):
        player.ConsideredScore = player.Score
    player.save()
    return JsonResponse({"correct":True}, safe=False)

@csrf_exempt
def FinallyView(request):
    data = json.loads(request.body.decode("utf-8"))
    if('uid' not in data):
        return JsonResponse({"detail":"error"}, status=400, safe=False)
    player = Profile.objects.get(uid=data['uid'])
    if not player.Played:
        player.ConsideredScore = player.Score
    score_send = math.floor(player.Score)
    player.Score = 0
    player.Played = True;
    player.Lives = 3;
    player.SolvedQns = json.dumps([])
    player.save()
    return JsonResponse({"detail":"success","score":score_send}, safe=False)
@csrf_exempt
def LeaderView(request):
    players = Profile.objects.all()
    max_score = -1
    player = None
    for p in players:
        if p.ConsideredScore > max_score:
            player = p
            max_score = p.ConsideredScore
    return JsonResponse({'name':player.Name, 'num':player.Phone_Number, 'sc':player.ConsideredScore, 'em':player.Email},safe=False);