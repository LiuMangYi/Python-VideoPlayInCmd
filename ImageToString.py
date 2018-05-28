from PIL import Image


# 将指定图片使用字符画出来
class ImageToString:
    def __init__(self):
        self.chs = [' ', ',', '+', '1', 'n', 'D', '&', 'M']
        self.targetImg = "image.jpg"
        self.saveTxt = "image.txt"
        self.data = []

    # 像素-->字符
    def getch(self, p):
        for i in range(0, 8):
            if p < (i + 1) * 32:
                return self.chs[7 - i]

    # resize表示缩放的倍数
    def convert(self, resize=0.5):
        img = Image.open(self.targetImg)
        img = img.convert("L")      # 转为灰度（0-255）
        w, h = img.size             # 像素点
        h /= 2                      # 在进行字符的表示的时候上下有间隔
        w = int(w * resize)
        h = int(h * resize)         # 缩放
        img = img.resize((w, h), Image.ANTIALIAS)
        # img.save("tmp.jpg")
        pixs = img.load()           # 开始转换（这里是加载图片像素点的值）
        self.data = []              # 暂存转换之后的数据
        for i in range(0, h):
            data = ''               # 暂存转换之后每一行的数据
            for j in range(0, w):
                data += self.getch(pixs[j, i])
            self.data.append(data)

    # 显示方式
    def show(self, tp="console"):
        if tp == "console":
            for s in self.data:
                print(s)
        elif tp == "txt":
            with open(self.saveTxt, "w+") as f:
                for s in self.data:
                    f.write(s + "\n")
                f.close()


