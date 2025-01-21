import subprocess
import platform
import sys
import urllib.parse  # 修改导入方式
from det_cli.protocol_handler import handle_protocol
# 全局协议名称变量
PROTOCOL_NAME = "det-cli"

def register_protocol():
    if platform.system() != 'Windows':
        print("This script currently only supports Windows.")
        return

    python_path = sys.executable  # 使用当前环境的 Python 解释器
    script_path = __file__  # 获取当前脚本路径

    # 注册协议到 Windows 注册表
    reg_path = rf"HKEY_CLASSES_ROOT\{PROTOCOL_NAME}"

    reg_command = f"reg add {reg_path} /ve /t REG_SZ /d \"URL:{PROTOCOL_NAME} Protocol\" /f"
    reg_protocol_command = f"reg add {reg_path} /v \"URL Protocol\" /t REG_SZ /f"
    reg_command_exec = f'reg add {reg_path}\\shell\\open\\command /ve /t REG_SZ /d "\"{python_path}\" \"{script_path}\" \"%1\"" /f'

    try:
        # 检查协议是否已注册
        check_reg = subprocess.run(
            f'reg query {reg_path}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if check_reg.returncode == 0:
            print(f"协议 '{PROTOCOL_NAME}://' 已经注册，是否更新(y/n): ", end="")
            user_input = input().strip().lower()

            if user_input == 'y':
                pass
            else:
                print("协议未更新。")
                return

        # 注册协议
        print(f"Run: {reg_command}")
        subprocess.run(reg_command, shell=True, check=True)
        print(f"Run: {reg_protocol_command}")
        subprocess.run(reg_protocol_command, shell=True, check=True)
        print(f"Run: {reg_command_exec}")
        subprocess.run(reg_command_exec, shell=True, check=True)
        print(f"协议 '{PROTOCOL_NAME}://' 注册成功.")

    except subprocess.CalledProcessError as e:
        print(f"注册协议时发生错误: {e}")
    except Exception as e:
        print(f"未预料的错误: {e}")
def handle_custom_protocol(url):
    # 解析 URL 参数
    print(f"请求路径{url}")
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    # 提取参数 id 和 name
    id = query_params.get('id', [None])[0]
    name = query_params.get('name', [None])[0]

    if id and name:
        print(f"获取配置 id={id} and name={name}")
        handle_protocol(id, name)
    else:
        print("缺少 'id' 或 'name' 参数.")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        url = sys.argv[1]
        print(sys.argv)
        handle_custom_protocol(url)
    input("按任意键退出...")