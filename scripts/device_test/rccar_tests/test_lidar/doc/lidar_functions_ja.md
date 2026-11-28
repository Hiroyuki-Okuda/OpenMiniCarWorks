# RPLidar の基本関数

このドキュメントでは、センサーへの接続、状態の確認、測定値の取得に使用する Python の `rplidar` ライブラリの基本関数を紹介します。インストールとハードウェアのセットアップについては、[LiDAR セットアップガイド](README_ja.md)を参照してください。

## 1. 接続とデバイスの状態

| 関数 | 説明 |
| ---- | ---- |
| `RPLidar(port)` | シリアルポートを使用して LiDAR 接続を初期化 |
| `get_info()` | デバイス情報を取得 |
| `get_health()` | デバイスの状態を確認 |
| `disconnect()` | シリアル接続を閉じる |

### [RPlidarA1M8_test.py](../RPlidarA1M8_test.py) でのデバイス状態の確認

```python
print('Device info:', lidar.get_info())
print('Health:', lidar.get_health())
```

**注:** `/dev/ttyUSB0` は LiDAR に割り当てられたシリアルポートに置き換えてください。

## 2. 測定値とスキャンの取得

| 関数 | 説明 |
| ---- | ---- |
| `iter_measures()` | 個々の測定値を取得 |
| `iter_scans()` | 完全なスキャンを取得 |

`iter_measures()` は `(new_scan, quality, angle, distance)` のタプルを返します。`new_scan` フラグはスキャンの開始を示します。`iter_scans()` は測定値をスキャン単位にまとめ、それぞれのスキャンには `(quality, angle, distance)` のタプルが含まれます。角度の単位は度、距離の単位はミリメートルです。

### 例: 個々の測定値を取得

```python
for new_scan, quality, angle, distance in lidar.iter_measures():
    print(new_scan, quality, angle, distance)
```

### [RPlidarA1M8_test.py](../RPlidarA1M8_test.py) でのスキャン取得

```python
for i, scan in enumerate(lidar.iter_scans()):
    print(f'Scan {i}: {len(scan)} measurements')
    print(scan[:5])
    if i >= 9:
        break
```

近くの障害物を検出するスキャンの絞り込み例は [test_obstacle_detection.py](../test_obstacle_detection.py)、リアルタイムの極座標表示は [animate.py](../animate.py) を参照してください。

## 3. モーター制御と終了処理

| 関数 | 説明 |
| ---- | ---- |
| `start_motor()` | LiDAR のモーターを開始 |
| `stop_motor()` | LiDAR のモーターを停止 |
| `stop()` | スキャンを停止 |
| `disconnect()` | シリアル接続を閉じる |

### 例: 状態確認、スキャン、終了処理

[RPlidarA1M8_test.py](../RPlidarA1M8_test.py) は 10 スキャンを取得します。`Ctrl+C` で途中停止することもできます。

```python
from rplidar import RPLidar

lidar = RPLidar('/dev/ttyUSB0')

try:
    print('Device info:', lidar.get_info())
    print('Health:', lidar.get_health())

    for i, scan in enumerate(lidar.iter_scans()):
        print(f'Scan {i}: {len(scan)} measurements')
        print(scan[:5])
        if i >= 9:
            break
except KeyboardInterrupt:
    pass
finally:
    try:
        lidar.stop()
    finally:
        try:
            lidar.stop_motor()
        finally:
            lidar.disconnect()
```

モーターを明示的に開始する必要がある場合は `start_motor()` を使用します。スキャン後は、接続を切る前にスキャンとモーターを停止してください。

## 参考資料

- [RPLidar Python ライブラリとサンプル](https://github.com/Roboticia/RPLidar)
- [Raspberry Pi LiDAR セットアップとテスト](README_ja.md)
