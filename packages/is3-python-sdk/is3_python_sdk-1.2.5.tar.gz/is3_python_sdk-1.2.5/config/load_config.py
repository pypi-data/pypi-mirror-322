import os
import sys

import yaml


def load_config():
    # 设置当前工作目录为项目根目录
    if getattr(sys, 'frozen', False):  # 如果是打包后的 exe 文件
        current_dir = os.path.dirname(sys.executable)
    else:  # 如果是在开发过程中
        current_dir = os.path.dirname(os.path.abspath(__file__))

    os.chdir(current_dir)  # 更改当前工作目录为 current_dir

    # python代码测试时候
    exe_dir = current_dir

    # 构造 config.yaml 的完整路径
    config_path = os.path.join(exe_dir, 'config.yaml')

    # 读取 YAML 文件，指定编码为 utf-8
    with open(config_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)

    return config
