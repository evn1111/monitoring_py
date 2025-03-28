#!/usr/bin/env python3
import os
import psutil
import requests
import socket
from datetime import datetime

# Конфигурация
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
SERVICES_TO_CHECK = ["nginx", "postgresql", "redis-server"]
DISK_USAGE_THRESHOLD = 80  # %
CPU_LOAD_THRESHOLD = 90    # %
MEMORY_USAGE_THRESHOLD = 85  # %

def check_disk_usage():
    problems = []
    for partition in psutil.disk_partitions():
        usage = psutil.disk_usage(partition.mountpoint)
        if usage.percent > DISK_USAGE_THRESHOLD:
            problems.append(
                f"Диск {partition.device} ({partition.mountpoint}) заполнен на {usage.percent}%"
            )
    return problems

def check_cpu_load():
    problems = []
    load = psutil.cpu_percent(interval=1)
    if load > CPU_LOAD_THRESHOLD:
        problems.append(f"Нагрузка CPU: {load}%")
    return problems

def check_memory_usage():
    problems = []
    mem = psutil.virtual_memory()
    if mem.percent > MEMORY_USAGE_THRESHOLD:
        problems.append(f"Использование памяти: {mem.percent}%")
    return problems

def check_services():
    problems = []
    for service in SERVICES_TO_CHECK:
        try:
            # Для systemd-систем
            status = os.system(f"systemctl is-active --quiet {service}")
            if status != 0:
                problems.append(f"Сервис {service} не работает")
        except:
            problems.append(f"Ошибка при проверке сервиса {service}")
    return problems

def send_slack_alert(message):
    if not SLACK_WEBHOOK_URL:
        return
        
    payload = {
        "text": f":warning: *Alert from {socket.gethostname()}* :warning:\n{message}",
        "username": "DevOps Bot",
        "icon_emoji": ":robot_face:"
    }
    try:
        requests.post(SLACK_WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"Ошибка отправки в Slack: {e}")

def main():
    all_problems = []
    
    # Собираем все проверки
    all_problems.extend(check_disk_usage())
    all_problems.extend(check_cpu_load())
    all_problems.extend(check_memory_usage())
    all_problems.extend(check_services())
    
    if all_problems:
        alert_message = "\n".join(all_problems)
        alert_message += f"\n\n*Время проверки:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        print("Обнаружены проблемы:\n", alert_message)
        send_slack_alert(alert_message)
    else:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Все системы работают нормально")

if __name__ == "__main__":
    main()
