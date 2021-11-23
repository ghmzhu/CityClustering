import urllib.error, urllib.request, urllib.parse
import http.cookiejar
import json
import tools

def crawlLocation():
    baseUrl = r"https://restapi.amap.com/v3/config/district?"
    handler = urllib.request.BaseHandler()
    opener = urllib.request.build_opener(handler)
    location = []

    def preWrite():
        get_request = urllib.request.Request(url)
        get_response = opener.open(get_request)
        ret = get_response.read().decode()
        ret_dict = json.loads(ret)
        for i in range(len(ret_dict['districts'][0]['districts'])):
            for j in range(len(ret_dict['districts'][0]['districts'][i]['districts'])):
                ret_dict['districts'][0]['districts'][i]['districts'][j]['province'] = ret_dict['districts'][0]['districts'][i]['name']
                location.append(ret_dict['districts'][0]['districts'][i]['districts'][j])
        print(location)


    url = baseUrl + 'subdistrict=2&key=8d4853811af6c69be20791c126e59e3e'
    print("start: " + url)
    print("done: urlopen")

    preWrite()

    print("Writing Json...")
    filename = r"./data/location.json"
    with open(filename, 'w', encoding = 'utf-8') as file_obj:
        json.dump(location, file_obj, ensure_ascii=False)
    print("Finish Writing!")

crawlLocation()
