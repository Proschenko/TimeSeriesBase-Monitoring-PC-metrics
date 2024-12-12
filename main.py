import psutil
from prometheus_client import start_http_server, Gauge
import os

# Определяем метрики с меткой 'core' для каждого ядра процессора
cpu_usage_percentage = Gauge('cpu_usage_percentage', 'Процент использования процессоров', ['core'])
memory_total_bytes = Gauge('memory_total_bytes', 'Общий объем оперативной памяти')
memory_used_bytes = Gauge('memory_used_bytes', 'Используемая оперативная память')
disk_total_bytes = Gauge('disk_total_bytes', 'Общий объем дисков')
disk_used_bytes = Gauge('disk_used_bytes', 'Используемое место на дисках')

# Функция для сбора метрик
def collect_metrics():
    # Получаем использование каждого ядра процессора
    cpu_percentages = psutil.cpu_percent(interval=1, percpu=True)
    for i, cpu_percent in enumerate(cpu_percentages):
        cpu_usage_percentage.labels(core=i).set(cpu_percent)  # Добавляем метку для каждого ядра

    # Получаем информацию о памяти
    memory = psutil.virtual_memory()
    memory_total_bytes.set(memory.total)
    memory_used_bytes.set(memory.used)

    # Получаем информацию о диске
    disk = psutil.disk_usage('/')
    disk_total_bytes.set(disk.total)
    disk_used_bytes.set(disk.used)

# Основная функция
def main():
    # Определяем переменные окружения для хоста и порта
    exporter_host = os.getenv('EXPORTER_HOST', 'localhost')
    exporter_port = os.getenv('EXPORTER_PORT', 8000)

    # Запуск HTTP-сервера для экспорта метрик
    start_http_server(int(exporter_port), addr=exporter_host)

    print(f"Exporter running on http://{exporter_host}:{exporter_port}")
    print(f"WEB:  http://localhost:9090")

    # Собираем метрики в цикле
    while True:
        collect_metrics()

if __name__ == '__main__':
    main()
