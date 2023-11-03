# Import necessary libraries
import cv2
import numpy as np
import tflite_runtime.interpreter as tflite

# Define your model path and confidence threshold
model_path = "weights/detect.tflite"
confidence_threshold = 0.5

# Load the TFLite model
interpreter = tflite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]
float_input = (input_details[0]['dtype'] == np.float32)
input_mean = 127.5
input_std = 127.5

# Open a webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()

    if not ret:
        break

    # Resize and preprocess the frame
    image_resized = cv2.resize(frame, (width, height))
    input_data = np.expand_dims(image_resized, axis=0)

    if float_input:
        input_data = (np.float32(input_data) - input_mean) / input_std

    # Perform object detection
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    boxes = interpreter.get_tensor(output_details[1]['index'])[0]
    scores = interpreter.get_tensor(output_details[0]['index'])[0]

    # Initialize a count of detected objects
    object_count = 0

    # Annotate the frame with "car" detections
    for i in range(len(scores)):
        if scores[i] > confidence_threshold:
            ymin, xmin, ymax, xmax = boxes[i]
            label_text = "car"
            confidence = int(scores[i] * 100)
            cv2.rectangle(frame, (int(xmin * frame.shape[1]), int(ymin * frame.shape[0])),
              (int(xmax * frame.shape[1]), int(ymax * frame.shape[0])), (0, 255, 0), 2)

            cv2.putText(frame, f"{label_text}: {confidence}%", (int(xmin * frame.shape[1]), int(ymin * frame.shape[0]) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # Increment the object count
            object_count += 1

    # Display an alert if more than two objects are detected
    if object_count >= 2:
        cv2.putText(frame, "Alert! More than 2 objects detected!", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the frame
    cv2.imshow('Object Detection', frame)

    # Break the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
