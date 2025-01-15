# run_tests.py
import subprocess
import os

def run_java_tests():
    # 确保当前工作目录正确
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)

    # 运行 mvn 命令
    process = subprocess.Popen(
        ["mvn", "test", "-Dtest=CucumberTestRunner_login_test"],
        cwd=project_root,  # 显式设置工作目录
        stdout=subprocess.PIPE,  # 捕获标准输出
        stderr=subprocess.PIPE,  # 捕获错误输出
        text=True  # 将输出解码为字符串
    )
    stdout, stderr = process.communicate()  # 等待命令执行完成并获取输出

    if process.returncode == 0:
        print("Test success")
        print(stdout)
    else:
        print("Test failed")
        print(stderr)

if __name__ == '__main__':
    run_java_tests()


