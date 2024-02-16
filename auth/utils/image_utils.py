import uuid


def save_image(image, key):
    file_path = f"media/{key}/{uuid.uuid4()}-{image.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(image.file.read())
    return file_path
