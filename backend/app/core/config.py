import requests

url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

payload={
  'scope': 'GIGACHAT_API_PERS'
}
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Accept': 'application/json',
  'RqUID': '9140fdd6-b19b-49f6-8d52-2e5214042957',
  'Authorization': 'Basic MDE5YzBmYTMtNjVkNi03NDQ1LTkxYWEtZjExMmQ0MTNiNTA5OjRiN2JmMDAwLWY1MDgtNGY3MC1hMzRkLWY2ZDBhMzhkYjA1Nw=='
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)