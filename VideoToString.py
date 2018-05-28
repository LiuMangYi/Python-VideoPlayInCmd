import cv2
import os
from ImageToString import ImageToString
import threading
import pygame
import time


# 播放背景音乐（目前我没有学会播放视频里面的音频，所以 . . .）
def playMusic(f):
    pygame.mixer.init()
    pygame.mixer.music.load(f)
    pygame.mixer.music.play()


# 停止背景音乐
def stopMusic():
    pygame.mixer.music.stop()


class VideoToString:
    def __init__(self):
        self.frame = None  # 帧
        # 转换的视频
        self.pathname = "video/Alstroemeria Records - Bad Apple!!.mp4"
        # pathname = 'video/fripSide - floral summer.mp4'
        # 转换的音乐
        # file = 'music/fripSide - only my railgun.mp3'
        self.file = 'music/Alstroemeria Records - Bad Apple!!.mp3'
        # cmd窗口的大小
        self.cols = 100
        self.lines = 35

    # cmd下播放视频
    # 我们采用的是将帧存储在OS磁盘下
    # 然后读取再解析（虽然很导致很卡，但是能力有限，没招 . . .）
    def show(self):
        while True:
            try:
                its = ImageToString()  # 自己写的类，能把图片转换成字符然后显示在cmd上
                cv2.imencode('.jpg', self.frame)[1].tofile("image.jpg")  # 帧存入OS磁盘
                its.convert(0.3)  # 按一定比例缩小然后转换成对应的字符
                os.system("cls")  # 清空cmd
                its.show()  # 在cmd上显示，也可以指定存储在txt文件上
            except RuntimeError:
                pass

    # 主入口
    # waitTime表示播放速度（毫秒），video表示是否同步播放视频，music表示是否播放背景音乐
    def run(self, waitTime=40, video=True, music=True):
        print("把cmd的背景颜色改为白色，字体颜色改为黑色，然后字体尽量小效果更佳 . . .")
        os.system("pause")
        winSize = "mode con cols=" + str(self.cols) + " lines=" + str(self.lines)
        os.system(winSize)
        cap = cv2.VideoCapture(self.pathname)   # 加载视频
        first = True
        while cap.isOpened():
            ret, self.frame = cap.read()        # 一帧一帧读取
            if not ret:  # 读不到数据则关闭背景音乐退出
                if music:
                    stopMusic()
                break
            if first:   # 第一次进来则启动cmd播放视频的线程
                t1 = threading.Thread(target=self.show)
                t1.setDaemon(True)
                t1.start()
                if music:
                    playMusic(self.file)            # 播放音乐
                first = False
            if video:
                cv2.imshow('Video', self.frame)     # 同步播放视频
                k = cv2.waitKey(waitTime)  # 等待一个输入并且规定等待时间
                if k & 0xff == ord('q'):  # 输入的q，则退出程序
                    stopMusic()
                    break
            else:
                time.sleep(waitTime / 1000)
        cap.release()
        cv2.destroyAllWindows()
