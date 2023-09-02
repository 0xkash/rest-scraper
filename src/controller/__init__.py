import os
from fastapi_router_controller import ControllerLoader

_dir = os.path.dirname(__file__)

ControllerLoader.load(_dir, __package__)