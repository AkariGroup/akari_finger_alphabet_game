
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
## 使い方
1. `python3 game_practice.py -m model/best_openvino_2022.1_6shave.blob -c json/best.json`を実行すると、`game_practice.py`が開始する
2. Akariの画面に表示されている指文字を真似して、指文字を練習する
3. 正しく指文字が表せたら、次の指文字が表示される
4. 「あいうえお」全ての練習が終わると、`game_main.py`が開始する
5. Akariの画面に表示される文字の母音を数え、最も多く含まれる母音を指文字で表す
## その他
このアプリケーションは愛知工業大学 情報科学部 知的制御研究室により作成されたものです