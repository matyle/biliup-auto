import os
import subprocess
import schedule
import time
from concurrent.futures import ThreadPoolExecutor

uploaded_files = set()  # 用于存储已上传的文件路径


def upload_file(file_path):
    upload_command = f"biliup upload {file_path}"
    process = subprocess.Popen(
        upload_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    if process.returncode == 0:
        uploaded_files.add(file_path)
        os.remove(file_path)


def scan_and_upload():
    folder_path = "."  # 替换为您要扫描的文件夹路径
    with ThreadPoolExecutor(max_workers=5) as executor:  # 根据需要设置最大线程数
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith((".mp4", ".flv")):  # 支持扫描 mp4 和 flv 文件
                    file_path = os.path.join(root, file)
                    if file_path not in uploaded_files:
                        executor.submit(upload_file, file_path)


# def job():
#     scan_and_upload()


# 设定每天的特定时间运行脚本，如每天的23:59
# schedule.every().day.at("23:59").do(job)

while True:
    schedule.run_pending()

if __name__ == "__main__":
    scan_and_upload()
