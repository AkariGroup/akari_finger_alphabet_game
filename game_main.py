#!/usr/bin/env python3
import argparse
import cv2
import pyttsx3
import random
import pykakasi
from lib.akari_yolo_lib.oakd_yolo import OakdYolo
from akari_client import AkariClient
from akari_client.color import Colors
from akari_client.position import Positions

def main() -> None:
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m",
        "--model",
        help="Provide model name or model path for inference",
        default="yolov7tiny_coco_416x416",
        type=str,
    )
    parser.add_argument(
        "-c",
        "--config",
        help="Provide config path for inference",
        default="json/yolov7tiny_coco_416x416.json",
        type=str,
    )
    parser.add_argument(
        "-f",
        "--fps",
        help="Camera frame fps. This should be smaller than nn inference fps",
        default=10,
        type=int,
    )
    args = parser.parse_args()

    end = False
    previous_message = None  # 前回のメッセージを格納する変数
    engine = pyttsx3.init() # 音声合成エンジンの初期化
    engine.setProperty('voice', 'Japanese') # 日本語モード
    engine.setProperty('rate', 150) # 速度を150に設定

    kakasi = pykakasi.kakasi() # インスタンスの作成
    kakasi.setMode('H','a') # ひらがなをローマ字に
    kakasi.setMode('K','a') # かたかな
    kakasi.setMode('J','a') # 漢字
    conversion = kakasi.getConverter() #上記モードの適用

    display = 0

    # カウントの閾値　この回数以上認識すると各文字として判定
    a_THRESHOLD = 15
    i_THRESHOLD = 15
    u_THRESHOLD = 15
    e_THRESHOLD = 15
    o_THRESHOLD = 15

    # カウントのための変数
    num_a = 0
    num_i = 0
    num_u = 0
    num_e = 0
    num_o = 0

    # 問題文になる単語群
    words = ["クリスマス","こんにちは","ありがとう","山本貴史","桜","おにぎり","おぼろ月","江戸前","海岸","戦績","伝説の剣聖","洗礼","トウモロコシ","微笑み","誇り",
             "ふるさと","宇宙船","トヨタ自動車","風景画","不正アクセス","長期的視野","六波羅探題","亜細亜"]
    # 母音の数を格納するリスト
    numbers = {'あ':0,'い':0,'う':0,'え':0,'お':0}

    while not end:
        oakd_yolo = OakdYolo(args.config, args.model, args.fps)
        while True:
            frame = None
            detections = []
            try:
                frame, detections = oakd_yolo.get_frame()
            except BaseException:
                print("===================")
                print("get_frame() error! Reboot OAK-D.")
                print("If reboot occur frequently, Bandwidth may be too much.")
                print("Please lower FPS.")
                print("==================")
                break

            akari = AkariClient()
            m5 = akari.m5stack
            if display==0:
                word = random.choice(words) # 単語群からランダムに一個取得
                # 問題文としてAKARIの画面に表示
                m5.set_display_text(
                        text=word,
                        pos_x=Positions.CENTER,
                        pos_y=Positions.CENTER,
                        size=5,
                        text_color=Colors.BLACK,
                        back_color=Colors.WHITE,
                        refresh=True,
                )
                display = 1

            if frame is not None:
                if detections:
                    for detection in detections:
                        message = ""


                        roma = conversion.do(word) # ローマ字変換
                        # 各母音の数を数える
                        count_a = roma.count('a')
                        numbers['あ'] = count_a
                        count_i = roma.count('i')
                        numbers['い'] = count_i
                        count_u = roma.count('u')
                        numbers['う'] = count_u
                        count_e = roma.count('e')
                        numbers['え'] = count_e
                        count_o = roma.count('o')
                        numbers['お'] = count_o
                        maxis = max(numbers,key=numbers.get) # 最も多く含まれる母音

                        
                        # 認識したらカウントを増やす
                        if detection.label == 0:
                            num_a += 1
                        elif detection.label == 1:
                            num_i += 1
                        elif detection.label == 2:
                            num_u += 1
                        elif detection.label == 3:
                            num_e += 1
                        elif detection.label == 4:
                            num_o += 1
                        
                        # カウントが閾値を超えたら、ラベルIDに応じてメッセージを設定
                        if num_a > a_THRESHOLD:
                            message = "あ"
                        elif num_i > i_THRESHOLD:
                            message = "い"
                        elif num_u > u_THRESHOLD:
                            message = "う"
                        elif num_e > e_THRESHOLD:
                            message = "え"
                        elif num_o > o_THRESHOLD:
                            message = "お"
                       
                        # メッセージが前回と異なる場合のみ表示・読み上げ
                        if message and message != previous_message:

                            if message == maxis:
                                judge = "せいかい"
                                engine.say(judge+",                A")
                                engine.runAndWait()
                                display = 0
                            else:
                                judge = "ざんねん"
                                engine.say(judge+",                A")
                                engine.runAndWait()
                                display = 0


                            # # デバック用
                            # print(word)
                            # print("max="+maxis+"myhand="+message)
                            # print(numbers)

                            previous_message = message  # 現在のメッセージを前回のメッセージとして更新
                else:
                    # 指が認識されていない場合、previous_messageを初期化
                    # 指文字の認識カウントをリセット
                    previous_message = None
                    num_a = 0
                    num_i = 0
                    num_u = 0
                    num_e = 0
                    num_o = 0
            
                oakd_yolo.display_frame("nn", frame, detections)

            

            if cv2.waitKey(1) == ord("q"):
                end = True
                break
        oakd_yolo.close()

if __name__ == "__main__":
    main()
