# monitoring_py
Как использовать:

1. Установите зависимости: pip install psutil requests
2. Настройте конфигурацию в начале скрипта (SLACK_WEBHOOK_URL, пороги срабатывания)
3. Добавьте скрипт в cron для регулярного выполнения: crontab -e
*/5 * * * * /path/to/your/script.py
4. Для работы Slack-уведомлений нужно создать Incoming Webhook в настройках Slack
