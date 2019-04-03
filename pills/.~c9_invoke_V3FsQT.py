#-*- coding: utf-8 -*-
import pprint, json, requests
                                                                        
import xml.etree.ElementTree
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.

serviceKey = "sYYsbAStv5lTMH32zXdixfecuB3dMciY5lyOva1NYa0rQD2odfRg82LZn%2F3QBqa%2BerqaXm28HDph%2FcPI%2BQe7Tw%3D%3D"
# serviceKey = URLEncoder.encode(serviceKey, "UTF-8")

def health(request):
    return JsonResponse({})
# serviceKey = URLEncoder.encode(serviceKey, "UTF-8");
def interaction(request):
    pprint.pprint(request.body)
    if request.method == 'POST':
        # nugu_body = json.loads(request.body, encoding='utf-8')
        aItem = request.POST.get("a")
        bItem = request.POST.get("b")
        url = f"http://apis.data.go.kr/1470000/DURPrdlstInfoService/getUsjntTabooInfoList?ServiceKey={serviceKey}&itemName={aItem}"
        print(url)
        responses = requests.get(url)
        response = BeautifulSoup(responses.content, 'lxml-xml')
        pprint.pprint(response)
    
        # pprint.pprint(nugu_body)
    serviceKey = service
    else:
        return render(request, 'pills/interaction.html')
    
def oldmanCare(request):
    global serviceKey    # 서비스 인증키 불러오기 (전역변수)
    
    # 요청변수(Request Parameter)
    typeName = "병용금기"    # DUR 유형
    ingrName = "클로르디아제폭시드"    # DUR 성분
    
    # DUR 품목정보 API
    # 서비스요청 URL
    url = f'http://apis.data.go.kr/1470000/DURIrdntInfoService/getOdsnAtentInfoList?ServiceKey={serviceKey}&typeName={typeName}&ingrName={ingrName}&numOfRows=3&pageNo=1'
    responses = requests.get(url)
    response = BeautifulSoup(responses.content, 'lxml-xml')
    pprint.pprint(response)
    return render(request, 'pills/oldmanCare.html', {'response': response})
    