# Picamera2 の基本機能

このドキュメントでは、Picamera2 の基本的な機能である画像キャプチャ、動画録画、カメラプレビュー、およびカメラコントロールの 4 つを紹介します。
詳細については、[Picamera2 Official Manual (PDF)](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf) を参照してください。

## 1. 画像キャプチャ

Picamera2 には、画像をキャプチャするための複数の方法が用意されています。

| Function                          | Description                                  |
| --------------------------------- | -------------------------------------------- |
| `capture_file()`                  | 画像をキャプチャしてファイルに保存する       |
| `capture_array()`                 | 画像を NumPy 配列としてキャプチャする        |
| `capture_image()`                 | 画像を PIL Image としてキャプチャする        |
| `switch_mode_and_capture_file()`  | 設定を切り替え、画像をキャプチャして保存する |
| `switch_mode_and_capture_array()` | 設定を切り替え、キャプチャした画像を配列で返す |

### [camera_test.py:26](../camera_test.py) で使用している例

```python
# 画像を保存
picam2.capture_file("test.jpg")

# NumPy 配列としてキャプチャ
frame = picam2.capture_array()

# PIL Image としてキャプチャ
image = picam2.capture_image()

# 設定を切り替えてキャプチャ
picam2.switch_mode_and_capture_file(
    capture_config,
    "test.jpg"
)
```

**注:** `switch_mode_and_capture_file()` は、低解像度の動画設定で動作させながら、必要に応じて高解像度の静止画を撮影したい場合に便利です。

## 2. 動画録画

Picamera2 は、H.264 や MJPEG など、さまざまなエンコーダを使用した連続動画録画に対応しています。

### 例: [camera_test_video.py](../camera_test_video.py) に示す H.264 録画

### 主な関数

| Function            | Description                  |
| ------------------- | ---------------------------- |
| `start_recording()` | 動画録画を開始する            |
| `stop_recording()`  | 動画録画を停止する            |
| `start_encoder()`   | エンコーダを個別に開始する    |
| `stop_encoder()`    | エンコーダを個別に停止する    |

**注:** この例では H.264 elementary stream を保存します。FFmpeg を使用すると、再エンコードせずに MP4 に変換できます。

```bash
ffmpeg -i output.h264 -c:v copy output.mp4
```

## 3. カメラプレビュー

Picamera2 は、OpenCV を必要とせずにライブカメラプレビューを表示できます。

次のプレビューバックエンドに対応しています。

| Preview Backend | Description                   |
| --------------- | ----------------------------- |
| `Preview.QTGL`  | Qt ベースの OpenGL プレビュー |
| `Preview.QT`    | Qt ベースのソフトウェアプレビュー |
| `Preview.DRM`   | Direct Rendering プレビュー   |

### [camera_test.py:8](../camera_test.py) で使用している例

```python
from picamera2 import Picamera2, Preview

picam2 = Picamera2()

# プレビューウィンドウを開始
picam2.start_preview(Preview.QTGL)

# カメラキャプチャを開始
picam2.start()

input("Press Enter to stop...")

picam2.stop_preview()
picam2.stop()
picam2.close()
```

### 主な関数

| Function          | Description                  |
| ----------------- | ---------------------------- |
| `start_preview()` | カメラプレビューを開いて表示する |
| `stop_preview()`  | カメラプレビューを閉じる       |

**重要:** `picam2.start()` と `picam2.start_preview()` は、それぞれ異なる役割を持ちます。

- `start()` はカメラのキャプチャパイプラインを開始します。
- `start_preview()` はプレビューウィンドウにカメラ映像を表示します。

プレビューウィンドウを開かなくても、画像のキャプチャや動画の録画は可能です。

## 4. カメラコントロール

Picamera2 では、プログラムからカメラ設定を調整できます。

### 一般的なカメラコントロール

| Control        | Description                    |
| -------------- | ------------------------------ |
| `ExposureTime` | 露光時間を制御する              |
| `AnalogueGain` | センサーゲインを調整する         |
| `Brightness`   | 画像の明るさを調整する           |
| `Contrast`     | 画像のコントラストを調整する     |
| `Saturation`   | 色の彩度を調整する               |
| `Sharpness`    | 画像のシャープネスを調整する     |
| `AwbEnable`    | オートホワイトバランスの有効／無効を切り替える |
| `AeEnable`     | 自動露出の有効／無効を切り替える |
| `FrameRate`    | フレームレートを制御する         |
| `AfMode`       | オートフォーカスモードを設定する（対応カメラのみ） |

### 例: カメラ設定の調整

```python
picam2.set_controls({
    "ExposureTime": 10000,
    "AnalogueGain": 2.0,
    "Brightness": 0.1,
    "Contrast": 1.2,
    "Saturation": 1.0,
    "AwbEnable": True
})
```

### 例: Continuous Autofocus（IMX708）— [camera_test_picamCV.py](../camera_test_picamCV.py) に示す例

```python
picam2.set_controls({
    "AfMode": controls.AfModeEnum.Continuous
})
```

### 使用可能なカメラコントロールの確認

すべてのカメラが、すべてのコントロールに対応しているわけではありません。次のコードで使用可能なコントロールを確認できます。

```python
print(picam2.camera_controls)
```

**注:** カメラコントロールは、接続されているカメラモジュールの機能に応じて設定してください。

---

## References

- [Picamera2 Official Manual (PDF)](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf)
- [Raspberry Pi Camera Software Documentation](https://www.raspberrypi.com/documentation/accessories/camera-software.html)
