import requests
import json
import time
def textExtraction(image_data):
  pg1=0
  pg2=0
  pg3=0
  pg4=0
  endpoint = "###############"
  subscription_key = "################"
  text_recognition_url = endpoint + "vision/v3.0/read/analyze"
  #image_data = open(image_path, "rb").read()
  headers = {'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/octet-stream'}
  response = requests.post(text_recognition_url, headers=headers, data=image_data)
  location=response.headers["Operation-Location"]
  analysis = {}
  poll = True
  headers = {'Ocp-Apim-Subscription-Key': subscription_key}
  while (poll):
    time.sleep(1)
    response_final = requests.get(location, headers=headers)
    analysis = response_final.json()
    if ("analyzeResult" in analysis):
      poll = False
    if ("status" in analysis and analysis['status'] == 'failed'):
      poll = False
    elif ("status" in analysis and analysis['status'] == 'succeeded'):
      #print("Successfull ! goto JSON file for output")
      f = open("AzureJsonResult.json", "w+")
      f.write(json.dumps(analysis, indent=4))
      f.close()
      poll = False
  kit=[]
  for page in analysis['analyzeResult']['readResults']:
    bg=page['height']*.008
    i=0
    while i<len(page['lines']):
      k=0
      kit.append([page['lines'][i]['text']])
      for j in range(i+1,len(page['lines'])):
        if(abs(page['lines'][i]['boundingBox'][1]-page['lines'][j]['boundingBox'][1])<bg):
          if(kit[-1][0]==page['lines'][i]['text']):
            kit[-1].append(page['lines'][j]['text'])
            k=j+1
      i=i+1
      if(k>0):
        i=k
  #print(kit)
  for element in kit:
    if(type(element)==list):
      kit[kit.index(element)] = ' '.join(element)
  
  for pt in kit:
    '''print(pt[0])'''
    if(pt[0:8]=="Due Date"):
      pg2=pt[9:]
      #print("Due Date:",pg2)
    if(pt[0:7]=="Payable"):
      pg4=pt[8:]
      #print("Bill Amount:",pg4)
    if(pt[0:2]=="C#"):
      pg1=pt[3:]
      #print("Consumer Number:",pg1)
    if(pt[0:10]=="Disconn Dt"):
      pg3=pt[12:]
      #print("Disconn Date:",pg3)
  return pg1,pg2,pg3,pg4;
