import requests
import os


def download_file(url, start_byte, end_byte, output_file):
    headers = {'Range': f'bytes={start_byte}-{end_byte}'}
    response = requests.get(url, headers=headers, stream=True)
    print(response.content)

    if response.status_code == 200:
        with open(output_file, 'ab') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"Downloaded bytes {start_byte}-{end_byte}")
    else:
        print("Failed to download file.")


def main():
    url = 'https://ds-file-1.cognix.tech/download/b8aac3ad-1389-4bb2-ba79-5ae3dd6b655e/9ce3209c-171f-484b-a2f5-15d0a994a4d7/'
    output_file = 'example.mp4'
    num_chunks = 5
    file_size = 17839845

    chunk_size = 3567969
    start_byte = 0
    end_byte = 0 + chunk_size

    for i in range(num_chunks):
        download_file(url, start_byte, end_byte, output_file)
        start_byte = end_byte + 1
        end_byte = end_byte + chunk_size


if __name__ == '__main__':
    main()
