import sys
import subprocess

def get_os_ver() -> str:
    platform_name = sys.platform.lower()
    if "win" in platform_name:
        return get_os_windows()
    elif "linux" in platform_name:
        return get_os_linux()
    elif "darwin" in platform_name:
        return get_os_macos()
    else:
        return "Unknown OS"

def get_os_windows() -> str:
    command = "Get-ComputerInfo | Select-Object -Property WindowsProductName, WindowsVersion, WindowsBuildLabEx"
    result = subprocess.run(
        ["powershell", "-Command", command],
        capture_output=True,
        text=True
    )
    lines = result.stdout.splitlines()  # result.stdout에서 splitlines 호출
    if lines:
        return lines[0].strip()  # 첫 번째 줄 반환
    return None  # 정보가 없을 경우 None 반환

def get_os_macos() -> str:
    command = "sw_vers -productVersion"
    result = subprocess.run(
        ["bash", "-c", command],
        capture_output=True,
        text=True
    )
    lines = result.stdout.splitlines()  # result.stdout에서 splitlines 호출
    if lines:
        return lines[0].strip()  # 첫 번째 줄 반환
    return None  # 정보가 없을 경우 None 반환

def get_os_linux() -> str:
    with open('/etc/os-release', 'r') as f:
        for line in f:
            if line.startswith('PRETTY_NAME='):  # PRETTY_NAME 라인을 찾음
                return line.split('=')[1].strip().strip('"')  # 값 반환
    return None  # 정보가 없을 경우 None 반환

