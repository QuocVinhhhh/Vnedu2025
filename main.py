# import traceback
from keep_alive import keep_alive

keep_alive()

from datetime import datetime
from time import sleep
import json
# from urllib.parse import unquote
import requests, threading
import base64
import html


with open('json.txt', 'r', encoding='utf-8') as file:
    default_json = file.read()

url_notepad = "https://notepad.vn/dGhvbmdiYW9WbmVkdQ"
url = "aHR0cHM6Ly9hcGkucHJveHlzY3JhcGUuY29tL3YzL2ZyZWUtcHJveHktbGlzdC9nZXQ/cmVxdWVzdD1kaXNwbGF5cHJveGllcyZwcm90b2NvbD1odHRwJmNvdW50cnk9Vk4mdGltZW91dD05OTk5OTk5OSZwcm94eV9mb3JtYXQ9aXBwb3J0JmZvcm1hdD10ZXh0"
# url_telegram = "https://pushmore.io/webhook/PPw89b5TJ4uyNzmvCqrNkkwN"
api_token_telegram = "6457055340:AAHSdr2VP4L-LdbXk7O4GuAog9pXEbfzpL4"
chat_id_telegram = "6216790518"

jQuery = 'jQuery112409611886264735514_1726321203680'

link_0 = 'https://hocbadientu.vnedu.vn/sllservices/captcha/image.php'
link1 = f"https://hocbadientu.vnedu.vn/sllservices/index.php?callback=jQuery112409611886264735514_1726321203680&call=solienlac.checkSll&mahocsinh=2203059504&tinh_id=1&password=0356113982&namhoc=2024&dot_diem_id=0&_=1726321203683"
link2 = f"https://hocbadientu.vnedu.vn/sllservices/index.php?callback=jQuery112409611886264735514_1726321203680&call=solienlac.getSodiem&mahocsinh=2203059504&key=d33e425220d1f1184a9fb9a477055fd6&namhoc=2024&tinh_id=1&dot_diem_id=0&ngay_sinh=12%2F02%2F2007&_=1726321203684"

showScore = True
hoc_ky = 0

debug_mode = True


def write_notepad(content):
    content = {'content': content}
    r = requests.post("https://notepad.vn/update_data/dGhvbmdiYW9WbmVkdQ", data=content)
    if not 'true' in str(r.text):
        message = 'Write message error: ' + r
        # to_discord(r)
        # send_telegram_message(r)
def read_notepad():
    r = requests.get(url_notepad).text
    content = r.split('class="contents" spellcheck="true">')[1].split('<')[0]
    content = html.unescape(content)

    if len(content) < 5: 
            write_notepad(default_json)
            pdb('không có json, write json vào')
            return read_notepad()

    return content.replace("'", '"')

def decode_base64(encoded_string):
    try:
        decoded_bytes = base64.b64decode(encoded_string)
        decoded_string = decoded_bytes.decode('utf-8')
        return decoded_string
    except Exception as e:
        print("Lỗi khi giải mã Base64:", str(e))
        return None

def get_current_time():
    time = datetime.now()
    hour = time.strftime("%H")
    hour = str(int(hour) + 7)
    if int(hour) >= 24:
        if int(hour) == 24:
            hour = 0
        else:
            hour = str(int(hour) - 24)
    f = time.strftime(':%M:%S')
    return f'{hour}{f}'
def pdb(text):
    if debug_mode:
        print(f'[debug] {text}')

def to_discord(s, type):
    if type:
        data = {
            "username": "VnEdu Bot" 
        }
        data["embeds"] = [
            {
                "description" : s,
                "title" : "Cập Nhật Điểm"
            }
        ]
        requests.post("https://discord.com/api/webhooks/1149692352479379486/NSlRacGabe5Bi6jJD6G9Knn58iGqxKDxoksLagwcLhzTEpjw22wpIAAFfSXf-aU7nd_P", json=data)

    else:
        s = "Alive" + ' | ' + get_current_time()
        requests.post("https://discord.com/api/webhooks/1164948897681133659/bWo1iaFT8IoW8MJ582EOjy-Up7c4u8a3Grr3Cp5Voyd1Llw6fFG_q4sPT7CXFxhLtxsC", data={"content": s})
def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{api_token_telegram}/sendMessage'
    payload = {
        'chat_id': chat_id_telegram,
        'text': message
    }
    response = requests.post(url, data=payload)

def rq(proxy):
    try: 
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,pl;q=0.4',
            'Connection': 'keep-alive',
            # 'Cookie': 'PHPSESSID=83jhhhhlf87of6vf4li3v3fep6; BIGipServerAPP_EDU_HBDT=722837258.20480.0000',
            'Host': 'hocbadientu.vnedu.vn',
            'Referer': 'https://tracuu.vnedu.vn/',
            'Sec-Fetch-Dest': 'script',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
        # rquest = requests.get('https://tracuu.vnedu.vn/so-lien-lac/tra-cuu-diem/index.php?mahs=2203059504&fullname=Nguy%E1%BB%85n%20Qu%E1%BB%91c%20Vinh&key=0356113982&tinh_id=1&cap=3', headers=headers)
        tach = str(proxy).split(':')
        proxies = {
            'http':'http://{0}:{1}'.format(tach[0],tach[1]),
            'https':'http://{0}:{1}'.format(tach[0],tach[1]),
        }
        # proxies = None
        session = requests.session()
        # #------------------------------------------#
        for i in range(99):
            r = session.get(link_0, headers=headers, proxies=proxies)
            rq1 = session.get(link1, proxies=proxies, headers=headers)
            pdb(rq1.text)
            if "M\\u00e3 x\\u00e1c th\\u1ef1c kh\\u00f4ng \\u0111\\u00fang" in str(rq1.text):
                # send_telegram_message("Lỗi mã xác thực")
                rquest = session.get(link1, headers=headers)
                pdb('lỗi mã xác thực requests lại')
            else: break
            
        cookie_string = '; '.join([f'{name}={value}' for name, value in (rq1.cookies).items()])
        # headers = {'Cookie': cookie_string}
        response = session.get(link2, headers=headers, proxies=proxies).text
        pdb(response)
        for i in range(99):
            if "M\\u00e3 x\\u00e1c th\\u1ef1c kh\\u00f4ng \\u0111\\u00fang" in str(response):
                    send_telegram_message("Lỗi mã xác thực 2")
                    rquest = session.get(link2, headers=headers)
                    pdb('lỗi mã xác thực requests lại222')
            else: break
        response = response.split(f"{jQuery}(")[1].replace(")", "")
        parsed_response = json.loads(response)
        return parsed_response
    except Exception as e:
        pdb(e)
        # traceback.print_exc()

def check_compare(json1, json2):
    ten_mon_hoc = ""
    compare = []

    c = 0
    for item in json2:
        for key, value in item.items():
            if key == "ten_mon_hoc":
                # ten_mon_hoc = unquote(value)
                ten_mon_hoc = value
                continue
            if key in ["TX", "GK", "CK", "TK"]:
                for i in range(len(item[key])):
                    try:
                        matching_item = next(i for i in json1 if i["ten_mon_hoc"] == item["ten_mon_hoc"])
                        matching_entry = next((e for e in matching_item[key] if e["stt"] == item[key][i]["stt"]), None)
                        if matching_entry is None:
                            if showScore:
                                diem = item[key][i].get('diem', '')
                            else:
                                diem = "xxx"
                            compare.append(f"Môn: {ten_mon_hoc} | {key} | stt:{item[key][i]['stt']} | diem: {diem}")
                    except StopIteration:
                        compare.append(f"Môn: {ten_mon_hoc} không tồn tại trong JSON ban đầu.")
        c += 1
    return compare


def run(proxy):
    try:
        initial_json = json.loads(read_notepad())
        new_json = rq(proxy)['diem'][hoc_ky]["mon_hoc"]
        pdb(new_json)
        cmp_rtn = check_compare(initial_json, new_json)
        print(cmp_rtn)
        if cmp_rtn != []:
            for data in cmp_rtn:
                threading.Thread(target=(send_telegram_message), args=(data,)).start()
            to_discord("\n".join(cmp_rtn), True)
            # with open('initial_json.json', 'w', encoding='utf-8') as outfile:
            #     json.dump(new_json, outfile)
            write_notepad(str(new_json))
    except Exception as e:
        pdb(e)
        # traceback.print_exc()

while True:
    try:
        proxy = requests.get(decode_base64(url)).text
        # proxy = "103.57.211.92:3128\n"
        proxy = proxy.split("\n")
        proxy = [line.replace('\r', '') for line in proxy]
        for i in proxy:
            if i == '': continue
            pdb(i)
            threading.Thread(target=run, args=(i,)).start()
            # break
            # exit()
        to_discord("", False)
        sleep(100)
        # exit()
    except Exception as e:
        pdb(e)
# run(None)
