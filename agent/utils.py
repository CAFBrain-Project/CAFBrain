import os

def save_img(img, img_ext):
    if not os.path.exists("temp"):
        os.mkdir("temp")

    file_name = os.path.join("temp", str(len(os.listdir("temp"))) + "." + img_ext)
    img.save(file_name)

    return file_name