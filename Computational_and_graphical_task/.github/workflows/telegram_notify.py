import os
import requests

# Получаем переменные из окружения (GitHub Secrets)
TOKEN = os.getenv("MY_BOT_TOKEN")
CHAT_ID = os.getenv("MY_BOT_CHAT_ID")

STATUS = os.getenv("PIPELINE_STATUS", "unknown")

# Формируем сообщение в зависимости от результата
if STATUS == "success":
    message = "✅ CI/CD pipeline завершился УСПЕШНО!"
elif STATUS == "failure":
    message = "❌ CI/CD pipeline завершился С ОШИБКОЙ!"
else:
    message = "⚙️ CI/CD pipeline завершился (статус неизвестен)."

# URL для Telegram API
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# Отправляем сообщение
try:
    response = requests.post(
        url,
        data={"chat_id": CHAT_ID, "text": message},
        timeout=10
    )
    if response.status_code != 200:
        print(f"Ошибка при отправке: {response.text}")
except requests.RequestException as e:
    print(f"Не удалось отправить сообщение: {e}")
