# BentoML integration with TaskMatrix

This folder contains a quick and simple BentoML integration with TaskMatrix. We automatically convert TaskMatrix's models to BentoML's [runners](https://docs.bentoml.org/en/latest/concepts/runner.html). With the help of [yatai](https://github.com/bentoml/Yatai), we can distribute runners to kubernetes' nodes, hence making TaskMatrix distributed!.

## Quick start

Run your TaskMatrix with BentoML server locally in 3 simple steps

```bash
# setup environment
python -m venv venv && . venv/bin/activate && pip install -r requirements.txt
pip install git+https://github.com/facebookresearch/segment-anything.git
pip install  git+https://github.com/IDEA-Research/GroundingDINO.git

# set your openai api key
export OPENAI_API_KEY={your openai api key}

# start! VISUALCHATGPT_LOAD has the same format of visual_chatgpt.py's --load argument
VISUALCHATGPT_LOAD=Text2Box_cpu,Segmenting_cpu,ImageCaptioning_cuda:0,Text2Image_cuda:0 python start_server.py
```

Then go to <http://127.0.0.1:3000/ui> to visit TaskMatrix's interface.


## Build a bento and make a docker image

[Bento](https://docs.bentoml.org/en/latest/concepts/bento.html) is a standardized format that can be containerized to a docker image or deployed by yatai. Let's build a TaskMatrix.
 
```
# still in the virtual environment we make in last step
bentoml build
```

The output will be something like:

```
██████╗░███████╗███╗░░██╗████████╗░█████╗░███╗░░░███╗██╗░░░░░
██╔══██╗██╔════╝████╗░██║╚══██╔══╝██╔══██╗████╗░████║██║░░░░░
██████╦╝█████╗░░██╔██╗██║░░░██║░░░██║░░██║██╔████╔██║██║░░░░░
██╔══██╗██╔══╝░░██║╚████║░░░██║░░░██║░░██║██║╚██╔╝██║██║░░░░░
██████╦╝███████╗██║░╚███║░░░██║░░░╚█████╔╝██║░╚═╝░██║███████╗
╚═════╝░╚══════╝╚═╝░░╚══╝░░░╚═╝░░░░╚════╝░╚═╝░░░░░╚═╝╚══════╝

Successfully built Bento(tag="bentoml-visual-chatgpt:nlfdgsqgls4uqasc").

Possible next steps:

 * Containerize your Bento with `bentoml containerize`:
    $ bentoml containerize bentoml-visual-chatgpt:nlfdgsqgls4uqasc

 * Push to BentoCloud with `bentoml push`:
    $ bentoml push bentoml-visual-chatgpt:nlfdgsqgls4uqasc
```

We can follow the instruction above to build a docker image:

```
bentoml containerize bentoml-visual-chatgpt:nlfdgsqgls4uqasc
```

To utilize GPU in docker image, install [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-docker). Then run the docker image with:

```
docker run -it --rm -p 3000:3000 --gpus=all \
    --env OPENAI_API_KEY={your openai api key} \
    --env VISUALCHATGPT_LOAD="Text2Box_cpu,Segmenting_cuda:0,ImageCaptioning_cuda:0,Text2Image_cuda:0" \
    bentoml-visual-chatgpt:nvc7ibagj6qnkasc serve --api-workers=1
```

## BentoCloud section?
