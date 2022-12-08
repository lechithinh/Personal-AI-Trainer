import cv2
import numpy as np
import time

import DetectModule as pm


class utilities():
    def __init__(self) -> None:
        pass
    def illustrate_exercise(self, example, exercise):
        """_summary_
            Show instructions
        Args:
            example (_string_): Image path
            exercise (_string_): Exercise name
        """
        seconds = 5 
        img = cv2.imread(example)
        img = cv2.resize(img, (980, 550))
        cv2.imshow("Exercise Illustration", img)
        cv2.waitKey(1)
        
        while seconds > 0:
            img = cv2.imread(example)
            img = cv2.resize(img, (980, 550))
            time.sleep(1)
            cv2.putText(img, exercise + " in: " + str(int(seconds)), (350, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255),5)
            cv2.imshow("Exercise Illustration", img)
            seconds -= 1 
            cv2.waitKey(1)
        cv2.destroyAllWindows()

    def repitition_counter(self, per, count, direction):
        if (per == 100 and direction == 0):
            count += 0.5
            direction = 1
        if (per == 0 and direction == 1):
            count += 0.5
            direction = 0
        return {"count": count, "direction":  direction}

    def display_rep_count(self, img, count, total_reps):
        cv2.rectangle(img, (0, 0), (240, 150), (255, 255, 255), cv2.FILLED)
        cv2.putText(img, str(int(count)) + "/" + str(total_reps), (20, 110), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 10)

    def get_performance_bar_color(self, per):
        color = (0, 205, 205)
        if 0 < per <= 30:
            color = (51, 51, 255)
        if 30 < per <= 60:
            color = (0, 165, 255)
        if 60 <= per <= 100:
            color = (0, 255, 255)
        return color

    def draw_performance_bar(self, img, per, bar, color, count):
        cv2.rectangle(img, (1100, 100), (1175, 550), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 550), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)


class simulate_exercise():
    def __init__(self, difficulty_level=1, reps=2, calories_burned=0):
        self.reps = reps
        self.difficulty_level = difficulty_level
        self.calories_burned = calories_burned

    def skip(self):
       
        utilities().illustrate_exercise("Images/skip.jpg", "Skip")
       
        #webcam setup
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) 
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        #activate posture module
        detector = pm.posture_detector()

        #parameter setup
        count = 0
        direction = 0 
        start = time.process_time()
        total_reps = self.reps * self.difficulty_level * 3

        while count < total_reps:
            success, img = cap.read()
            img = detector.find_person(img, False)
            landmark_list = detector.find_landmarks(img, False)

            if len(landmark_list) != 0:
                
                left_arm_angle = detector.find_angle(img, 11, 13, 15)
                right_arm_angle = detector.find_angle(img, 12, 14, 16)

                left_leg_angle = detector.find_angle(img, 24, 26, 28)
                right_leg_angle = detector.find_angle(img, 23, 25, 27)

                #from angle -> per -> color -> draw
                per = np.interp(left_arm_angle, (130, 145), (0, 100))
                bar = np.interp(left_arm_angle, (130, 145), (650, 100))

                color = utilities().get_performance_bar_color(per)
               
                if per == 100 or per == 0:
                    color = (0, 255, 0)
                    rep = utilities().repitition_counter(per, count, direction)
                    count = rep["count"]
                    direction = rep["direction"] 

                utilities().draw_performance_bar(img, per, bar, color, count)

            utilities().display_rep_count(img, count, total_reps)
            cv2.imshow("Skipping", img)
            cv2.waitKey(1)
        time_elapsed = int(time.process_time() - start)

        # Calorie calculator: Duration (in minutes)*(MET*3.5*weight in kg)/200
        calories_burned = int((time_elapsed / 60) * ((8.0 * 3.5 * 64) / 50))
        #Needs to check the algorithms
        return {"calories": calories_burned, "time_elapsed": time_elapsed}

    def push_ups(self):
        utilities().illustrate_exercise("Images/push.jpg", "PUSH UP'S")
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        detector = pm.posture_detector()
        count = 0
        direction = 0
        start = time.process_time()
        total_reps = self.reps * self.difficulty_level*2

        while count < total_reps:
            success, img = cap.read()
            img = detector.find_person(img, False)
            landmark_list = detector.find_landmarks(img, False)

            if len(landmark_list) != 0:
                left_arm_angle = detector.find_angle(img, 11, 13, 15)
                right_arm_angle = detector.find_angle(img, 12, 14, 16)

                per = np.interp(left_arm_angle, (220, 280), (0, 100))
                bar = np.interp(left_arm_angle, (220, 280), (650, 100))

                color = utilities().get_performance_bar_color(per)
                # When exercise is in start or terminal state
                if per == 100 or per == 0:
                    color = (0, 255, 0)
                    rep = utilities().repitition_counter(per, count, direction)
                    count = rep["count"]
                    direction = rep["direction"]  # Unused

                utilities().draw_performance_bar(img, per, bar, color, count)

            utilities().display_rep_count(img, count, total_reps)
            cv2.imshow("Skipping", img)
            cv2.waitKey(1)
            time_elapsed = int(time.process_time() - start)

        # Calorie calculator: Duration (in minutes)*(MET*3.5*weight in kg)/200
            calories_burned = int((time_elapsed / 60) * ((8.0 * 3.5 * 64) / 50))
        # Needs to check the algorithms
        return {"calories": calories_burned, "time_elapsed": time_elapsed}

    def bicep_curls(self):
        utilities().illustrate_exercise("Images/bicep.jpg", "BICEP CURLS")
       
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        detector = pm.posture_detector()
        count = 0
        direction = 0
        start = time.process_time()
        total_reps = self.reps * self.difficulty_level

        while count < total_reps:
            success, img = cap.read()
            img = detector.find_person(img, False)
            landmark_list = detector.find_landmarks(img, False)

            if len(landmark_list) != 0:
                right_arm_angle = detector.find_angle(img, 12, 14, 16)

                per = np.interp(right_arm_angle, (50, 160), (0, 100))
                bar = np.interp(right_arm_angle, (50, 160), (650, 100))

                color = utilities().get_performance_bar_color(per)
                # When exercise is in start or terminal state
                if per == 100 or per == 0:
                    color = (0, 255, 0)
                    rep = utilities().repitition_counter(per, count, direction)
                    count = rep["count"]
                    direction = rep["direction"]
                utilities().draw_performance_bar(img, per, bar, color, count)

            utilities().display_rep_count(img, count, total_reps)
            cv2.imshow("Image", img)
            cv2.waitKey(1)

            time_elapsed = int(time.process_time() - start)
            calories_burned = (time_elapsed / 60) * ((4.0 * 3.5 * 64) / 200)
        return {"calories": calories_burned, "time_elapsed": time_elapsed}

    def mountain_climbers(self):
        utilities().illustrate_exercise("Images/climber.jpg", "MOUNTAIN CLIMBERS")
        # cap = cv2.VideoCapture("TrainerData/action.mp4")
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # change 4
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        detector = pm.posture_detector()
        count = 0
        direction = 0
        start = time.process_time()

        total_reps = self.reps * self.difficulty_level

        while count < total_reps:
            success, img = cap.read()
            img = detector.find_person(img, False)
            landmark_list = detector.find_landmarks(img, False)

            if len(landmark_list) != 0:
                left_arm_angle = detector.find_angle(img, 11, 13, 15)
                right_arm_angle = detector.find_angle(img, 12, 14, 16)
                left_leg_angle = detector.find_angle(img, 24, 26, 28)

                right_leg_angle = detector.find_angle(img, 23, 25, 27)

                per = np.interp(right_leg_angle, (220, 280), (0, 100))
                bar = np.interp(right_leg_angle, (220, 280), (650, 100))

                color = utilities().get_performance_bar_color(per)
                # When exercise is in start or terminal state
                if per == 100 or per == 0:
                    color = (0, 255, 0)
                    rep = utilities().repitition_counter(per, count, direction)
                    count = rep["count"]
                    direction = rep["direction"]

                utilities().draw_performance_bar(img, per, bar, color, count)

            utilities().display_rep_count(img, count, total_reps)
            cv2.imshow("Mountain Climbers", img)
            cv2.waitKey(1)
            time_elapsed = int(time.process_time() - start)
            calories_burned = (time_elapsed / 60) * ((4.0 * 3.5 * 64) / 200)

        return {"calories": calories_burned, "time_elapsed": time_elapsed}

    def squats(self):
        utilities().illustrate_exercise("Images/squat.jpg", "SQUATS")
        # cap = cv2.VideoCapture("TrainerData/action.mp4")
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # change 5
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        detector = pm.posture_detector()
        count = 0
        direction = 0
        start = time.process_time()

        total_reps = self.reps * self.difficulty_level

        while count < total_reps:
            success, img = cap.read()
            img = detector.find_person(img, False)
            landmark_list = detector.find_landmarks(img, False)

            if len(landmark_list) != 0:
                right_leg_angle = detector.find_angle(img, 24, 26, 28)
                left_leg_angle = detector.find_angle(img, 23, 25, 27)

                per = np.interp(left_leg_angle, (190, 240), (0, 100))
                bar = np.interp(left_leg_angle, (190, 240), (650, 100))

                color = utilities().get_performance_bar_color(per)
                # When exercise is in start or terminal state
                if per == 100 or per == 0:
                    color = (0, 255, 0)
                    rep = utilities().repitition_counter(per, count, direction)
                    count = rep["count"]
                    direction = rep["direction"]
                utilities().draw_performance_bar(img, per, bar, color, count)

            utilities().display_rep_count(img, count, total_reps)
            cv2.imshow("Squats", img)
            cv2.waitKey(1)
            time_elapsed = int(time.process_time() - start)
            calories_burned = (time_elapsed / 60) * ((4.0 * 3.5 * 64) / 200)
        return {"calories": calories_burned, "time_elapsed": time_elapsed}





def main():
    exercise = simulate_exercise(difficulty_level=1)
    exercise.bicep_curls()



if __name__ == "__main__":
    main()