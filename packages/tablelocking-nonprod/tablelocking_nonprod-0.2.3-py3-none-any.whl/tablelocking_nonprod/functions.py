# import requests

def lock_table(full_table_name: str, partition: str, base_url: str, headers: dict[str, str], workspace_id: int = 0, run_id: int = 0) -> bool:
    print(f"lock table: {full_table_name}")
    # data = {
    #     "table_name": full_table_name,
    #     "partition": partition,
    #     "workspace_id": workspace_id,
    #     "run_id": run_id
    # }
    # url = f"{base_url}/locked_target_tables/"
    # response = requests.post(url, json=data, headers=headers)
    # print(f"response.status_code: {response.status_code}")
    # print(f"response.text: {response.text}")

    # if response.status_code == 200:
    #     return True
    # return False


def check_table_lock(full_table_name: str, base_url: str, headers: dict[str, str]) -> bool:
    print(f"check_table_lock: {full_table_name}")
    # data = {
    #     "table_name": full_table_name
    # }
    # url = f"{base_url}/locked_target_tables/is_locked"
    # response = requests.post(url, json=data, headers=headers)
    # print(f"response: {response.text}")
    
    # if response.status_code == 200:
    #     return response.json().get('is_locked', False)
    # else:
    #     return False