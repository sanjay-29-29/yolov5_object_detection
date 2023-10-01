# YOLOv5 Object Detection on Windows

This repository contains a Python script for performing object detection using the YOLOv5 model on Windows. It captures video frames from a webcam and overlays bounding boxes on detected objects, counting the number of detections for a specific class and displaying an alert message if a threshold is met.

## Prerequisites

Before running the code, ensure you have the following dependencies installed on your Windows machine:

- Python 3.x
- OpenCV (`opencv-python`)
- PyTorch (`torch`)
- NumPy (`numpy`)

## Installation

1. Clone or download this repository to your local machine.
```
git clone https://github.com/PattasuBalu/yolo_object_detection.git
```
2. Navigate to the cloned repository folder:
```
cd yolo_object_detection
```

3. Install the required packages by running:
```
pip install -r requirements.txt
```

4. Open the Python script `alerting_and_count.py` and make the following adjustments:

   - Update the `weights_path` variable to point to the location of your custom YOLOv5 model weights.
   - Ensure your webcam is accessible via camera index `0`, or change the index if needed.

5. Save the script and run it using:
```
python alerting_and_count.py
```
