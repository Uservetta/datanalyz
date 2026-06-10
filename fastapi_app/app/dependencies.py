from app.init_dependencies import get_container

def get_app_config():
    return get_container()["app_config"]

def get_runtime_config_service():
    return get_container()["runtime_config_service"]