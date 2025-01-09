
# akari_finger_alphabet_game

## セットアップ方法
1. 指文字画像をSDカードへコピー  
   `finger_alphabet_images`に入っている指文字の各画像をAkari内のSDカードの`jpg/`にコピーする
2. ローカルにクローンする  
   `cd ~`  
   `git clone https://github.com/AkariGroup/akari_finger_alphabet_game.git`  
   `cd akari_finger_alphabet_game`  
3. 仮想環境の作成  
   `python3 -m venv venv`  
   `. venv/bin/activate`  
   `pip install -r requirements.txt`  
## 起動方法  
1. 仮想環境の有効化  
   `.venv/bin/activate`  
2. `python3 game_practice.py`を実行すると、`game_practice.py`が開始する  
   練習モードをスキップする場合は、`python3 game_main.py`を実行し、手順6へ  
3. Akariの画面に表示されている指文字を真似して、指文字を練習する  
4. 正しく指文字が表せたら、次の指文字が表示される  
5. 「あいうえお」全ての練習が終わると、`game_main.py`が開始する  
6. Akariの画面に表示される文字の母音を数え、最も多く含まれる母音を指文字で表す  
7. AKARI_MAINウィンドウを選択した状態でキーボードの`q`キーを押すと終了する  
## その他
このアプリケーションは愛知工業大学 情報科学部 知的制御研究室により作成されたものです