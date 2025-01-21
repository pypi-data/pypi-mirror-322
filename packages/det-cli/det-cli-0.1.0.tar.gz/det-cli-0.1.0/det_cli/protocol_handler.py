import os
import re
import sys


def handle_protocol(id, name):
    try:
        # 执行原有的 SSH 配置写入逻辑
        print(f"正在获取 id={id} 对应的 SSH 配置...")
        cmd = os.popen(f'det shell show-ssh-command {id}').read()

        # 提取 ProxyCommand
        proxy_cmd = re.search(r'ProxyCommand=(.+%h)', cmd)
        if proxy_cmd:
            proxy_cmd = proxy_cmd.group(1).replace('%h', id)
        else:
            print("未找到 ProxyCommand 配置。")
            return

        # 提取身份文件
        identity_file = re.search(r'-i ([^\s]+)', cmd)
        if identity_file:
            identity_file = identity_file.group(1)
        else:
            print("未找到身份文件配置。")
            return

        # 提取用户名和主机名
        user, host = re.search(r'([^\s@]+)@([^\s@]+)', cmd).groups()

        # 获取 SSH 配置文件路径
        config_file = os.path.expanduser('~/.ssh/config')

        # 确保配置文件存在
        if not os.path.exists(config_file):
            print(f"配置文件 {config_file} 不存在，正在创建...")
            open(config_file, 'w', encoding='utf-8').close()

        # 写入 SSH 配置
        with open(config_file, 'r+', encoding='utf-8') as f:
            content = f.read()
            if f'Host {name}' not in content:
                print(f"正在将配置写入 {config_file}...")
                f.seek(0, 2)
                f.write(f'\nHost {name}\nHostName {host}\nProxyCommand {proxy_cmd}\n'
                        f'StrictHostKeyChecking no\nIdentitiesOnly yes\n'
                        f'IdentityFile {identity_file}\nUser {user}\n')
                print(f"配置已成功添加到 {config_file}。")

                # 输出添加的主机信息
                print(f"\n添加的主机信息：")
                print(f"Host {name}")
                print(f"HostName {host}")
                print(f"ProxyCommand {proxy_cmd}")
                print(f"StrictHostKeyChecking no")
                print(f"IdentitiesOnly yes")
                print(f"IdentityFile {identity_file}")
                print(f"User {user}")

                # 提示用户如何通过 SSH 连接
                print(f"\n您可以通过以下命令使用 SSH 连接到该主机：")
                print(f"ssh {user}@{name}")
            else:
                print(f"配置已存在于 {config_file} 中，跳过添加。")
    except Exception as e:
        print(f"发生错误: {e}")

