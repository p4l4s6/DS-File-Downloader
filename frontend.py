import asyncio
import concurrent.futures
import random
import threading
import time

import aiofiles
import aiohttp
import requests
import hashlib
import os

from requests import JSONDecodeError

CHUNK_SIZE = 1 * 1024 * 1024  # 2 megabyte
AUTH_SERVER = "https://ds-auth.cognix.tech"


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


# def download_file(url, start_byte, end_byte, output_file):
#     headers = {'Range': f'bytes={start_byte}-{end_byte}'}
#     response = requests.get(url, headers=headers, stream=True)
#
#     if response.status_code == 200:
#         # with open(output_file, 'ab') as f:
#         #     for chunk in response.iter_content(chunk_size=1024):
#         #         if chunk:
#         #             f.write(chunk)
#         print(f"Downloaded bytes {start_byte}-{end_byte}")
#         return response
#     else:
#         print("Failed to download file.")
#         print(response.json())


def check_hash(file_name, original_hash):
    h = hashlib.sha256()
    b = bytearray(128 * 1024)
    mv = memoryview(b)
    with open(file_name, 'rb', buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])
    current_hash = h.hexdigest()
    print(current_hash)
    return current_hash == original_hash


def login():
    username = input("Enter your email:\n")
    password = input("Enter your password:\n")
    # username = 'admin@admin.com'
    # password = '1234'
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
    for item in response:
        print(f"{item['id']}:-> {item['name']}")
    return response


def get_file_info(token, file_id):
    headers = {'Authorization': f"Token {token}"}
    response = send_request(path=f"{AUTH_SERVER}/file/{file_id}/", data=None, headers=headers, method="GET")
    return response


async def perform_download(session, url, headers, output_path):
    is_success = False
    async with session.get(url, headers=headers) as response:
        if response.status == 200:
            async for data in response.content.iter_chunked(1024):
                async with aiofiles.open(output_path, "ba") as f:
                    await f.write(data)
        else:
            is_success = False
    return is_success


async def download_chunk(session, urls, start, end, output_path):
    """
    Downloads a specific byte range of the file from a server.
    """
    first_url = urls[0]
    print(f"Downloading chunk {start}-{end} from server {first_url}")
    # headers = {'Range': f'bytes={start}-{end}'}
    # status = perform_download()


import threading
import asyncio


async def download_manager(tasks):
    threads = []  # Store active threads
    max_threads = 3  # Maximum concurrent threads

    while tasks:
        # Launch new threads up to the maximum limit
        while len(threads) < max_threads and tasks:
            task = tasks.pop(0)
            loop = asyncio.new_event_loop()  # Create a new event loop for each thread
            thread = threading.Thread(target=task, args=(task, loop))
            threads.append(thread)
            thread.start()

        # Monitor thread completion and handle errors
        for i, (thread, loop) in enumerate(threads):
            if not thread.is_alive():
                threads.pop(i)  # Remove completed thread
                try:
                    loop.run_until_complete(task)  # Run any remaining coroutines
                    loop.close()  # Close the event loop
                except Exception as e:
                    print(f"Task failed: {task}\nException: {e}")
                    tasks.insert(0, task)  # Requeue failed task


def run_task(task, loop):
    """Runs the given async task in a new event loop."""
    asyncio.set_event_loop(loop)  # Set the loop for this thread
    loop.run_until_complete(task)


async def download(file_info, output_filename):
    """
    Downloads the file in parts using multiple threads.
    """
    file_uid = file_info['file_uid']
    file_hash = file_info['locations']
    download_token = file_info['token']
    locations = file_info['locations']
    file_size = int(file_info['file_size'])
    print(f"file size {file_size}")
    file_hash = file_info['file_hash']

    num_chunks = (file_size // CHUNK_SIZE) + 1
    print(f"number of chunks {num_chunks}")
    urls = []
    tasks = []
    for location in locations:
        urls.append(f"{location['server_ip']}/download/{download_token}/{file_uid}/")

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(keepalive_timeout=300)) as session:
        start_byte = 0
        end_byte = 0 + CHUNK_SIZE
        index = 0
        for i in range(num_chunks):
            if end_byte < file_size:
                if index > len(urls):
                    index = 0
                tasks.append(download_chunk(
                    session=session,
                    urls=urls,
                    start=start_byte,
                    end=end_byte,
                    output_path=f"{output_filename}.part.{i}"
                ))
                start_byte = end_byte + 1
                end_byte = end_byte + CHUNK_SIZE
                index += 1
        await download_manager(tasks)

    # Merge downloaded chunks into the final file
    with open(output_filename, 'wb') as f:
        for i in range(num_chunks):
            chunk_path = f'{output_filename}.part.{i}'
            with open(chunk_path, 'rb') as chunk_file:
                f.write(chunk_file.read())
            os.remove(chunk_path)  # Remove temporary chunks


async def main():
    token = login()
    files = get_file_list(token)
    selected_file = int(input('Enter file number you want to download:\n'))
    file_info = get_file_info(token, selected_file)
    file_uid = file_info['file_uid']
    file_hash = file_info['locations']
    download_token = file_info['token']
    locations = file_info['locations']
    file_size = file_info['file_size']
    file_hash = file_info['file_hash']
    start = time.time()
    await download(file_info, "test.mp4")
    end = time.time()
    print(end - start)

    # # username = input('Enter your username:\n')
    # # password = input('Enter your password:\n')
    # username = 'admin@admin.com'
    # password = '1234'
    # response = requests.post('https://ds-auth.cognix.tech/auth/login/',
    #                          json=)
    # auth_token = response.json()['token']
    # print(auth_token)
    # # We should get the file name from the user and fetch the appropriate file id from that
    # file_name = 'example.mp4'
    # file_id = 1
    # response = requests.get(f'https://ds-auth.cognix.tech/file/{file_id}/',
    #                         headers={'Authorization': f"Token {auth_token}"}).json()
    # print(response)
    # file_hash = response['file_hash']
    # print('file hash:', file_hash)
    # file_token = response['token']
    # file_uid = response['file_uid']
    # # url = 'server-ip/download/token/file_uid
    # server_ips = [x['server_ip'] for x in response['locations']]
    # url = f'{server_ips[0]}/download/{file_token}/{file_uid}/'
    # # file_size = int(response.json()['file_size'])
    # file_size = 17839845
    #
    # chunk_size = CHUNK_SIZE
    # chunks_length = int(file_size / chunk_size) + 1
    # start_byte = 0
    # end_byte = 0 + chunk_size
    # last_written_byte = -1
    # current_chunk_number = 0
    # # print(response['locations'][0])
    #
    # while current_chunk_number <= chunks_length:


# TODO
# Here we should have different threads downloading chunks

# chuck_response = download_file(url, start_byte, end_byte, file_name)
# if start_byte == last_written_byte + 1:
#     with open(file_name, 'ab') as f:
#         for chunk in response.iter_content(chunk_size=1024):
#             if chunk:
#                 f.write(chunk)
#     start_byte = end_byte + 1
#     end_byte = end_byte + chunk_size
# else:
#     with open(file_name, 'r+b') as f:
#         f.write(bytearray(start_byte - last_written_byte))
# print(check_hash(file_name, file_hash))


if __name__ == '__main__':
    asyncio.run(main())
