from __future__ import annotations

import os

import visual_chatgpt as vc

import bentoml
from bentoml.io import JSON

from bentoml_utils import BentoMLConversationBot
from bentoml_utils import create_gradio_blocks
from bentoml_utils import create_bentoml_service
from bentoml_utils import parse_load_dict

if not os.path.exists("checkpoints"):
    os.mkdir("checkpoints")

load_str = os.environ.get("VISUALCHATGPT_LOAD", "ImageCaptioning_cuda:0,Text2Image_cuda:0")
load_dict = parse_load_dict(load_str)

bot = BentoMLConversationBot(load_dict)
runners = [model.runner for model in bot.models.values()]
svc = bentoml.Service("bentoml-visual-chatgpt", runners=runners)

# Dummy api endpoint
@svc.api(input=JSON(), output=JSON())
def echo(d):
    return d

demo = create_gradio_blocks(bot)
svc.mount_asgi_app(demo.app, path="/ui")
