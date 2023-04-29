import requests
import cv2
import numpy as np

print('start')
url = "https://maps.googleapis.com/maps/api/staticmap?center=40.714728,-73.998672&zoom=12&maptype=satellite&size=400x400&key=AIzaSyA3kg7YWugGl1lTXmAmaBGPNhDW9pEh5bo&signature=5tyWj9NAOGlFz33nroLk6sV4ASk="
response = requests.get(url).content
image = cv2.imdecode(np.frombuffer(response, np.uint8), cv2.IMREAD_UNCHANGED)

cv2.imshow("Satellite Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()