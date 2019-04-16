import pprint, json, requests
from .models import Pill
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse


serviceKey = "sYYsbAStv5lTMH32zXdixfecuB3dMciY5lyOva1NYa0rQD2odfRg82LZn%2F3QBqa%2BerqaXm28HDph%2FcPI%2BQe7Tw%3D%3D"

# 노인 복용 여부 체크 함수
def check_oldman_pills(nugu_body, pill):
    global serviceKey
    url = f"http://apis.data.go.kr/1470000/DURPrdlstInfoService/getPwnmTabooInfoList?ServiceKey={serviceKey}&itemName={pill}"
    responses = requests.get(url)
    response = BeautifulSoup(responses.content, 'lxml-xml')
    cnt = response.find('totalCount')
    cnt = int(cnt.text)
    
    flag = 0
    if cnt >= 1:
        flag = 1
    return flag


# 임부 복용 여부 체크 함수
def check_pregnant_pills(nugu_body, pill):
    global serviceKey
    url = f"http://apis.data.go.kr/1470000/DURPrdlstInfoService/getPwnmTabooInfoList?ServiceKey={serviceKey}&itemName={pill}"
    responses = requests.get(url)
    response = BeautifulSoup(responses.content, 'lxml-xml')
    cnt = response.find('totalCount')
    cnt = int(cnt.text)
    
    flag = 0
    if cnt >= 1:
        flag = 1
    return flag
    
# 병용 여부 체크 함수
def check_interaction_pills(nugu_body, pilla, pillb):
    global serviceKey
    warning = False
    # answer_pills_a 입력하여 검사
    url = f"http://apis.data.go.kr/1470000/DURPrdlstInfoService/getUsjntTabooInfoList?ServiceKey={serviceKey}&itemName={pilla}"
    responses = requests.get(url)
    response = BeautifulSoup(responses.content, 'lxml-xml')
    pillset = response.findAll('MIXTURE_ITEM_NAME')
    
    # answer_pills_b 입력하여 검사
    url = f"http://apis.data.go.kr/1470000/DURPrdlstInfoService/getUsjntTabooInfoList?ServiceKey={serviceKey}&itemName={pillb}"
    responses = requests.get(url)
    response = BeautifulSoup(responses.content, 'lxml-xml')
    pillset += response.findAll('MIXTURE_ITEM_NAME')
    
    for r in pillset:
        if pilla in str(r) or pillb in str(r):
            warning = True
            break
    return warning


def health(request):
    return JsonResponse({})

def request_pills(request):
    return JsonResponse({})


def request_pills_oldman_default(request):
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
    
    flag = check_oldman_pills(nugu_body, answer_oldman_pill)
    if flag == 1:
        answer_oldman = '권장하지 않습니다. 전문의와 상의하세요.'
    else:
        answer_oldman = '드셔도 괜찮아요.'
    
    result = nugu_body
    result['output'] = {'answer_oldman' : answer_oldman, 'answer_oldman_pill':answer_oldman_pill}
    result['output'] = {'answer_oldman_front':answer_oldman_front, 'answer_oldman' : answer_oldman, 'answer_oldman_pill':answer_oldman_pill}
    # pprint.pprint(result)
    
    return JsonResponse(result)
    
    
def request_pills_oldman_complex(request):
    nugu_body = json.loads(request.body, encoding='utf-8')

    if nugu_body.get('action').get('parameters').get('request_oldman'):
        answer_oldman_pill_a = nugu_body.get("action").get('parameters').get('pills_a').get('value')
        answer_oldman_pill_b = nugu_body.get("action").get('parameters').get('pills_b').get('value')
    
    flag_a = check_oldman_pills(nugu_body, answer_oldman_pill_a)
    flag_b = check_oldman_pills(nugu_body, answer_oldman_pill_b)
    warning = check_interaction_pills(nugu_body, answer_oldman_pill_a, answer_oldman_pill_b)
    
    answer_oldman_interaction_complex = ""
    # 2. 노인금기 약품 조회
    if flag_a + flag_b == 1 :  # 둘 중 하나가 노인금기 약품일 경우
        if flag_a == 1 and flag_b == 0 :  # A 약품 -> 노인금기
            answer_oldman_pill_a = '65세 이상이라면 ' + answer_oldman_pill_a
            answer_oldman_front = 'ㄷ면 안되고,'
            answer_oldman_back = '먹어도 됩니다.'
        elif flag_a == 0 and flag_b == 1 :  # B 약품 -> 노인금기
            answer_oldman_pill_a = '65세 이상이라면 ' + answer_oldman_pill_a
            answer_oldman_back = '먹으면 안됩니다.'
            answer_oldman_front = '먹어도 되고,'
    elif flag_a + flag_b == 2 : # 둘다 금기약품
        answer_oldman_pill_a = '65세 이상'
        answer_oldman_pill_b = '말씀하신 약들'
        answer_oldman_back = '먹어도 됩니다.'
        answer_oldman_front = ''
    else : # 둘다 안전한 약품
        if warning == True:
            answer_oldman_interaction_complex = '두 약품은 병용을 권장하지 않습니다. 전문의와 상의하세요.'
        else:
            answer_oldman_interaction_complex = '두 약품은 함께 드셔도 괜찮아요.'
        answer_oldman_pill_a = '65세 이상'
        answer_oldman_pill_b = '말씀하신 약들'
        answer_oldman_back = '먹어도 됩니다.'
        answer_oldman_front = ''

    result = nugu_body
    result['output'] = {'answer_oldman_interaction_complex' : answer_oldman_interaction_complex,
                        # 'answer_pregnant_complex' : answer_pregnant_complex,
                        'answer_oldman_front':answer_oldman_front,
                        'answer_oldman_back':answer_oldman_back,
                        'answer_oldman_pill_a': answer_oldman_pill_a,
                        'answer_oldman_pill_b': answer_oldman_pill_b
                    }
    result['resultCode'] = 'OK'
    return JsonResponse(result)



def request_pills_pregnant(request):
    nugu_body = json.loads(request.body, encoding='utf-8')
    # pprint.pprint(nugu_body)
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
        

    flag = check_pregnant_pills(nugu_body, answer_pregnant_pill)
    if flag == 1:
        answer_pregnant = '권장하지 않습니다. 전문의와 상의하세요.'
    else:
        answer_pregnant = '임산부가 드셔도 괜찮아요.'
    
        
    result = nugu_body
    result['output'] = {'answer_pregnant' : answer_pregnant, 'answer_pregnant_pill':answer_pregnant_pill}
    result['resultCode'] = 'OK'
    
    return JsonResponse(result)
    

def request_pills_pregnant_complex(request):
    nugu_body = json.loads(request.body, encoding='utf-8')
    # pprint.pprint(nugu_body)
    '''
    {'action': {'actionName': 'request_pills_pregnant_complex',
            'parameters': {'pills_a': {'type': 'PILLS', 'value': '디아제팜'},
                           'pills_b': {'type': 'PILLS', 'value': '타이레놀'},
                           'request_interaction_pregnant': {'type': 'PREGNANT',
                                                            'value': '임산부'},
                           'request_oldman_pills_b': {'type': 'PILLS',
                                                      'value': '타이레놀'},
                           'request_oldman_pregnant': {'type': 'PREGNANT',
                                                       'value': '임산부'},
                           'request_pregnant': {'type': 'PREGNANT',
                                                'value': '임산부'},
                           'request_pregnant_pills_b': {'type': 'PILLS',
                                                        'value': '타이레놀'}}},
 'context': {'device': {'state': {}, 'type': 'speaker'},
             'session': {'id': '1306a892-8c25-4e59-a0c5-629435946410',
                         'isNew': True,
                         'isPlayBuilderRequest': True},
             'supportedInterfaces': None},
 'version': '2.0'}
 '''
    if nugu_body.get('action').get('parameters').get('request_pregnant'):
        answer_pregnant_pill_a = nugu_body.get("action").get('parameters').get('pills_a').get('value')
        answer_pregnant_pill_b = nugu_body.get("action").get('parameters').get('pills_b').get('value')
    
    flag_a = check_pregnant_pills(nugu_body, answer_pregnant_pill_a)
    flag_b = check_pregnant_pills(nugu_body, answer_pregnant_pill_b)
    warning = check_interaction_pills(nugu_body, answer_pregnant_pill_a, answer_pregnant_pill_b)
    
    # 1. 병용금기 여부 확인 후 결과값 저장
    # if warning == True :  # A, B 약품 병용금기
    #     answer_pregnant_interaction_complex = '두 약품은 병용을 권장하지 않습니다. 전문의와 상의하세요.'
    # else:
    #     answer_pregnant_interaction_complex = '두 약품은 함께 드셔도 괜찮아요.'
    
    answer_pregnant_interaction_complex = ""
    # 2. 임부금기 약품 조회
    if flag_a + flag_b == 1 :  # 둘 중 하나가 임부금기 약품일 경우
        if flag_a == 1 and flag_b == 0 :  # A 약품 -> 임부금기
            answer_pregnant_pill_a = '임산부라면 ' + answer_pregnant_pill_a
            answer_pregnant_front = '먹으면 안되고,'
            answer_pregnant_back = '먹어도 됩니다.'
        elif flag_a == 0 and flag_b == 1 :  # B 약품 -> 임부금기
            answer_pregnant_pill_a = '임산부라면 ' + answer_pregnant_pill_a
            answer_pregnant_back = '먹으면 안됩니다.'
            answer_pregnant_front = '먹어도 되고,'
    elif flag_a + flag_b == 2 : # 둘다 금기약품
        answer_pregnant_pill_a = '임산부'
        answer_pregnant_pill_b = '말씀하신 약들'
        answer_pregnant_back = '먹으면 안됩니다.'
        answer_pregnant_front = ''
    else : # 둘다 안전한 약품
        if warning == True:
            answer_pregnant_interaction_complex = '두 약품은 병용을 권장하지 않습니다. 전문의와 상의하세요.'
        else:
            answer_pregnant_interaction_complex = '두 약품은 함께 드셔도 괜찮아요.'
        answer_pregnant_pill_a = '임산부'
        answer_pregnant_pill_b = '말씀하신 약들'
        answer_pregnant_back = '먹어도 됩니다.'
        answer_pregnant_front = ''
    
    result = nugu_body
    result['output'] = {'answer_pregnant_interaction_complex' : answer_pregnant_interaction_complex,
                        # 'answer_pregnant_complex' : answer_pregnant_complex,
                        'answer_pregnant_front':answer_pregnant_front,
                        'answer_pregnant_back':answer_pregnant_back,
                        'answer_pregnant_pill_a': answer_pregnant_pill_a,
                        'answer_pregnant_pill_b': answer_pregnant_pill_b
                    }
    result['resultCode'] = 'OK'
    
    return JsonResponse(result)


def request_pills_interaction(request):
    nugu_body = json.loads(request.body, encoding='utf-8')
    # pprint.pprint(nugu_body)
    '''
    {'action': {'actionName': 'request_pills_interaction',
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
    answer_pills_b = nugu_body.get("action").get('parameters').get('pills_b').get('value')
    
    # warning = False
    # # answer_pills_a 입력하여 검사
    # url = f"http://apis.data.go.kr/1470000/DURPrdlstInfoService/getUsjntTabooInfoList?ServiceKey={serviceKey}&itemName={answer_pills_a}"
    # responses = requests.get(url)
    # response = BeautifulSoup(responses.content, 'lxml-xml')
    # pillset = response.findAll('MIXTURE_ITEM_NAME')
    
    # # answer_pills_b 입력하여 검사
    # url = f"http://apis.data.go.kr/1470000/DURPrdlstInfoService/getUsjntTabooInfoList?ServiceKey={serviceKey}&itemName={answer_pills_b}"
    # responses = requests.get(url)
    # response = BeautifulSoup(responses.content, 'lxml-xml')
    # pillset += response.findAll('MIXTURE_ITEM_NAME')
    
    # for r in pillset:
    #     if answer_pills_b in str(r) or answer_pills_a in str(r):
    #         warning = True
    #         break
    warning = check_interaction_pills(nugu_body, answer_pills_a, answer_pills_b)
    
    if warning == True:
        answer_interaction = '병용을 권장하지 않습니다. 전문의와 상의하세요.'
    else:
        answer_interaction = '함께 먹어도 괜찮아요.'
        
    result = nugu_body
    result['output'] = {'answer_pills_a' : answer_pills_a, 'answer_pills_b': answer_pills_b, 'answer_interaction': answer_interaction}
    result['resultCode'] = 'OK'
    # pprint.pprint(result)
    
    return JsonResponse(result)