import requests

FILE_NAME = 'large_video.mp4'

with open(FILE_NAME, 'rb') as file:
    headers = {'X-Filename': FILE_NAME}
    response = requests.post(
        'http://localhost:8080/upload', data=file, headers=headers, timeout=30)

print(response.text)
