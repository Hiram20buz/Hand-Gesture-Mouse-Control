import cv2
import mediapipe as mp
import pyautogui
capture_hands = mp.solutions.hands.Hands()
drawing_option = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
cap = cv2.VideoCapture(0)
x1 = y1 = x2 = y2 = 0
while cap.isOpened():
    ret, frame = cap.read()
    image_height, image_width, ret = frame.shape
    frame = cv2.flip(frame, 1)
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output_hands = capture_hands.process(rgb_image)
    all_hands = output_hands.multi_hand_landmarks
    if all_hands:
        for hand in all_hands:
            drawing_option.draw_landmarks(frame, hand)
            one_hand_landmarks = hand.landmark
            for id, lm in enumerate(one_hand_landmarks):
                x = int(lm.x * image_width)
                y = int(lm.y * image_height)
                print(x, y)
                #Specific points
                if id == 8:
                    mouse_x = int(screen_width / image_width * x)
                    mouse_y = int(screen_height / image_height * y)
                    cv2.circle(frame, (x, y), 10, (0, 255, 255))
                    pyautogui.moveTo(mouse_x, mouse_y)
                    x1 = x
                    y1 = y
                if id == 4:
                    x2 = x
                    y2 = y
                    cv2.circle(frame, (x, y), 10, (0, 255, 255))
        dist = y2 - y1
        print(dist)
        if (dist < 40):
            pyautogui.click()
            print("clicked")
    cv2.imshow("Hand movement video capture", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
