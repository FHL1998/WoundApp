import json
import urllib.request
import webbrowser

from kivy import args
from kivy.network.urlrequest import UrlRequest


def open_website(self, link):
    webbrowser.open(link)


url = "http://oliverfan.top/posts/2adb/"
name = []
email = []
website = []

# req=urllib.request.Request(url)
# resp=urllib.request.urlopen(req)
# webbrowser.open(url)
# def set_user1( *args):
# user1 = args[1]
# self.ids.user1.avatar = "https://cdn4.iconfinder.com/data/icons/avatars-21/512/avatar-circle-human-male-3-512.png"
# name = user1["name"]
# email = user1["email"]
# website = user1["website"]
# print(name)
# print(email)
# print(website)

# set_user1()

# def print(self):
# UrlRequest(
# "https://my-json-server.typicode.com/TOESL100/dataloader/users/1", self.set_user1, on_error=self.got_error,
# timeout=4
# )


# print(self)
# set_user1()
# UrlRequest("https://my-json-server.typicode.com/TOESL100/dataloader/users/1")
# user1 = args[2]
#data={
    #"id": 1,
    #"name": "OliverFan",
    #"username": "Bret",
    #"email": "fhlielts8@gmail.com",
    #"phone": "86-18810328618",
    #"website": "http://oliverfan.top"
#}

web = urllib.request.urlopen("https://my-json-server.typicode.com/TOESL100/dataloader/users/1")
data= json.loads(web.read())
json_str = json.dumps(data)
print("Python 原始数据：", repr(data))
print("JSON 对象：", json_str)

# 将 JSON 对象转换为 Python 字典
data1 = json.loads(json_str)
print("data1['name']: ", data1['name'])
print("data1['email']: ", data1['email'])
# import urllib2
import urllib.request


def get_record(url):
    data=[]
    resp = urllib.request.urlopen(url)
    ele_json = json.loads(resp.read())


    #for i in ele_json:
        #name.append(i.get("name"))
    print(name)
    print(ele_json)
    print(type(ele_json))
    #return ele_json
    #for list_item in ele_json:
        #for key, value in list_item.items():
            #if key == "NAME":
                #print(value)

if __name__ == '__main__':
    print(get_record('https://my-json-server.typicode.com/TOESL100/dataloader/users/1'))
    print(get_record('https://jsonplaceholder.typicode.com/users/1'))
