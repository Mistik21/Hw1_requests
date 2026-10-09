import io
import requests
from bs4 import BeautifulSoup


def parser_html(text):
    soup = BeautifulSoup(text, "html.parser")
    result = {}
    code = []
    for table in soup.find("table").find_all("code"):
        code.append(table.text)
    for i in range(0, len(code), 2):
        result[code[i]] = code[i + 1]
    return result


def parser_html_route(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.find("code").text


def parser_html_route_teg_a(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.find("a").get("href")


ID = "908f4d71a61883c70a9081215d69fab9"
URL = "http://hw1.alexbers.com"

response = requests.get(URL, cookies={"user": ID})

result_html = response.content.decode()

request_count = 0
while response.status_code == 200:
    cookies = {}
    params = {}
    headers = {}
    body = {}
    request_count += 1
    if "При переходе выставьте следующие параметры запроса, указанные в таблице:" in result_html:
        params = parser_html(result_html[result_html.find("При переходе выставьте следующие параметры запроса, указанные в таблице:"):])
    if "Запрос должен иметь следующие заголовки:" in result_html:
        headers = parser_html(result_html[result_html.find("Запрос должен иметь следующие заголовки:"):])
    if "Запрос должен иметь следующие данные формы:" in result_html:
        body = parser_html(result_html[result_html.find("Запрос должен иметь следующие данные формы:"):])
    if "В запросе должны быть выставлены cookie:" in result_html:
        cookies = parser_html(result_html[result_html.find("В запросе должны быть выставлены cookie:"):])
    cookies["user"] = ID

    if "Отправьте GET-запрос" in result_html:
        rout_url = parser_html_route(result_html[result_html.find("Отправьте GET-запрос"):])
        response = requests.get(URL + rout_url, cookies=cookies, params=params, headers=headers,timeout=None)
    elif "Отправьте POST-запрос" in result_html:
        rout_url = parser_html_route(result_html[result_html.find("Отправьте POST-запрос"):])
        response = requests.post(URL + rout_url, cookies=cookies, params=params, headers=headers, data=body,timeout=None)
    elif "Загрузите файлы по адресу" in result_html:
        rout_url = parser_html_route(result_html[result_html.find("Загрузите файлы по адресу"):])
        files_dict = parser_html(result_html)
        files_to_send = [
            ('file', (fname, io.BytesIO(fcontent.encode('utf-8')), 'text/plain'))
            for fname, fcontent in files_dict.items()
        ]
        response = requests.post(URL + rout_url, cookies=cookies, files=files_to_send,timeout=None)
    elif "Перейдите по" in result_html:
        rout_url = parser_html_route_teg_a(result_html[result_html.find("Перейдите по"):])
        response = requests.get(URL + rout_url, cookies=cookies, params=params, headers=headers,timeout=None)
    else:
        print(result_html)
        break
    result_html = response.content.decode()

print(f"Запросов:{request_count}")
