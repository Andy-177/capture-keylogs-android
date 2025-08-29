import subprocess
import threading
import re

# 定义一个全局变量来存储最新的日志行
global_log = None

def logcat_thread(keyword, stop_event):
    global global_log  # 声明使用全局变量
    # 启动adb logcat命令，并实时获取输出
    process = subprocess.Popen(
        ['adb', 'logcat'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        encoding='utf-8'  # 指定编码为utf-8
    )

    try:
        print(f"正在实时获取包含关键词'{keyword}'的日志...")
        while not stop_event.is_set():
            line = process.stdout.readline()
            if line:
                # 使用正则表达式匹配关键词
                if re.search(keyword, line):
                    print(line.strip())
                    global_log = line.strip()  # 更新全局变量为最新的日志行
    finally:
        # 停止adb logcat进程
        process.kill()

def start():
    keyword = "ACC"
    stop_event = threading.Event()

    # 创建并启动线程
    thread = threading.Thread(target=logcat_thread, args=(keyword, stop_event))
    thread.start()

    try:
        # 主线程等待用户输入，例如输入'q'来停止
        input("按任意键停止...\n")
    finally:
        # 设置停止事件，通知线程停止
        stop_event.set()
        thread.join()
        print("日志捕获已停止。")
    return global_log
