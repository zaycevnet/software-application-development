import os
import requests

# Получаем переменные из окружения (GitHub Secrets)
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

STATUS = os.getenv("PIPELINE_STATUS", "unknown") # Получаем статус пайплайна из переменной окружения

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
    response = requests.post( #Выполняет HTTP-запрос типа POST на сгенерированный url. Это и есть сам факт отправки сообщения.
        url, #URL для отправки сообщения
        data={"chat_id": CHAT_ID, "text": message}, #Данные, которые отправляются в запросе. В данном случае это идентификатор чата и текст сообщения.
        timeout=10 #Максимальное время ожидания ответа от сервера (в секундах).
    )
    if response.status_code != 200: #Проверяет, успешен ли запрос (код 200 означает успех).
        print(f"Ошибка при отправке: {response.text}") #Если запрос не успешен, выводит текст ошибки.
except requests.RequestException as e: 
    print(f"Не удалось отправить сообщение: {e}") 