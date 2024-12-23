
# akari_finger_alphabet_game

## セットアップ方法
1. ローカルにクローンする
   `cd ~`
   `git clone https://github.com/AkariGroup/akari_finger_alphabet_game.git`
   `cd akari_finger_alphabet_game`
2. 仮想環境の作成
   `python3 -m venv venv`
   `. venv/bin/activate`
   `pip install -r requirements.txt`
## 起動方法
1. 仮想環境の有効化
   `.venv/bin/activate`
2. 物体認識を実行する
   `python3 game_practice.py -m model/best_openvino_2022.1_6shave.blob -c json/best.json`
3. 物体認識を終了する
   AKARI_MAINウィンドウを選択した状態でキーボードの`q`キーを押す

## その他
このアプリケーションは愛知工業大学 情報科学部 知的制御研究室により作成されたものです