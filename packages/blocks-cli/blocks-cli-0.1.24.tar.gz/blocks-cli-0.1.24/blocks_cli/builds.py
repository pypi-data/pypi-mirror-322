import time

from blocks_cli.api import api_client
from blocks_cli.config.config import config

def poll_build_status(image_id: str, build_id: str):
    build_completed = False
    while not build_completed:
        res = api_client.get(f"{config.clients.orchestrator_url}/v1/images/{image_id}/builds/{build_id}")
        build_completed = res.json().get("is_completed")
        time.sleep(1)
