# Distributed File Download System

### Contributors:
| Name | Student number |
| ---- | ------ |
| Raisul Islam | 2304795 |
| Mohammadreza Sadeghi | 2305005 |
| Ameen Maniparambath | 2307266 |
| Nazmul Mahmud | 2307263 |

# About the Project
## Abstract
The Distributed File Download System represents a cutting-edge solution for optimizing file retrieval processes in a distributed environment. Comprising four distinct components—Client App, Information Server, Message Broker, and File Server—the system aims to streamline file distribution while ensuring scalability and reliability. Leveraging RabbitMQ as the message broker, the system orchestrates seamless communication between servers, facilitating efficient event-driven interactions. Key features include the Information Server's role in storing file metadata and generating unique download tokens, and the File Server's distribution across multiple zones for optimal download speeds. This report provides a comprehensive analysis of the system's architecture, process flow, and implementation, highlighting its significance in modern file management.

## Introduction
In an era marked by exponential growth in digital content, efficient file distribution is paramount for enhancing productivity and user experience. Traditional centralized download systems often face challenges in handling large file volumes, leading to performance bottlenecks and user frustration. To address these issues, we introduce the Distributed File Download System—an innovative solution designed to revolutionize file retrieval processes through distributed architecture. This project aims to optimize file distribution by decentralizing the download process and leveraging distributed components to enhance speed, reliability, and scalability.

The system comprises four essential components, each playing a critical role in facilitating file retrieval: the Client App, Information Server, Message Broker, and File Server. The Client App serves as the user interface, initiating download requests and overseeing file handling operations. Meanwhile, the Information Server acts as a central repository, storing vital file metadata and generating unique download tokens for secure access. Leveraging RabbitMQ as the Message Broker, the system ensures efficient communication between servers, enabling event-driven interactions and real-time updates. Additionally, the File Server, strategically distributed across multiple zones, ensures optimal download speeds by serving files from the nearest location.


# Implemented Components

## System Architecture
<img src="https://github.com/p4l4s6/DS-File-Downloader/assets/50152321/354a8286-e730-4531-90fa-a8f4693e8666" alt="drawing" width="820"/>

## 1. Client App
The Client App is a crucial component of our Distributed File Download System, responsible for facilitating user interactions and managing file downloads efficiently. Leveraging advanced asynchronous programming techniques, such as aiohttp and asyncio, the Client App optimizes the download process by fetching files in smaller, manageable chunks. This approach not only enhances download speed but also improves system resource utilization, enabling concurrent downloads while minimizing memory overhead.

### Key Features:
<b>Chunked Download:</b> Utilizing aiohttp and asyncio libraries, the Client App downloads files in smaller, manageable chunks rather than fetching the entire file at once. This approach allows for efficient utilization of network resources and improved download speeds.

<b>Integrity Verification:</b> To ensure the integrity of downloaded files, the Client App employs SHA-2 hash algorithms for checksum verification. After downloading each chunk, the Client App computes its hash value and compares it against the expected hash value provided by the server. Any discrepancies in hash values indicate potential data corruption or tampering, prompting the Client App to take appropriate corrective actions.

<b>Resilient Download Mechanism:</b> In scenarios where a download attempt fails from one server, the Client App seamlessly switches to alternative servers to retrieve the remaining file chunks. This dynamic failover mechanism ensures uninterrupted download progress and enhances system reliability, especially in distributed environments with varying server conditions.

<b>Progress Tracking:</b> The Client App provides real-time feedback to users by tracking the progress of file downloads and displaying informative status updates. Users can monitor the download progress, including the number of chunks downloaded, remaining download time, and overall completion percentage, enhancing transparency and user experience.

### Implementation Details:

<b>aiohttp and asyncio Integration:</b> The Client App harnesses the asynchronous capabilities of aiohttp and asyncio to perform non-blocking I/O operations, enabling efficient handling of concurrent download requests without blocking the main execution thread.

<b>Chunked Download and Joining:</b> Upon receiving a download request, the Client App divides the file into smaller chunks and initiates asynchronous download tasks for each chunk. Once all chunks are downloaded, the Client App efficiently joins them to reconstruct the original file, ensuring data integrity and completeness.

<b>Error Handling and Retry Mechanism:</b> In the event of download failures or network interruptions, the Client App implements robust error handling mechanisms to retry failed download tasks and recover from transient errors. This proactive approach minimizes downtime and ensures continuous progress towards completing the file download process.

## 2. Information Server

The Information Server stands as a critical component within our Distributed File Download System, serving as the backbone for authentication, file management, and event triggering functionalities. Developed using the Python and FastAPI framework, the Information Server ensures seamless interaction between clients and the distributed system while maintaining robust security measures and efficient data management practices.

### Key Features:

<b>Authentication Mechanism:</b> The Information Server employs Token authentication to validate user access and ensure secure interactions with the system. Through the generation and verification of unique tokens, the server safeguards sensitive operations and data from unauthorized access, enhancing overall system security.

<b>File Management APIs:</b> Leveraging the FastAPI framework, the Information Server exposes comprehensive APIs for file management, including File List API and File Details API. These APIs enable clients to retrieve information about available files, their attributes, and other relevant metadata, facilitating informed decision-making during file selection and download processes.

<b>Database Integration:</b> Utilizing SQLite database technology, the Information Server efficiently stores and manages file-related data, including file paths, attributes, and authentication tokens. The lightweight and embeddable nature of SQLite ensures seamless integration with the server, enabling efficient data retrieval and manipulation while minimizing resource overhead.

<b>Event Triggering:</b> Upon receiving file download requests from clients, the Information Server triggers events to notify the Message Broker, facilitating seamless communication and event-driven interactions within the distributed system. This asynchronous event handling mechanism ensures timely processing of download requests and enables efficient coordination between server components.

<img src="https://github.com/p4l4s6/DS-File-Downloader/assets/50152321/1d6c0ed1-2e28-4a50-999b-92742857dc13" alt="drawing" width="820"/>

### Implementation Details:

<b>FastAPI Integration:</b> The Information Server leverages the FastAPI framework to develop robust and high-performance APIs for seamless interaction with clients. FastAPI's asynchronous capabilities enable efficient handling of concurrent requests and facilitate rapid development of RESTful endpoints for file management functionalities.

<b>Token Authentication:</b> To authenticate users and authorize access to system resources, the Information Server implements Token authentication mechanisms. Upon successful authentication, clients receive access tokens, which are subsequently used to authenticate subsequent requests and ensure secure interactions with the server.
SQLite Database Integration: The Information Server integrates SQLite database technology to store and manage file-related data efficiently. Leveraging SQL queries and transactions, the server retrieves file information, validates user access, and maintains authentication tokens, ensuring consistent and reliable data management across system operations.

<b>Event Triggering Mechanism:</b> Upon receiving file download requests from clients, the Information Server triggers events to notify the Message Broker, utilizing asynchronous event-driven programming paradigms. This event-driven architecture enables seamless communication and coordination between server components, ensuring timely processing of download requests and efficient resource utilization.

![image](https://github.com/p4l4s6/DS-File-Downloader/assets/50152321/da5a86a5-17da-4a6d-9459-3cb1a3881c6d)
![image](https://github.com/p4l4s6/DS-File-Downloader/assets/50152321/854bfd67-0684-4384-a1e5-de21b3c20ece)
![image](https://github.com/p4l4s6/DS-File-Downloader/assets/50152321/34d8377e-2f2a-49ff-9cb2-9a9b0b82d89d)
![image](https://github.com/p4l4s6/DS-File-Downloader/assets/50152321/44dc15ae-4085-4bbe-a85c-32881c9f17e7)
![image](https://github.com/p4l4s6/DS-File-Downloader/assets/50152321/373ec140-d3e3-4034-ac57-dd401f916fdd)


## 3. Message Broker

The Message Broker serves as a pivotal intermediary within our Distributed File Download System, facilitating seamless communication and event-driven interactions between components. Utilizing robust routing, channel, and subscription mechanisms, the Message Broker ensures efficient relay of events from the Information Server to File Servers, enabling timely processing of file download requests and data synchronization across distributed nodes.

The Message Broker serves as a central intermediary within the Distributed File Download System, receiving events from the Information Server and facilitating their seamless relay to File Servers. Utilizing predefined routing rules and subscription mechanisms, the Message Broker directs events to the appropriate File Servers based on factors such as server availability and geographic proximity. This ensures efficient distribution of event data, allowing File Servers to retrieve crucial information such as file details and download tokens. Through its robust infrastructure and real-time event processing capabilities, the Message Broker plays a pivotal role in orchestrating timely communication and coordination between system components, ultimately enabling smooth and reliable file download operations.


### RabbitMQ:


RabbitMQ is a robust and versatile message broker software that facilitates communication between distributed systems by enabling the exchange of messages across various applications and services. It functions by receiving, storing, and routing messages between producers (applications that send messages) and consumers (applications that receive messages), employing a variety of message queuing protocols such as AMQP (Advanced Message Queuing Protocol) and MQTT (Message Queuing Telemetry Transport). RabbitMQ's flexible routing mechanisms, including direct, topic-based, and fanout exchanges, allow for efficient and customizable message distribution based on specified criteria. Additionally, RabbitMQ provides features such as message persistence, delivery acknowledgments, and clustering capabilities, ensuring reliable and scalable message processing in diverse deployment scenarios. Overall, RabbitMQ serves as a crucial middleware component in distributed systems, facilitating seamless communication and integration between disparate applications and services.


## 4. File Server

The File Server serves as a critical component within our Distributed File Download System, responsible for efficiently delivering file downloads to clients based on provided download tokens and file UIDs. Developed using Python and FastAPI, the File Server leverages modern web frameworks to provide a robust and scalable platform for streaming file downloads, enabling seamless retrieval of files in chunks.

### Key Features:

<b>File Download API:</b> The File Server exposes a comprehensive File Download API, allowing clients to initiate download requests using download tokens and file UIDs. Leveraging FastAPI, the server provides a RESTful interface that supports streaming downloads, enabling files to be retrieved in manageable chunks based on specified start and end byte ranges.

<b>Support for Stream Download:</b> By supporting stream downloads, the File Server enables clients to retrieve files in chunks, optimizing network utilization and enhancing download performance. This approach allows for efficient utilization of bandwidth and reduces latency, particularly when downloading large files over network connections with limited bandwidth.

<img src="https://github.com/p4l4s6/DS-File-Downloader/assets/50152321/3fb991d6-34bf-4fee-9f77-c7cbeec6a74f" alt="drawing" width="480">


### Deployment:

<b>Dockerization:</b> The entire application, including the File Server, is containerized using Docker, ensuring portability and ease of deployment across diverse environments. Docker-compose is utilized to define and manage the application's multi-container architecture, simplifying the deployment process and ensuring consistency across deployment environments.

<b>Service Replication:</b> The Docker-compose configuration includes three services: Information Server, Message Broker, and Provider (File Server). To enhance fault tolerance and scalability, the Provider service (File Server) is configured with three replicas, allowing for horizontal scaling and distributed load balancing across multiple instances.

<b>Deployment Procedure:</b> Deploying the Distributed File Download System is streamlined using Docker-compose. By executing the command docker-compose up, the entire application stack, including the File Server and associated services, can be launched seamlessly, ensuring rapid deployment and consistent operation across different deployment environments.

![image](https://github.com/p4l4s6/DS-File-Downloader/assets/50152321/fc96a473-fc61-4cd6-8e40-c64bf8fc3828)
![image](https://github.com/p4l4s6/DS-File-Downloader/assets/50152321/caf88f7f-989e-4a02-9161-54b736d618a0)


## Process Flow Diagram

![image](https://github.com/p4l4s6/DS-File-Downloader/assets/50152321/0d96d7b6-ae00-40c8-9e8b-de6c87d04d2b)

1. The process starts with the client application where the client will input the id of a file which it wants to download it.
2. After receiving the file id it will trigger a GET request to the Information server.
    1. Information server will get the file information from the database 
    2. Information server will generate a unique download token and publish it to the message broker.   
    3. Information server will return a JSON response containing file information and that unique token.
3. Multiple file servers in multiple zones will consume the published event from the broker
    published by the Information server and save the unique token id into the database. 
4. Client App will launch multiple threads for getting the chunks of the file by using the JSON
    information received in 2.2.
5. The file server will cross check the token received from the client app against the saved token
   in the database. If the token is matched it will release that chunk of the file otherwise it will
   throw a 403 status code.
6. Once all the chunks of the files are collected from the file servers the client app will organize
    the chunks as per JSON information and join them and make a whole file.


## Built with:
- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [RabbitMQ](https://www.rabbitmq.com/)
- [SQLite](https://www.sqlite.org/)
- [Nginx](https://www.nginx.com/)
- [Docker](https://www.docker.com/)

### Libraries:
| Library | Version |
| ------- | ------- |
| annotated-types | 0.6.0 |
| anyio | 4.2.0 |
| click | 8.1.7 |
| colorama | 0.4.6 |
| fastapi | 0.109.2 |
| greenlet | 3.0.3 |
| h11 | 0.14.0 |
| httptools | 0.6.1 |
| idna | 3.6 |
| passlib | 1.7.4 |
| pydantic | 2.6.1 |
| pydantic_core | 2.16.2 |
| python-dotenv | 1.0.1 |
| PyYAML | 6.0.1 |
| sniffio | 1.3.0 |
| SQLAlchemy | 2.0.27 |
| sqlmodel | 0.0.14 |
| starlette | 0.36.3 |
| typing_extensions | 4.9.0 |
| uvicorn | 0.27.1 |
| watchfiles | 0.21.0 |
| websockets | 12.0 |
| pika~ | 1.3.2 |



## Getting Started

1. Activate the virtual environment
```
source venv/bin/activate
```

2. Install the requirements
```
pip install -r requirements.txt
```

3. Run the frontend code
```
python frontend.py
```


## Results of the tests

Testing the system with one server running and only one client:
![Screenshot_20](https://github.com/p4l4s6/DS-File-Downloader/assets/50152321/268075cc-784a-4fbd-a5d9-734fbf6e11ce)

Testing the system with two servers running and one client:
![Screenshot_21](https://github.com/p4l4s6/DS-File-Downloader/assets/50152321/1c899ba6-2189-45f9-8a4c-6a9ad35ea9a1)

Testing the system with two servers running and 5 clients:
![Screenshot_22](https://github.com/p4l4s6/DS-File-Downloader/assets/50152321/e6df2e4c-1449-42ff-ae81-7ac64d2bd63e)

Testing the system with two servers running while one of them fails in the middle of download:
![Screenshot_27](https://github.com/p4l4s6/DS-File-Downloader/assets/50152321/d81ab309-ffdb-4348-829c-c4a7a5884cdd)

### Conclusion:

1. Having more servers to download increases the download speed because the client can download more from the faster servers.
2. The system has scalability, so we don't see a considerable drop in the performance by increasing the payload/number of clients.
3. The system is reliable, so failing one or more servers in the middle of a download operation doesn't result in failing that operation.

## Acknowledgments

https://www.toptal.com/python/beginners-guide-to-concurrency-and-parallelism-in-python

https://www.rabbitmq.com/tutorials/tutorial-two-python

