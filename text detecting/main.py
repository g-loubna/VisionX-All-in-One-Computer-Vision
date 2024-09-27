import cv2 
import easyocr 
import matplotlib.pyplot as plt

# Read the image
image_path = 'txt1.PNG'

img = cv2.imread(image_path)

reader = easyocr.Reader(['en'], gpu = False)
text_ = reader.readtext(img)

threshold = 0.25
#detect text in the photo 
for t in text_:
    print(t)


    bbox, text, score = t
    if score > threshold :
        cv2.rectangle(img, bbox[0], bbox[2], (0, 255, 0), 5 )
        cv2.putText(img, text, bbox[0], cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)

plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.show()

"""for t in result:
    print(t)

    bbox, text, prob = t

    if prob > 0.25:
        print(f'Detected text: {text} with confidence: {prob}')
        cv2.rectangle(img, bbox[0], bbox[2], (0, 255, 0), 5)
        cv2.putText(img, text, bbox[0], cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.show()"""