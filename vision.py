import cv2
import pytesseract
from yolo import YOLO  

class AIParkingLot:
    def __init__(self, capacity):
        super().__init__(capacity)
        self.yolo = YOLO()  # Initialize YOLO for car detection

    def detect_car(self, frame):
       
        detections = self.yolo.detect_objects(frame)  # Detect cars in the frame
        for detection in detections:
            if detection['label'] == 'car':
                x, y, w, h = detection['box']  # Extract bounding box
                car_image = frame[y:y+h, x:x+w]  # Crop the car image
                return car_image
        return None

    def recognize_license_plate(self, car_image):
        """ Use OCR to read the license plate from the car image """
        gray_image = cv2.cvtColor(car_image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
        plate_text = pytesseract.image_to_string(gray_image)  # OCR to recognize plate
        return plate_text.strip()

    def update_parking_status(self, frame):
        """ Analyze the video frame to update parking status """
        car_image = self.detect_car(frame)
        if car_image:
            plate_number = self.recognize_license_plate(car_image)
            if plate_number:
                self.park_car(plate_number)
                print(f"Detected car with plate number: {plate_number}")
            else:
                print("Failed to recognize the plate number.")
        else:
            print("No car detected in the frame.")

    def monitor_parking_lot(self):
        """ Continuously monitor the parking lot using video feed """
        cap = cv2.VideoCapture(0)  # Connect to the video feed
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            self.update_parking_status(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
