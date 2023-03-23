import re
import traceback
import requests
import id3Edit

PATH = r"D:\music\new/"
STOP = ["\\", "/", ":", "*", "?", "\"", "<", ">", "|"]


def getID(url):
    if "https://music.163.com/song" in url:
        c = re.search("id=(\d*)", url)
        return c.group(1)


class JBSOU:
    def __init__(self):
        self.URL = "https://www.jbsou.cn/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "x-requested-with": "XMLHttpRequest",
        }
        return

    def downloadMusic(self, musics):
        for music in musics:
            title = music["title"]
            picurl = re.search("(.*?)\?", music["pic"]).group(1)
            author = music["author"]
            url = music["url"]
            res = requests.get(url, stream=True)
            totalsize = int(res.headers["Content-Length"])
            filename = f"{title} - {author}.mp3"
            for i in STOP:
                filename = filename.replace(i, "")
            filepath = PATH+filename

            with open(filepath, "wb") as f:
                for cont in res.iter_content(10240):
                    progress = round(((f.tell() + len(cont)) / totalsize) * 100, 2)
                    print(f"\r Downloading...  {progress}%", end="", flush=True)
                    f.write(cont)
            print(" 正在修改歌曲信息...")
            pic = requests.get(picurl)
            id3Edit.editMusic(filepath, title, author, pic)

    def chooseMusic(self, music: list):
        print("搜索到以下音乐: ")
        for i in range(len(music)):
            print(f"{i}. [{music[i]['songid']}] {music[i]['title']} - {music[i]['author']} ")
        if len(music) == 1:
            while 1:
                inp = input("仅有一首，是否下载 (Y/n)").lower()
                if (inp == "y") | (inp == "yes") | (inp == ""):
                    self.downloadMusic(music)
                    return
                elif (inp == "n") | (inp == "no"):
                    return
                else:
                    print("仅接受y或n")
        else:
            while 1:
                try:
                    inp = input(">>>")
                    if inp == "exit":
                        return
                    num = int(inp)
                    print(f"正在下载: {music[num]}")
                    break
                except:
                    pass
            self.downloadMusic(music[num])

    def parseData(self, res):
        js = res.json()
        if js["code"] == 200:
            if len(js["data"]) > 0:
                self.chooseMusic(js["data"])

    def getMusicByID(self, ID):
        data = {
            "input": ID,
            "filter": "id",
            "type": "netease",
            "page": "1",
        }
        res = requests.post(self.URL, data=data, headers=self.headers)
        self.parseData(res)


def main():
    JBsou = JBSOU()
    while 1:
        try:
            print("音乐分享链接: ")
            url = input(">>>")
            if not url:
                continue
            ID = getID(url)
            JBsou.getMusicByID(ID)
            print("done.")
        except:
            traceback.print_exc()


if __name__ == "__main__":
    main()
