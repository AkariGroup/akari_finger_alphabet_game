#!/usr/bin/env python3
import game_main
import argparse
import cv2
from lib.akari_yolo_lib.oakd_yolo import OakdYolo
from akari_client import AkariClient


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
    i=0

    # AKARIのSDカード上に保存されている練習用画像のパス
    images = ["/jpg/handA.jpg","/jpg/handI.jpg","/jpg/handU.jpg","/jpg/handE.jpg","/jpg/handO.jpg"]

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
                # 練習用の指文字画像表示
                m5.set_display_image(images[i])
                display = 1

                
            if frame is not None:
                if detections:
                    for detection in detections:
                        
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
                        
                        # カウントが閾値を超え、かつ画像と一致していたら次の画像へ
                        if num_a > a_THRESHOLD and i == 0:
                            display = 0
                            i+=1
                        elif num_i > i_THRESHOLD and i == 1:
                            display = 0
                            i+=1
                        elif num_u > u_THRESHOLD and i == 2:
                            display = 0
                            i+=1
                        elif num_e > e_THRESHOLD and i == 3:
                            display = 0
                            i+=1
                        elif num_o > o_THRESHOLD and i == 4:
                            display = 0
                            end = True
                            oakd_yolo.close()
                            game_main.main()
                else:
                    # 指文字の認識カウントをリセット
                    num_a = 0
                    num_i = 0
                    num_u = 0
                    num_e = 0
                    num_o = 0
            
                oakd_yolo.display_frame("AKARI_PRACTICE", frame, detections)


            if cv2.waitKey(1) == ord("q"):
                end = True
                break
        oakd_yolo.close()

if __name__ == "__main__":
    main()
