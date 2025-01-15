# run_tests.py
import subprocess
import os

def run_java_tests():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    

    process = subprocess.Popen(["mvn", "test", "-Dtest=CucumberTestRunner_login_test"], shell=True)
    stdout, stderr = process.communicate()
    
    if process.returncode == 0:
        print("test success")
        print(stdout)
    else:
        print("test fail")
        print(stderr)





