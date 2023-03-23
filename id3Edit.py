import requests
from mutagen.id3 import ID3, APIC, TIT2, TPE1


def editMusic(filepath, title, author, pic):
    audio = ID3(filepath)
    audio["APIC"] = APIC(
        encoding = 0,
        mime = "image/png",
        type = 3,
        data = pic.content,
    )
    audio["TIT2"] = TIT2(
        encoding = 3,
        text = title,
    )
    audio["TPE1"] = TPE1(
        encoding = 3,
        text = author,
    )
    audio.save()

if __name__ == "__main__":
    path = r"C:\Users\moiiii\Downloads/"
    filepath = path + "Choking on Flowers - Fox Academy.mp3"
    pic = open(path + "109951166055015459.jpg", "rb")
    editMusic(filepath, "titletest", "authortest", pic)