from keep_alive import keep_alive
from datetime import datetime
from time import sleep
import requests, html, threading

from bs4 import BeautifulSoup
import json
keep_alive()
api_token_telegram = "6457055340:AAHSdr2VP4L-LdbXk7O4GuAog9pXEbfzpL4"
chat_id_telegram = "6216790518"
url_notepad = "https://notepad.vn/dGhvbmdiYW9WbmVkdQ"
def write_notepad(content):
    content = {'content': content}
    r = requests.post("https://notepad.vn/update_data/dGhvbmdiYW9WbmVkdQ", data=content)
    if not 'true' in str(r.text):
        message = 'Write message error: ' + r
def read_notepad():
    r = requests.get(url_notepad).text
    content = r.split('class="contents" spellcheck="true">')[1].split('<')[0]
    content = html.unescape(content)


    return content.replace("'", '"')
def getUrlLogin():
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

    session = requests.session()


    _continue = session.get("https://user.vnedu.vn/sso//?use_cache=0&continue=tracuu.vnedu.vn/kqht/", headers=headers).text.split('<input type="hidden" name="continue" value="')[1].split('"')[0]
    loginQrToken = session.get("https://user.vnedu.vn/sso//?use_cache=0&continue=tracuu.vnedu.vn/kqht/", headers=headers).text.split('<input type="hidden" name="loginQrToken" value="')[1].split('"')[0]

    data = {
        'continue': _continue,
        'app_id': '1',
        'loginQrToken': loginQrToken,
        'txtUsername': '0356113982',
        'txtPassword': 'vinh123789',
        'txtCaptcha': ''
    }

    r = session.post('https://user.vnedu.vn/sso//?call=auth.login&jtoken=0.28540240782635906&jcode=1fb748c909cd17dc2d45054ef4abf073', headers=headers, data=data).json()
    return session.get(r['data']).text

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
def compare():
    # Lấy nội dung HTML
    html_content = getUrlLogin()

    # Phân tích HTML và tách bảng
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('div', class_='table-point-content').find('table')

    # Trích xuất tiêu đề và dữ liệu bảng
    headers = [th.get_text(strip=True) for th in table.find('thead').find_all('th')]
    data = []
    for row in table.find('tbody').find_all('tr'):
        cells = row.find_all(['th', 'td'])
        row_data = [cell.get_text(strip=True) for cell in cells]
        data.append(dict(zip(headers, row_data)))

    # Đường dẫn file JSON trạng thái hiện tại
    json_file_path = 'latest_data.json'

    # Đọc dữ liệu từ file JSON hiện tại
    try:
        current_data = json.loads(read_notepad())
        print(current_data)
    except FileNotFoundError:
        current_data = []

    # So sánh và cập nhật JSON
    def compare_and_update_json(new_data, existing_data, file_path):
        differences = []
        updated = False

        for new_subject in new_data:
            existing_subject = next((s for s in existing_data if s["Môn học"] == new_subject["Môn học"]), None)
            
            if existing_subject:
                for field in ["Đánh giá thường xuyên", "Giữa kỳ", "Cuối kỳ"]:
                    if new_subject.get(field) != existing_subject.get(field):
                        differences.append({
                            "Môn học": new_subject["Môn học"],
                            "Trường": field,
                            "Giá trị mới": new_subject.get(field, ""),
                            "Giá trị hiện tại": existing_subject.get(field, "")
                        })
                        existing_subject[field] = new_subject.get(field)
                        updated = True
            else:
                existing_data.append(new_subject)
                updated = True

        if differences:
            print("Các điểm khác biệt:")
            for diff in differences:
                srt = f"Môn học: {diff['Môn học']}, Trường: {diff['Trường']}, " + f"Giá trị mới: {diff['Giá trị mới']}, Giá trị hiện tại: {diff['Giá trị hiện tại']}"
                print(srt)
                to_discord(srt, True)
                send_telegram_message(srt)
        else:
            print("Không có sự khác biệt nào.")

        if updated:
            json_string = json.dumps(existing_data, ensure_ascii=False, indent=4)
            write_notepad(json_string)
            print("Dữ liệu JSON đã được cập nhật.")

    # Thực hiện so sánh và cập nhật
    compare_and_update_json(data, current_data, json_file_path)

while True:
    try:
        threading.Thread(target=compare, args=()).start()
        to_discord("", False)
        sleep(100)
        # exit()
    except Exception as e:
        print(e)
