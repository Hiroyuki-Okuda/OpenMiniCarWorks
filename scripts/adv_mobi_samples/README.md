### 各スクリプトの概要
- main.py  
    全ての機能を組み込んだスクリプト．（LiDAR未実装）

- speed_observer.py  
    速度センサ用のスクリプト．
    速度センサのテストとmain.pyで利用する．

- color_observer.py  
    色検出用のスクリプト．
    カメラのテストとmain.pyで利用する．

- hsv_color_tester.py  
    HSV値確認用のスクリプト．

- lidar_test.py  
    LiDARテスト用のスクリプト．

- demo.py  
    走行テスト・デモ用のスクリプト．

### セットアップ
- python
    ```bash
    python3 -m pip install -r requirements.txt
    ```

- raspi gpio
    ```bash
    sudo systemctl enable pigpiod.service
    sudo systemctl start pigpiod
    ```

### トラブルシューティング
- ImportError: libcblas.so.3: cannot open shared object file: No such file or directory
    ```bash
    sudo apt-get install libatlas-base-dev
    ```

- ImportError: libjasper.so.1: cannot open shared object file: No such file or directory
    ```bash
    sudo apt-get install libjasper-dev
    ```

- ImportError: libQtGui.so.4: cannot open shared object file: No such file or directory
    ```bash
    sudo apt-get install qt4-dev-tools qt4-doc qt4-qtconfig libqt4-test
    ```
