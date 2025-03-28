# monitoring_py
Как использовать:

Установите зависимости: pip install psutil requests
Настройте конфигурацию в начале скрипта (SLACK_WEBHOOK_URL, пороги срабатывания)
Добавьте скрипт в cron для регулярного выполнения: crontab -e
Copy
*/5 * * * * /path/to/your/script.py
Для работы Slack-уведомлений нужно создать Incoming Webhook в настройках Slack
