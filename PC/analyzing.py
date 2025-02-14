from ultralytics import YOLO
import numpy as np
import cv2
import queue
import threading


# Function for adding a color for every other object
def getColors(cls_num):
    base_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    color_index = cls_num % len(base_colors)
    increments = [(1, -2, 1), (-2, 1, -1), (1, -1, 2)]
    color = [
        base_colors[color_index][i]
        + increments[color_index][i] * (cls_num // len(base_colors)) % 256
        for i in range(3)
    ]
    return tuple(color)


class VideoCapture:

    def __init__(self, name):
        self.cap = cv2.VideoCapture(name)
        self.q = queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    # read frames as soon as they are available, keeping only most recent one
    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()  # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            self.q.put(frame)

    def read(self):
        return self.q.get()


def handle_connection(connection):
    # Defining the model variable/choosing the model
    model = YOLO("yolo11n.pt")
    # Defining the cap variable/setting up the video capture method/input
    cap = VideoCapture("[Video Input]")
    

    while True:

        # Reading the captures next frame
        frame = cap.read()
        # Detecting objects and visualizing the code
        results = model.track(frame, stream=True)

        # Placing a box around every detection
        for result in results:
            # Retrieving the class/category names of the objects
            classes_names = result.names

            for box in result.boxes:
                # Checking if confidence is greater than 40%
                if box.conf[0] > 0.4:
                    # Get coordinates of box
                    [x1, y1, x2, y2] = box.xyxy[0]
                    # Converting into integers
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                    # Get the class/category
                    cls = int(box.cls[0])

                    # Get the class/category names
                    class_name = classes_names[cls]

                    # Get the color
                    color = getColors(cls)

                    # Draw a rectangle with the color of the corresponding class
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    # 2 is the thickness of the box

                    # Adding the class name and confidence on the image
                    cv2.putText(
                        frame,
                        f"{classes_names[int(box.cls[0])]} {box.conf[0]:.2f}",
                        (x1, y1),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        color,
                        2,
                    )

                    # Show the image
                    cv2.imshow("frame", frame)

                    connection.send(bytes(class_name, "UTF-8"))

        # If user presses q, then quit the program
        if cv2.waitKey(1) == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
