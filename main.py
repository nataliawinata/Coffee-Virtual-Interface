# Import modul yang dibutuhkan
import os
from cvzone.HandTrackingModule import HandDetector
import cv2

# Inisialisasi kamera (device 1)
cap = cv2.VideoCapture(1)
cap.set(3, 640)  # Set lebar frame
cap.set(4, 480)  # Set tinggi frame

# Load gambar background utama
imgBackground = cv2.imread("Resources/Background.png")

# Load semua gambar mode dari folder 'Modes'
folderPathModes = "Resources/Modes"
listImgModesPath = sorted(os.listdir(folderPathModes))  # Ambil dan urutkan nama file
listImgModes = [cv2.imread(os.path.join(folderPathModes, p)) for p in listImgModesPath]  # Load semua gambar mode

# Load semua ikon dari folder 'Icons'
folderPathIcons = "Resources/Icons"
listImgIconsPath = sorted(os.listdir(folderPathIcons))  # Ambil dan urutkan nama file ikon
listImgIcons = [cv2.imread(os.path.join(folderPathIcons, p)) for p in listImgIconsPath]  # Load semua gambar ikon

# Fungsi untuk mencari index ikon berdasarkan nama file
def find_icon_index(name):
    for i, p in enumerate(listImgIconsPath):
        if name == p:
            return i
    return 0  # Jika tidak ditemukan, kembalikan index 0

# Ambil index untuk ikon kosong (empty) dan null
idx_empty = find_icon_index("empty.png")
idx_null = find_icon_index("null.png")

# Posisi masing-masing ikon (dalam tampilan)
icon_positions = [
    (133, 636),
    (243, 636),
    (353, 636),
    (463, 636),
    (573, 636)
]

# Mode awal dimulai dari 1
mode = 1

# Inisialisasi daftar ikon yang dipilih (semua kosong di awal)
icons_selected = [idx_empty] * 5

# Inisialisasi hand detector dari cvzone
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Variabel gesture untuk deteksi gerakan tangan
gesture = -1
gesture_old = -1
counter = 0
counterMax = 60  # Jumlah frame untuk mengkonfirmasi gesture

# Posisi tombol reset (untuk gesture 5 jari)
reset_position = (735, 22)

# Posisi dan ukuran animasi lingkaran hijau untuk gesture
anim_positions_sizes = {
    1: ((1137, 199), (102, 102)),  # Gesture 1
    2: ((1000, 389), (102, 102)),  # Gesture 2
    3: ((1139, 585), (102, 102)),  # Gesture 3
    5: ((785, 72), (50, 50))       # Gesture reset (5 jari)
}

# Fungsi untuk menggambar ikon-ikon yang telah dipilih
def draw_icons(img):
    for i, icon_idx in enumerate(icons_selected):
        x, y = icon_positions[i]
        h, w, _ = listImgIcons[icon_idx].shape
        img[y:y+h, x:x+w] = listImgIcons[icon_idx]

# Main loop program
while True:
    success, img = cap.read()  # Baca frame dari kamera
    if not success:
        break  # Keluar jika kamera tidak tersedia

    tempBackground = imgBackground.copy()  # Salin background
    hands, img = detector.findHands(img)  # Deteksi tangan
    tempBackground[139:139 + 480, 50:50 + 640] = img  # Tempel frame kamera ke background
    tempBackground[0:720, 847:1280] = listImgModes[mode - 1]  # Tampilkan gambar mode saat ini

    fingers = []
    gesture = -1  # Reset gesture

    if hands:
        fingers = detector.fingersUp(hands[0])  # Deteksi jari yang terangkat

        # Deteksi kombinasi jari untuk gesture tertentu
        if fingers == [0,1,0,0,0]:
            gesture = 1
        elif fingers == [0,1,1,0,0]:
            gesture = 2
        elif fingers == [0,1,1,1,0]:
            gesture = 3
        elif fingers == [1,1,1,1,1]:
            gesture = 5  # Reset

        # Pada mode 6, hanya gesture reset yang diperbolehkan
        if mode == 6 and gesture != 5:
            gesture = -1  # Abaikan gesture lain

        # Hitung berapa lama gesture ditahan
        if gesture == gesture_old and gesture != -1:
            counter += 1
        else:
            counter = 0
        gesture_old = gesture

        # Gambar animasi lingkaran hijau saat gesture dikenali
        if gesture in anim_positions_sizes and counter > 0:
            center, radius = anim_positions_sizes[gesture]
            angle = int((counter / counterMax) * 360)
            cv2.ellipse(tempBackground, center, radius, 0, 0, angle, (0,255,0), 5)

        # Eksekusi aksi jika gesture ditahan cukup lama
        if counter >= counterMax:
            if gesture == 5:
                # Reset semua ikon dan kembali ke mode 1
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
                        icons_selected[1] = find_icon_index(f"{gesture + 3}.png")  # 4.png, 5.png, 6.png
                        mode = 3
                elif mode == 3:
                    if gesture in [1,2,3]:
                        icons_selected[2] = find_icon_index(f"{gesture + 6}.png")  # 7.png, 8.png, 9.png
                        mode = 4
                elif mode == 4:
                    if gesture in [1,2,3]:
                        icons_selected[3] = find_icon_index(f"{gesture + 9}.png")  # 10.png, 11.png, 12.png
                        if icons_selected[3] != idx_null:
                            if icons_selected[4] == idx_null:
                                mode = 6
                            else:
                                mode = 5
                elif mode == 5:
                    if gesture in [1,2,3]:
                        icons_selected[4] = find_icon_index(f"{gesture + 12}.png")  # 13.png, 14.png, 15.png
                        mode = 6  # Selesai, ke mode akhir

            counter = 0  # Reset counter
            gesture_old = -1  # Reset gesture lama

    draw_icons(tempBackground)  # Tampilkan ikon yang terpilih
    cv2.imshow("Background", tempBackground)  # Tampilkan UI
    if cv2.waitKey(1) == ord('q'):
        break  # Tekan 'q' untuk keluar
