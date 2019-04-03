import pprint, json, requests
from .models import Pill
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse


serviceKey = "sYYsbAStv5lTMH32zXdixfecuB3dMciY5lyOva1NYa0rQD2odfRg82LZn%2F3QBqa%2BerqaXm28HDph%2FcPI%2BQe7Tw%3D%3D"


def health(request):
    return JsonResponse({})

def request_pills(request):
    return JsonResponse({})
    
def request_pills_oldman(request):
    nugu_body = json.loads(request.body, encoding='utf-8')
    # pprint.pprint(nugu_body)
    '''
    {'action': {'actionName': 'request_pills_oldman',
            'parameters': {'pills_a': {'type': 'PILLS', 'value': '타이레놀'},
                           'request_oldman': {'type': 'OLDMANCARE',
                                              'value': '노인주의'}}},
 'context': {'device': {'state': {}, 'type': 'speaker'},
             'session': {'id': '8826ea31-6550-4eb3-a5c7-ed79fbeec36f',
                         'isNew': True,
                         'isPlayBuilderRequest': True},
             'supportedInterfaces': None},
 'version': '2.0'}
 '''
    
    if nugu_body.get('action').get('parameters').get('request_oldman'):
        answer_oldman_pill = nugu_body.get("action").get('parameters').get('pills_a').get('value')

    url = f"http://apis.data.go.kr/1470000/DURPrdlstInfoService/getPwnmTabooInfoList?ServiceKey={serviceKey}&itemName={answer_oldman_pill}"
    responses = requests.get(url)
    response = BeautifulSoup(responses.content, 'lxml-xml')
    cnt = response.find('totalCount')
    cnt = int(cnt.text)
    
    if cnt >= 1:
        answer_oldman = '권장하지 않습니다. 전문의와 상의하세요.'
    else:
        answer_oldman = '드셔도 괜찮아요.'
    
    result = nugu_body
    result['output'] = {'answer_oldman' : answer_oldman, 'answer_oldman_pill':answer_oldman_pill}
    result['resultCode'] = 'OK'
    # pprint.pprint(result)
    
    return JsonResponse(result)


def request_pills_pregnant(request):
    nugu_body = json.loads(request.body, encoding='utf-8')
    pprint.pprint(nugu_body)
    '''
    {'action': {'actionName': 'request_pills_pregnant',
                'parameters': {'pills_a': {'type': 'PILLS', 'value': '타이레놀'},
                               'request_pregnant': {'type': 'PREGNANT',
                                                    'value': '임산부'}}},
     'context': {'device': {'state': {}, 'type': 'speaker'},
                 'session': {'id': '98c206ea-202b-4504-8534-e785058f7c0d',
                             'isNew': True,
                             'isPlayBuilderRequest': True},
                 'supportedInterfaces': None},
     'version': '2.0'}
     '''
    
    if nugu_body.get('action').get('parameters').get('request_pregnant'):
        answer_pregnant_pill = nugu_body.get("action").get('parameters').get('pills_a').get('value')
        
    url = f"http://apis.data.go.kr/1470000/DURPrdlstInfoService/getPwnmTabooInfoList?ServiceKey={serviceKey}&itemName={answer_pregnant_pill}"
    responses = requests.get(url)
    response = BeautifulSoup(responses.content, 'lxml-xml')
    cnt = response.find('totalCount')
    cnt = int(cnt.text)
    
    if cnt >= 1:
        answer_pregnant = '권장하지 않습니다. 전문의와 상의하세요.'
    else:
        answer_pregnant = '임산부가 드셔도 괜찮아요.'
        
    result = nugu_body
    result['output'] = {'answer_pregnant' : answer_pregnant, 'answer_pregnant_pill':answer_pregnant_pill}
    result['resultCode'] = 'OK'
    
    return JsonResponse(result)
    

def request_pills_interaction(request):
    nugu_body = json.loads(request.body, encoding='utf-8')
    pprint.pprint(nugu_body)
    '''
    '''
                'parameters': {'pills_a': {'type': 'PILLS', 'value': '타이레놀'},
                               'pills_b': {'type': 'PILLS', 'value': '디아제팜'}}},
     'context': {'device': {'state': {}, 'type': 'speaker'},
                 'session': {'id': 'c846abe7-67b4-4b58-bc96-b2418be7d8dc',
                             'isNew': True,
                             'isPlayBuilderRequest': True},
                 'supportedInterfaces': None},
     'version': '2.0'}
 '''
    if nugu_body.get('action').get('parameters').get('pills_b'):
        answer_pills_a = nugu_body.get("action").get('parameters').get('pills_a').get('value')
    
    url = f"http://apis.data.go.kr/1470000/DURPrdlstInfoService/getUsjntTabooInfoList?ServiceKey={serviceKey}&itemName={answer_pills_a}"
    responses = requests.get(url)
    response = BeautifulSoup(responses.content, 'lxml-xml')
    pillset = response.findAll('MIXTURE_ITEM_NAME')
    # pills_a = nugu_body.get("action").get('parameters').get('pills_a').get('value')
    answer_pills_b = nugu_body.get("action").get('parameters').get('pills_b').get('value')
    warning = False
    for r in pillset:
        if pills_b in str(r):
            warning = True

    if warning == True:
        answer_interaction = '아니오. 병용을 권장하지 않습니다. 전문의와 상의하세요.'
    else:
        answer_interaction = '함께 먹어도 괜찮아요.'
        
    result = nugu_body
    result['output'] = {'answer_pills_a' : answer_pills_a, 'answer_pills_b': answer_pills_b, 'answer_interaction': answer_interaction}
    result['resultCode'] = 'OK'
    # pprint.pprint(result)
    
    return JsonResponse(result)
    