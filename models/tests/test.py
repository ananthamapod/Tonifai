from PIL import Image

with Image.open("favicon.ico") as img:
    data = img.tobytes()

    with open("test-1.txt", "wb") as test1:
        test1.write(data)


with open("favicon.ico", "rb") as img:
    data = img.read().encode('base64')

    with open("test-2.txt", "wb") as test2:
        test2.write(data)
