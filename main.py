import os
from cvzone.HandTrackingModule import HandDetector
import cv2

cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread("Resources/Background.png")

folderPathModes = "Resources/Modes"
listImgModesPath = sorted(os.listdir(folderPathModes))
listImgModes = [cv2.imread(os.path.join(folderPathModes, p)) for p in listImgModesPath]

folderPathIcons = "Resources/Icons"
listImgIconsPath = sorted(os.listdir(folderPathIcons))
listImgIcons = [cv2.imread(os.path.join(folderPathIcons, p)) for p in listImgIconsPath]

def find_icon_index(name):
    for i, p in enumerate(listImgIconsPath):
        if name == p:
            return i
    return 0

idx_empty = find_icon_index("empty.png")
idx_null = find_icon_index("null.png")

icon_positions = [
    (133, 636),
    (243, 636),
    (353, 636),
    (463, 636),
    (573, 636)
]

mode = 1
icons_selected = [idx_empty] * 5

detector = HandDetector(detectionCon=0.8, maxHands=1)

gesture = -1
gesture_old = -1
counter = 0
counterMax = 60

reset_position = (735, 22)

anim_positions_sizes = {
    1: ((1137, 199), (102, 102)),  # elips 205x205 pixel
    2: ((1000, 389), (102, 102)),
    3: ((1139, 585), (102, 102)),
    5: ((785, 72), (50, 50))       # Reset gesture (5 jari), elips 100x100
}

def draw_icons(img):
    for i, icon_idx in enumerate(icons_selected):
        x, y = icon_positions[i]
        h, w, _ = listImgIcons[icon_idx].shape
        img[y:y+h, x:x+w] = listImgIcons[icon_idx]

while True:
    success, img = cap.read()
    if not success:
        break

    tempBackground = imgBackground.copy()
    hands, img = detector.findHands(img)
    tempBackground[139:139 + 480, 50:50 + 640] = img
    tempBackground[0:720, 847:1280] = listImgModes[mode - 1]

    fingers = []
    gesture = -1

    if hands:
        fingers = detector.fingersUp(hands[0])

        # Deteksi gesture hanya 1,2,3 dan 5 (reset)
        if fingers == [0,1,0,0,0]:
            gesture = 1
        elif fingers == [0,1,1,0,0]:
            gesture = 2
        elif fingers == [0,1,1,1,0]:
            gesture = 3
        elif fingers == [1,1,1,1,1]:
            gesture = 5

        # Mode 6 hanya baca gesture 5 (reset)
        if mode == 6 and gesture != 5:
            gesture = -1  # abaikan gesture selain 5

        if gesture == gesture_old and gesture != -1:
            counter += 1
        else:
            counter = 0
        gesture_old = gesture

        if gesture in anim_positions_sizes and counter > 0:
            center, radius = anim_positions_sizes[gesture]
            angle = int((counter / counterMax) * 360)
            cv2.ellipse(tempBackground, center, radius, 0, 0, angle, (0,255,0), 5)

        if counter >= counterMax:
            if gesture == 5:
                # Reset semua ke awal
                icons_selected = [idx_empty] * 5
                mode = 1
            else:
                if mode == 1:
                    if gesture == 1:
                        icons_selected[0] = find_icon_index("1.png")
                        icons_selected[4] = idx_null
                        mode = 2
                    elif gesture == 2:
                        icons_selected[0] = find_icon_index("2.png")
                        icons_selected[1:4] = [idx_null]*3
                        mode = 5
                    elif gesture == 3:
                        icons_selected[0] = find_icon_index("3.png")
                        mode = 2
                elif mode == 2:
                    if gesture in [1,2,3]:
                        icons_selected[1] = find_icon_index(f"{gesture + 3}.png")
                        mode = 3
                elif mode == 3:
                    if gesture in [1,2,3]:
                        icons_selected[2] = find_icon_index(f"{gesture + 6}.png")
                        mode = 4
                elif mode == 4:
                    if gesture in [1,2,3]:
                        icons_selected[3] = find_icon_index(f"{gesture + 9}.png")
                        if icons_selected[3] != idx_null:
                            if icons_selected[4] == idx_null:
                                mode = 6
                            else:
                                mode = 5
                elif mode == 5:
                    if gesture in [1,2,3]:
                        icons_selected[4] = find_icon_index(f"{gesture + 12}.png")
                        mode = 6

            counter = 0
            gesture_old = -1

    draw_icons(tempBackground)
    cv2.imshow("Background", tempBackground)
    if cv2.waitKey(1) == ord('q'):
        break
