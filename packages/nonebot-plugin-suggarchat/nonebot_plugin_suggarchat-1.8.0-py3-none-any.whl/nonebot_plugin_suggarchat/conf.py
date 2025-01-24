import os
from pathlib import Path
__KERNEL_VERSION__:str = "V1.8.0-Public-Dev"
# 获取当前工作目录  
current_directory:str = os.getcwd()  
config_dir = Path.cwd()/"config"
if not config_dir.exists():
    config_dir.mkdir()
group_memory = Path.cwd()/"group"
if not group_memory.exists():
    group_memory.mkdir()
private_memory = Path.cwd()/"private"
if not private_memory.exists():
    private_memory.mkdir()
main_config = config_dir/"config.json"
group_prompt = config_dir/"prompt_group.txt"
private_prompt = config_dir/"prompt_private.txt"
custom_models_dir = config_dir/"models"