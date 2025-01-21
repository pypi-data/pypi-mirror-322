import asyncio
import json
import socket
import click
import websockets
import psutil
import platform
import logging
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

hostname = socket.gethostname()
stop_event = asyncio.Event()

def get_user_process_names():
    try:
        current_user = psutil.Process().username()
        os_type = platform.system()
        processes = psutil.process_iter(['pid', 'name', 'username', 'exe'])
        system_prefixes = {
            'Darwin': ['/System', '/usr/bin', '/usr/sbin'],
            'Linux': ['/sbin', '/usr/sbin', '/bin', '/usr/bin']
        }
        user_process_names = [
            proc.info['name'] for proc in processes
            if proc.info['username'] == current_user
            and proc.info['exe'] is not None
            and not any(proc.info['exe'].startswith(prefix) for prefix in system_prefixes.get(os_type, []))
        ]
        return user_process_names
    except psutil.AccessDenied:
        logging.warning("权限不足，无法获取进程信息")
        return []

async def init():
    url = os.getenv('WEBSOCKET_URL_INIT', "ws://114.236.93.153:8083/iov/websocket/dual?topic=test_devices")
    async with websockets.connect(url) as websocket:
        while True:
            await websocket.send(json.dumps({"hostname": hostname, "process_names": get_user_process_names()}))
            try:
                data = await asyncio.wait_for(websocket.recv(), timeout=2)

                data = json.loads(data)
                if data.get("ack") == "ack":
                    await websocket.close()
                    break
            except Exception as e:
                logging.error(f"还未收到ack: {e}")
                continue

        await connect()

async def connect():
    url = os.getenv('WEBSOCKET_URL_CONNECT', f"ws://114.236.93.153:8083/iov/websocket/dual?topic={hostname}")

    async with websockets.connect(url) as websocket:
        receive_data = await websocket.recv()
        await websocket.send(json.dumps({"ack":"ack"}))
        receive_data = json.loads(receive_data)
        process_name = receive_data.get("process_name")
        if not process_name:
            logging.error("无效的进程名称")
            return
        await collect_and_push_metrics(process_name, websocket)

# def get_total_cpu_usage(process_name):
#     total_cpu = 0.0
#     total_memory = 0.0
#     total_memory_percent = 0.0
#     num_cpus = psutil.cpu_count()
#     for proc in psutil.process_iter(['pid', 'name']):
#         try:
#             if proc.info['name'] == process_name:
#                 total_cpu += proc.cpu_percent(interval=0.1) / num_cpus
#                 total_memory += proc.memory_info().rss
#                 total_memory_percent += proc.memory_percent(memtype="rss")
#                 for child in proc.children(recursive=True):
#                     total_cpu += child.cpu_percent(interval=0.1) / num_cpus
#                     total_memory += child.memory_info().rss
#                     total_memory_percent += child.memory_percent(memtype="rss")
#         except (psutil.NoSuchProcess, psutil.AccessDenied):
#             continue
#
#     return round(total_cpu, 2), round(total_memory / 1024.0 / 1024.0, 2), round(total_memory_percent, 2)
async def collect_and_push_metrics(process_name, websocket):
    num_cpus = psutil.cpu_count()
    while not stop_event.is_set():
        try:
            total_cpu = 0.0
            total_memory = 0.0
            total_memory_percent = 0.0
            cpu_percent = psutil.cpu_percent(interval=0.1)
            # cpu_times_percent = psutil.cpu_times_percent(interval=0.5)._asdict()
            # cpu_percent_process, total_memory_process, total_memory_percent_process = get_total_cpu_usage(process_name)
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'] == process_name:
                        total_cpu += proc.cpu_percent(interval=0.1) / num_cpus
                        total_memory += proc.memory_info().rss
                        total_memory_percent += proc.memory_percent(memtype="rss")
                        for child in proc.children(recursive=True):
                            total_cpu += child.cpu_percent(interval=0.1) / num_cpus
                            total_memory += child.memory_info().rss
                            total_memory_percent += child.memory_percent(memtype="rss")
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    break
            load_avg = psutil.getloadavg()
            load_avg = [f"{load:.2f}" for load in load_avg]
            memory_info = psutil.virtual_memory()._asdict()
            initial_io = psutil.net_io_counters()
            initial_bytes_sent = initial_io.bytes_sent
            initial_bytes_recv = initial_io.bytes_recv
            await asyncio.sleep(1)
            final_io = psutil.net_io_counters()
            final_bytes_sent = final_io.bytes_sent
            final_bytes_recv = final_io.bytes_recv
            bytes_sent_per_sec = (final_bytes_sent - initial_bytes_sent) / 1024
            bytes_recv_per_sec = (final_bytes_recv - initial_bytes_recv) / 1024
            data = {
                "cpu_percent": cpu_percent,
                # "cpu_times_percent": cpu_times_percent,
                "load_avg": load_avg,
                "cpu_percent_process": round(total_cpu, 2),
                "total_memory": round(memory_info['used'] / (1024 ** 2), 2),
                "total_memory_process": round(total_memory / 1024.0 / 1024.0, 2),
                "total_memory_percent_process": round(total_memory_percent, 2),
                "memory_percent": memory_info['percent'],
                "bytes_sent_per_sec": round(bytes_sent_per_sec, 3),
                "bytes_recv_per_sec": round(bytes_recv_per_sec, 3),
            }

            await websocket.send(json.dumps(data))
        except Exception as e:
            logging.error(f"收集和推送指标失败: {e}")
            break

@click.command()
def main():
    asyncio.run(init())

@click.group()
def cli():
    pass

@cli.command(name='run')
def run_command():
    """Start running the application."""
    asyncio.run(run())

async def run():
    await init()

@cli.command(name='stop')
def stop():
    """Stop the application."""
    stop_event.set()

if __name__ == '__main__':
    cli()
