import torch
from super_gradients.training import models
import os
import cv2

def getPath(path):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), path)

model = models.get('yolo_nas_l', num_classes=3, checkpoint_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "yolo_custom_w\combined yolo\weapon.pth"))


lab = {0: "Person", 1: "Knife", 2: "Gun"}

cols = {0: (255, 165, 18), 1: (0, 68, 172), 2: (12, 69, 188)}

while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            results = model.to(0 if torch.cuda.is_available() else "cpu").predict(frame)
            # print(results[0].prediction.labels)
            col = (255, 255, 0)
                
            for box in results[0].prediction.bboxes_xyxy:
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(frame, (x1, y1), (x2, y2), col, 3)
                c = 0
                for label in results[0].prediction.labels:
                    confidence = 0
                    try:
                         confidence = results[0].prediction.confidence[c]
                    except:
                         pass
                    cv2.putText(frame, f"{lab[label]}: {confidence:.2f}", (x1, y1-15), cv2.FONT_HERSHEY_SIMPLEX, 1.1, cols[label], 2)
                    c+= 1
            cv2.imshow('Detected Objects', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
cap.release()
cv2.destroyAllWindows()