from __future__ import annotations

import os

import visual_chatgpt as vc

import bentoml

from bentoml_utils import parse_load_dict
from service import svc


def build_runner_resource_configs(load_dict: dict[str, str]) -> list[str]:
    runner_cuda_tmpl = 'runners.{name}.resources."nvidia.com/gpu"[0]={gpu}'

    config_strs = []
    for class_name, resource in load_dict.items():
        if not resource.startswith("cuda"):
            continue

        runner_name = f"{class_name}_runner".lower()
        gpu = resource.split(":")[-1]
        config = runner_cuda_tmpl.format(name=runner_name, gpu=gpu)
        config_strs.append(config)

    return config_strs
        

if __name__ == '__main__':

    if not os.path.exists("checkpoints"):
        os.mkdir("checkpoints")

    load_str = os.environ.get("VISUALCHATGPT_LOAD", "ImageCaptioning_cuda:0,Text2Image_cuda:0")
    load_dict = parse_load_dict(load_str)

    runner_resource_configs = build_runner_resource_configs(load_dict)
    configs = runner_resource_configs
    bentoml_config_env_str = " ".join(configs)
    env_vars = {
        "BENTOML_CONFIG_OPTIONS": bentoml_config_env_str,
    }

    server = bentoml.HTTPServer(svc, api_workers=1)
    server.start(env=env_vars, blocking=True)
