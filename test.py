# https://ru.stackoverflow.com/questions/681594/json-post-%D0%B7%D0%B0%D0%BF%D1%80%D0%BE%D1%81-python

import requests
import json

headers = {
    'Content-type': 'application/json',  # Определение типа данных
    'Accept': 'text/plain',
    'Content-Encoding': 'utf-8'
}
data = {}
data['username'] = 'test_user'
data['password'] = 'test_pass'
data['format'] = 'ascii'

def test_request():
    print(' ==== test_request ====')
    url = 'http://127.0.0.1:5000/api/request/'
    # events start at '1998-05-08 16:35:38' and end at '1998-05-08 16:35:51'
    data['start_time'] = '1078741520'
    data['end_time'] = '1078741540'
    print('Request:', data)

    #fout = open('test_response.html', 'wb')
    answer = requests.post(url, data=json.dumps(data), headers=headers) # отправка запроса методом post. Data преобразуется из словаря в json.
    if answer.status_code != 200:
        print('Invalid response: %d for %s\n    %s' % (answer.status_code, url, answer.content))
        #fout.write(answer.content)
        #fout.close()
        return
    content = json.loads(answer.content)  # преобразование из формата json в словарь
    print('Response:', content)
    #fout.write(answer.content)
    #fout.close()

def test_my_requests():
    print(' ==== test_my_requests ====')
    url = 'http://127.0.0.1:5000/api/my_requests/'
    print('Request:', data)
    answer = requests.post(url, data=json.dumps(data), headers=headers)
    if answer.status_code != 200:
        print('Invalid response: %d for %s\n    %s' % (answer.status_code, url, answer.content))
        return
    content = json.loads(answer.content)
    print('Response:', content)

def test_download(filename):
    print(' ==== test_download ====')
    url = 'http://127.0.0.1:5000/api/data/'+filename
    print('Request:', data)
    answer = requests.post(url, data=json.dumps(data), headers=headers)
    if answer.status_code != 200:
        print('Invalid response: %d for %s\n    %s' % (answer.status_code, url, answer.content))
        return
    print('Response:', answer.content)

def test_request_status(uuid):
    print(' ==== test_request_status ====')
    url = 'http://127.0.0.1:5000/api/request_status/'+uuid+'/'
    print('Request:', data)
    answer = requests.post(url, data=json.dumps(data), headers=headers)
    if answer.status_code != 200:
        print('Invalid response: %d for %s\n    %s' % (answer.status_code, url, answer.content))
        return
    content = json.loads(answer.content)
    print('Response:', content)

if __name__ == '__main__':
    test_request()
    test_my_requests()
    test_request_status('60a1fa84-3aa7-46a8-a17e-5a99336b8d69')
    test_download('60a1fa84-3aa7-46a8-a17e-5a99336b8d69.txt')
