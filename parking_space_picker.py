import cv2
import pickle

# Charger l'image du parking
image = cv2.imread('car_park_img.jpeg')

# Liste des positions des espaces de stationnement
position_list = []

# Charger les positions des espaces de stationnement sauvegardées si elles existent
try:
    with open('car_park_positions.pkl', 'rb') as f:
        position_list = pickle.load(f)
except:
    position_list = []

# Fonction pour gérer les clics de souris
def mouse_click(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        position_list.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(position_list):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                position_list.pop(i)

    # Sauvegarde des positions dans un fichier pickle
    with open('car_park_positions.pkl', 'wb') as f:
        pickle.dump(position_list, f)

# Dimensions de chaque espace de stationnement (ajustez selon vos besoins)
width, height = 107, 48

# Assigner la fonction de clic de souris
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", mouse_click)

while True:
    img = image.copy()

    # Dessiner les rectangles pour chaque espace de stationnement
    for pos in position_list:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (0, 255, 0), 2)

    cv2.imshow("Image", img)

    # Quitter avec la touche 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
