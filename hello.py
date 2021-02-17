import requests

url="http://40.115.35.164:8000/predict"

#url="http://localhost:8000/predict"

def request(filename):
    with open(filename,mode="rb") as f:
        img=f.read()
    test_res=requests.post(url+"/minimal",files={"image":img})
    if test_res.ok:
        print(test_res.text)
    else:
        print("Error")
        
        
def request_described(filename):
    with open(filename,mode="rb") as f:
        img=f.read()
    test_res=requests.post(url,files={"image":img})
    if test_res.ok:
        print(test_res.text)
    else:
        print("Error")
        
        
def request_detailed(filename):
    with open(filename,mode="rb") as f:
        img=f.read()
    test_res=requests.post(url+"/detailed",files={"image":img})
    if test_res.ok:
        print(test_res.text)
    else:
        print("Error")