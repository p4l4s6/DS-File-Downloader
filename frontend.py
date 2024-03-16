import ast
import asyncio
import os
import random
import time
from json import JSONDecodeError

import aiofiles
import aiohttp
import requests

CHUNK_SIZE = 3 * 1024 * 1024  # 2 megabyte
AUTH_SERVER = "https://ds-auth.cognix.tech"
download_report = {}


def send_request(path, data, headers, method):
    if method == "GET":
        response = requests.get(path, headers=headers)
    else:
        response = requests.post(path, json=data, headers=headers)
    if response.status_code == 200:
        try:
            data = response.json()
            return data
        except JSONDecodeError as e:
            print(f"Cannot parse JSON from the response {e}")
    else:
        print("Unable to send network request")


def login():
    # username = input("Enter your email:\n")
    # password = input("Enter your password:\n")
    username = 'admin@admin.com'
    password = '1234'
    payload = {'email': username, 'password': password}
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = send_request(path=f"{AUTH_SERVER}/auth/login/", data=payload, headers=headers, method="POST")
    if response is not None:
        return response['token']
    return None


def get_file_list(token):
    headers = {'Authorization': f"Token {token}"}
    response = send_request(f"{AUTH_SERVER}/file/", data=None, headers=headers, method="GET")
    print("==============File List============")
    for item in response:
        print(f"{item['id']}:-> {item['name']}")
    print("===================================")
    return response


def get_file_info(token, file_id):
    headers = {'Authorization': f"Token {token}"}
    response = send_request(path=f"{AUTH_SERVER}/file/{file_id}/", data=None, headers=headers, method="GET")
    return response


async def generate_report(server_ip, size):
    if server_ip in download_report.keys():
        download_report[server_ip] = download_report[server_ip] + size
    else:
        download_report[server_ip] = size


async def download(session, chunk, server, file_info):
    """Downloads a chunk from a server."""
    # print(f"Downloading chunk {chunk} from server {server}...")
    # await asyncio.sleep(10)  # Simulate download time
    # if chunk == random.randint(0, 10) and server == "server1":  # Simulate occasional failures
    #     raise Exception("Download failed for chunk {}".format(chunk))
    # print(f"Chunk {chunk} downloaded from server {server['id']}!")
    try:
        print(f"Downloading chunk {chunk} from server {server['id']}...")
        file_uid = file_info['file_uid']
        download_token = file_info['token']
        output_path = f"{file_uid}.part.{chunk.get('chunk_no')}"
        headers = chunk['data']
        async with session.get(f"{server['server_ip']}/download/{download_token}/{file_uid}/",
                               headers=headers) as response:
            if response.status == 200:
                async for data in response.content.iter_chunked(1024):
                    async with aiofiles.open(output_path, "ba") as f:
                        await f.write(data)
                await generate_report(server['id'], chunk['total_byte'])
    except Exception as e:
        chunk['server'] = server
        raise Exception(f"{chunk}")


async def download_manager(file_info, session, chunks):
    """Manages download tasks across multiple servers."""

    active_tasks = set()
    completed_chunks = set()
    servers = file_info['locations']
    error_servers = []

    while chunks or active_tasks:
        while chunks and len(active_tasks) < len(servers):
            chunk = chunks.pop(0)
            server = servers[len(active_tasks)]  # Assign server based on task count
            for item in servers:
                if item['id'] not in error_servers:
                    server = item
            task = asyncio.create_task(download(session, chunk, server, file_info))
            active_tasks.add(task)

        done, pending = await asyncio.wait(active_tasks, return_when=asyncio.FIRST_COMPLETED)

        for task in done:
            try:
                result = await task  # Get the result (None for successful completion)
                completed_chunks.add(result)  # Add completed chunk to set
            except Exception as e:
                chunk = ast.literal_eval(str(e))
                server = chunk.pop('server')
                print("#########################################")
                print(f"Task failed: {chunk} from {server['id']}")
                print("#########################################")
                server_id = server['id']
                if server_id not in error_servers:
                    error_servers.append(server_id)
                print("Assigning task to another server.....")
                chunks.append(chunk)
            active_tasks.remove(task)

    print("All chunks downloaded!")


async def process_download(file_info):
    file_uid = file_info['file_uid']
    # file_hash = file_info['locations']
    # download_token = file_info['token']
    # locations = file_info['locations']
    file_size = int(file_info['file_size'])
    # # print(f"file info {file_info}")
    # file_hash = file_info['file_hash']
    chunks = []
    num_chunks = int((file_size / CHUNK_SIZE)) + 1
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(keepalive_timeout=300)) as session:
        start_byte = 0
        end_byte = 0 + CHUNK_SIZE
        for i in range(num_chunks):
            if end_byte > file_size:
                end_byte = file_size
            chunks.append({
                'chunk_no': i,
                'total_byte': end_byte - start_byte,
                'data': {
                    'Range': f'bytes={start_byte}-{end_byte}'
                }
            })
            start_byte = end_byte + 1
            end_byte = end_byte + CHUNK_SIZE
        start = time.time()
        await download_manager(file_info, session, chunks)
        end = time.time()
    # Merge downloaded chunks into the final file
    with open(file_info['name'], 'wb') as f:
        for i in range(num_chunks):
            chunk_path = f'{file_uid}.part.{i}'
            with open(chunk_path, 'rb') as chunk_file:
                f.write(chunk_file.read())
            os.remove(chunk_path)  # Remove temporary chunks

    print("==============Download Report============")
    print(f"Total Time taken: {end - start}")
    print("--------server percentage----------------")
    for key in download_report.keys():
        print(f"{key}: {download_report[key]} ---> {round((download_report[key] / file_size) * 100, 2)}%")


async def main():
    token = login()
    files = get_file_list(token)
    selected_file = int(input('Enter file number you want to download:\n'))
    file_info = get_file_info(token, 1)
    await process_download(file_info)


if __name__ == '__main__':
    asyncio.run(main())
