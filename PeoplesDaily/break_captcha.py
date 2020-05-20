import pytesseract
import requests
'''
url = "http://data.people.com.cn/servlet/validateCodeServlet"

payload = {}
headers = {
  # 'Cookie': 'JSESSIONID=B1C8917EC212C621CA563B164854BDF5; validateCode=r7a%2FbEv%2BYi%2FQc2nOA2vdog%3D%3D'

    'Cookie': 'JSESSIONID=B1C8917EC212C621CA563B164854BDF5; validateCode=r7a%2FbEv%2BYi%2FQc2nOA2vdog%3D%3D'
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
'''
binary_data = b"\xe6\x8f\x90\xe7\xa4\xba\xe5\xa6\x82\xe6\x9e\x9c\xe6\x82\xa8\xe7\x9a\x84\xe8\xae\xbf\xe9\x97\xae\xe9" \
              b"\x87\x8f\xe8\xbf\x87\xe5\xa4\xa7\xe6\x88\x96\xe4\xbd\xbf\xe7\x94\xa8\xe8\xbd\xaf\xe4\xbb\xb6\xe5\xb7" \
              b"\xa5\xe5\x85\xb7\xe6\x8a\x93\xe5\x8f\x96\xe6\x95\xb0\xe6\x8d\xae\xef\xbc\x8c\xe5\x8f\xaf\xe8\x83\xbd" \
              b"\xe5\xaf\xbc\xe8\x87\xb4\xe6\x82\xa8\xe7\x9a\x84\xe8\xb4\xa6\xe5\x8f\xb7\xe6\x97\xa0\xe6\xb3\x95\xe6" \
              b"\xad\xa3\xe5\xb8\xb8\xe4\xbd\xbf\xe7\x94\xa8\xef\xbc\x8c\xe9\x81\x87\xe5\x88\xb0\xe6\xad\xa4\xe9\x97" \
              b"\xae\xe9\xa2\x98\xe8\xaf\xb7\xe8\x81\x94\xe7\xb3\xbb\xe3\x80\x82"

from PIL import Image
import io
import tesserocr
io.BytesIO(binary_data)
im = Image.open(io.BytesIO(binary_data))
print(tesserocr.image_to_text(im))
