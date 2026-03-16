from gigachat import GigaChat

giga = GigaChat(
   credentials="MDE5YzBmYTMtNjVkNi03NDQ1LTkxYWEtZjExMmQ0MTNiNTA5OjRiN2JmMDAwLWY1MDgtNGY3MC1hMzRkLWY2ZDBhMzhkYjA1Nw==",
   model="GigaChat-Pro"
)

response = giga.chat("Привет! Как дела?")

print(response.choices[0].message.content)