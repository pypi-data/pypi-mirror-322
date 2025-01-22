from dotenv import load_dotenv, find_dotenv
import os
import subprocess
import shutil
import sys

load_dotenv(find_dotenv(),verbose=True,override=True)

def check_command_exists(command):
    """检查命令是否存在"""
    try:
        subprocess.run([command.split()[0], '--version'], capture_output=True)
        return True
    except FileNotFoundError:
        return False

def run_command(command):
    try:
        process = subprocess.Popen(command, shell=True)
        process.wait()
        if process.returncode != 0:
            raise Exception(f"命令执行失败: {command}")
    except Exception as e:
        print(f"执行命令时出错: {e}")
        sys.exit(1)

def main():
    # 检查是否安装了 uv
    if check_command_exists('uv'):
        # 清理之前的构建文件
        if os.path.exists("dist"):
            shutil.rmtree("dist")
        # 同步依赖
        run_command("uv sync")

        # 添加所有文件到 git
        run_command("git add .")

        # 检查是否有暂存的更改
        process = subprocess.Popen("git status --porcelain", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, _ = process.communicate()
        if stdout:
            # 提交到 git
            run_command("git commit -m 'publish'")
        else:
            print("没有暂存的更改，跳过 git commit 步骤")

        # 构建包
        run_command("uv build")

        # 上传到 PyPI
        run_command(f"uv publish --username {os.getenv('username')} --password {os.getenv('password')}")
    else:
        print("未检测到 uv，请先安装 uv")
        sys.exit(1)

if __name__ == "__main__":
    main()
