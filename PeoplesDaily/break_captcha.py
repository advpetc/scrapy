import pytesseract
import requests

url = "http://data.people.com.cn/servlet/validateCodeServlet"

payload = {}
headers = {
  'Cookie': 'JSESSIONID=4802FDDB230CBF528602BCB1F0041174; validateCode=yZjXm%2FLSfaUEsLvYALGelg%3D%3D'
}

response = requests.request("GET", url, headers=headers, data = payload)

print(response.text.encode('utf8'))


with open('pic1.jpg', 'wb') as handle:

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)
