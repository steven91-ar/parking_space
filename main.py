import cv2
import pickle
import numpy as np
import cvzone

# Charger les positions des espaces de stationnement
with open('car_park_positions.pkl', 'rb') as f:
    position_list = pickle.load(f)

# Capture vidéo du parking
cap = cv2.VideoCapture('car_park.mp4')

# Vérifier si la vidéo s'ouvre correctement
if not cap.isOpened():
    print("Erreur : Impossible d'ouvrir la vidéo.")
    exit()

# Dimensions des espaces de stationnement
width, height = 107, 48


def check_parking_space(img_processed, img_original):
    space_counter = 0

    for pos in position_list:
        x, y = pos
        # Extraire la région d'intérêt pour chaque espace
        img_crop = img_processed[y:y + height, x:x + width]

        # Compter les pixels blancs (zones occupées)
        count = cv2.countNonZero(img_crop)

        # Définir les seuils pour considérer l'espace comme vide ou occupé
        if count < 900:
            color = (0, 255, 0)  # Vert pour espace libre
            thickness = 5
            space_counter += 1
        else:
            color = (0, 0, 255)  # Rouge pour espace occupé
            thickness = 2

        # Dessiner les rectangles autour des espaces sur l'image originale
        cv2.rectangle(img_original, pos, (pos[0] + width, pos[1] + height), color, thickness)

        # Afficher le nombre de pixels dans chaque espace sur l'image originale
        cvzone.putTextRect(img_original, str(count), (x, y + height - 3), scale=1, thickness=2, offset=0, colorR=color)

    # Afficher le nombre total d'espaces libres sur l'image originale
    cvzone.putTextRect(img_original, f'Libre: {space_counter}/{len(position_list)}', (100, 50), scale=3, thickness=5, offset=20,
                       colorR=(0, 200, 0))


while True:
    success, img = cap.read()
    if not success:
        print("Fin de la vidéo ou erreur lors de la lecture.")
        break

    # Pré-traitement de l'image
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
    img_thresh = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    img_median = cv2.medianBlur(img_thresh, 5)
    img_dilate = cv2.dilate(img_median, np.ones((3, 3), np.uint8), iterations=1)

    # Vérification des espaces de stationnement avec l'image originale en paramètre
    check_parking_space(img_dilate, img)

    # Afficher la vidéo avec les annotations
    cv2.imshow("Image", img)

    # Quitter avec la touche 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer la capture et fermer les fenêtres
cap.release()
cv2.destroyAllWindows()
