import requests
import json
import textwrap
import urllib.request
import ssl

API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"

def main():
    # 創建不驗證證書的上下文
    context = ssl._create_unverified_context()
    
    response = requests.get(API_URL)
    data = response.json()

    print(data["title"], end="\n\n")
    print(textwrap.fill(data["extract"]))

if __name__ == "__main__":
    main()