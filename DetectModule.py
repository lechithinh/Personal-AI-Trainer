import cv2
import mediapipe as mp
import math

class posture_detector():
    def __init__(self, mode=False,
                 mComplexity = 1,
                 smLandmarks=True,
                 enableSegmentation=False, 
                 smoothSegmentation=True,
                 detectionCon=0.5, 
                 trackCon=0.5):
        
        self.mode = mode
        self.mComplexity = mComplexity
        self.smLandmarks = smLandmarks
        self.smoothSegmentation = smoothSegmentation
        self.enableSegmentation = enableSegmentation
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        
        self.pose = self.mp_pose.Pose(self.mode, 
                                      self.mComplexity, 
                                      self.smLandmarks,
                                      self.enableSegmentation, 
                                      self.smoothSegmentation, 
                                      self.detectionCon,
                                      self.trackCon)

    def find_person(self, img, draw = True):
        """
        :param img: Image link
        :param draw: To check whether we need to draw or do not
        :return: A matrix of pixel - numpy array
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(img_rgb)
        
        if self.results.pose_landmarks and draw:
            self.mp_draw.draw_landmarks(img, 
                                        self.results.pose_landmarks, 
                                        self.mp_pose.POSE_CONNECTIONS)
        return img

    def find_landmarks(self, img, draw=True):
        """
        :param img: Image link
        :param draw: To check whether we need to draw or do not
        :return: A two-dimension array f landmark
        """
        self.landmark_list = []
        if self.results.pose_landmarks: #The length is 33 coordinates
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h) #Transfer cordinates to the same size as CV2
                self.landmark_list.append([id, cx, cy])
                if draw: 
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.landmark_list

    def find_angle(self, img, p1, p2, p3, draw=True):
        """
        Given any three points/co-ordinates, it gives us an angle(joint)
        :param img: image link
        :param p1: point 1
        :param p2: point 2
        :param p3: point 3
        :param draw: true equals to draw otherwise
        :return: angle
        """
        # Get the landmarks
        x1, y1 = self.landmark_list[p1][1:]
        x2, y2 = self.landmark_list[p2][1:]
        x3, y3 = self.landmark_list[p3][1:]
        
        # Calculate the Angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                                 math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360
        # Draw
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 5)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 5)
            cv2.circle(img, (x1, y1), 11, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 16, (255, 60, 0), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 16, (255, 60, 0), 2)
            cv2.circle(img, (x3, y3), 11, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 16, (255, 60, 0), 2)

            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 60),
                        cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1)
        return angle

def main():
    
        # image_line = "test.png"
        # image = cv2.imread(image_line)
        # detector = posture_detector()
        # img = detector.find_person(image)
        # cv2.imshow("image", img)
        # cv2.waitKey(0)

        
        cap = cv2.VideoCapture(0)
        detector = posture_detector()
        while True:
            success, img = cap.read()
            img = detector.find_person(img)
            cv2.imshow("Image", img)
            landmark_list = detector.find_landmarks(img, draw=False)
            print(len(landmark_list))
            if len(landmark_list) != 0:
                cv2.circle(
                    img, (landmark_list[14][1], landmark_list[14][2]), 15, (0, 0, 255), cv2.FILLED)
            key = cv2.waitKey(1)

            if key == ord('q'):
                break

if __name__ == "__main__":
    main()