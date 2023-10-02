import cv2
import torch
import numpy as np

# Load your custom YOLOv5 model with specific weights and device
weights_path = "D:\\yolo_object_detection\\weights\\best.pt"
device = 'cpu'  # Specify the device as 'cpu'
model = torch.hub.load('ultralytics/yolov5', 'custom', path=weights_path, force_reload=True, device=device)

# Confidence threshold
confidence_threshold = 0.5  # Set the confidence threshold to 0.5

# Initialize webcam
cap = cv2.VideoCapture(0)  # Use '0' for the default camera, or specify the camera index if you have multiple cameras

while True:
    ret, frame = cap.read()  # Read a frame from the webcam
    
    if not ret:
        break

    # Preprocess the frame (e.g., resizing, normalization) as needed for your custom model
    # You may need to adjust this based on your custom model's requirements
    
    # Perform inference on the frame using your custom model
    results = model(frame)

    # Extract bounding boxes, class labels, and confidence scores from the results
    bboxes = results.pred[0][:, :4].cpu().numpy()
    labels = results.pred[0][:, 5].cpu().numpy()
    confidences = results.pred[0][:, 4].cpu().numpy()

    # Filter detections based on confidence threshold
    filtered_indices = np.where(confidences >= confidence_threshold)[0]
    filtered_bboxes = bboxes[filtered_indices]
    filtered_labels = labels[filtered_indices]

    # Count the number of detections for your specific class or object of interest
    # Modify this code to count detections for your desired class
    class_of_interest = 0  # Replace with the class index of your object
    num_detections = np.sum(filtered_labels == class_of_interest)

    # Display the frame with bounding boxes and detection count
    for bbox in filtered_bboxes:
        x1, y1, x2, y2 = map(int, bbox)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Draw the alert text on the frame
    alert_text = f'Detections: {num_detections}'
    if num_detections >= 2:
        alert_text += " Alert!"
    cv2.putText(frame, alert_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Custom YOLOv5 Object Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

