import subprocess
from tdtui.core.subprocess_runner import run_bash
from yaspin import yaspin
from yaspin.spinners import Spinners
import time
from tdtui.core.yaml_getter_setter import set_yaml_value
from tdtui.core.find_instances import define_root


def set_config_yaml(instance, ip_address="127.0.0.1"):
    instance_name = instance['name']
    external_port = instance['external_port']
    internal_port = instance['insternal_port']
    config_yaml_path = define_root(instance_name, "workspace/config/proc/regular/apiserver/config/config.yaml")
    set_yaml_value(path=config_yaml_path,key="addresses",value=f"{ip_address}:{external_port}")
    set_yaml_value(path=config_yaml_path,key="internal_addresses",value=f"{ip_address}:{internal_port}")

    yamlz set --path "$CONFIG_PATH" --key addresses --value "$PRIVATE_IP:$external_port" --type "list"
    yamlz set --path "$CONFIG_PATH" --key internal_addresses --value "127.0.0.1:$internal_port" --type "list"
    return


def start_instance(instance):
    instance_name = instance["name"]
    with yaspin().bold.blink.bouncingBall.on_cyan as sp:
        run_bash(f"tdserver start --instance {instance_name}")
    return None
    return


def stop_instance(instance):
    instance_name = instance["name"]
    with yaspin().bold.blink.bouncingBall.on_cyan as sp:
        run_bash(f"tdserver stop --instance {instance_name}")
    return None


def create_instance(instance):
    instance_name = instance["name"]
    with yaspin().bold.blink.bouncingBall.on_cyan as sp:
        run_bash(f"tdserver create --instance {instance_name}")
    return None


