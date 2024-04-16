import config, os
from webdav3.client import Client

client = None

def init_server():
    global client
    options = {
        'webdav_hostname': config.get_config("webdav_url"),
        'webdav_login':    config.get_config("webdav_username"),
        'webdav_password': config.get_config("webdav_password"),
    }
    client = Client(options)

    init_result = None
    try:
        _ = client.list('/')
        init_result = True
    except Exception as _:
        init_result = False
    
    return init_result

def check_target_sync_exist():
    if not client: return False
    target_sync_path = config.get_config("webdav_datapath")

    if not client.check(target_sync_path): return False

    # todo: check if is a dir
    path_info = client.info(target_sync_path)
    if "httpd/unix-directory" != path_info["content_type"]: return False

    return True

def upload(pdf_file_name: str):
    if not client: return

    local_sync_path = config.get_config("local_sync_path")
    local_sync_path = os.path.expanduser(local_sync_path)
    local_pdf_file_full_path = os.path.join(local_sync_path, pdf_file_name)
    
    annotation_file_full_path = local_pdf_file_full_path[:-4]+".pkl"
    if not os.path.isfile(annotation_file_full_path): return
    
    remote_path = config.get_config("webdav_datapath")
    remote_path = remote_path.rstrip("/")
    remote_path = remote_path + "/" + os.path.basename(annotation_file_full_path)
    client.upload_sync(remote_path=remote_path, local_path=annotation_file_full_path)

def download(pdf_file_name: str):
    if not client: return

    local_sync_path = config.get_config("local_sync_path")
    local_sync_path = os.path.expanduser(local_sync_path)
    local_pdf_file_full_path = os.path.join(local_sync_path, pdf_file_name)

    annotation_file_full_path = local_pdf_file_full_path[:-4]+".pkl"
    if os.path.isfile(annotation_file_full_path):
        os.remove(annotation_file_full_path)

    # todo: make sure remote_path is not a dir
    remote_path = config.get_config("webdav_datapath")
    remote_path = remote_path.rstrip("/")
    remote_path = remote_path + "/" + os.path.basename(annotation_file_full_path)
    if client.check(remote_path):
        client.download_sync(remote_path=remote_path, local_path=annotation_file_full_path)
