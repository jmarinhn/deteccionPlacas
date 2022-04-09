import numpy as np
import argparse
import imutils
import time
import cv2
import pytesseract
from imutils.video import VideoStream
from imutils.video import FPS
from imutils.object_detection import non_max_suppression

##Ruta a la instalación de Tesseract en MacOS.
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/Cellar/tesseract/5.1.0/bin/tesseract'


def box_extractor(scores, geometry, min_confidence):

    num_rows, num_cols = scores.shape[2:4]
    rectangles = []
    confidences = []

    for y in range(num_rows):
        scores_data = scores[0, 0, y]
        x_data0 = geometry[0, 0, y]
        x_data1 = geometry[0, 1, y]
        x_data2 = geometry[0, 2, y]
        x_data3 = geometry[0, 3, y]
        angles_data = geometry[0, 4, y]

        for x in range(num_cols):
            if scores_data[x] < min_confidence:
                continue

            offset_x, offset_y = x * 4.0, y * 4.0

            angle = angles_data[x]
            cos = np.cos(angle)
            sin = np.sin(angle)

            box_h = x_data0[x] + x_data2[x]
            box_w = x_data1[x] + x_data3[x]

            end_x = int(offset_x + (cos * x_data1[x]) + (sin * x_data2[x]))
            end_y = int(offset_y + (cos * x_data2[x]) - (sin * x_data1[x]))
            start_x = int(end_x - box_w)
            start_y = int(end_y - box_h)

            rectangles.append((start_x, start_y, end_x, end_y))
            confidences.append(scores_data[x])

    return rectangles, confidences


def get_arguments():
    ap = argparse.ArgumentParser() 
    ap.add_argument('-v', '--video', type=str,
                    help='Ruta a un video')
    ap.add_argument('-east', '--east', type=str, required=True,
                    help='ruta al modo de deteccion de texto EAST')
    ap.add_argument('-c', '--min_confidence', type=float, default=0.7,
                    help='Nivel de confianza minimo de proceso a region')
    ap.add_argument('-w', '--width', type=int, default=320,
                    help='Ancho de imagen redimensionada (multiple of 32)')
    ap.add_argument('-e', '--height', type=int, default=320,
                    help='Alto de imagen redimensionada (multiple of 32)')
    ap.add_argument('-p', '--padding', type=float, default=0.0,
                    help='La distancia entre cada region de interes')                   
    arguments = vars(ap.parse_args())

    return arguments


if __name__ == '__main__':

    args = get_arguments()

    w, h = None, None
    new_w, new_h = args['width'], args['height']
    ratio_w, ratio_h = None, None

    layer_names = ['feature_fusion/Conv_7/Sigmoid', 'feature_fusion/concat_3']

    print("Iniciando el motor OCR...")
    net = cv2.dnn.readNet(args["east"])

    if not args.get('video', False):
        print("Activando webcam...")
        vs = VideoStream(src=0).start()
        time.sleep(1)
        print("Esperando placas...")
    else:
        vs = cv2.VideoCapture(args['video'])

    fps = FPS().start()

    while True:
        frame = vs.read()
        frame = frame[1] if args.get('video', False) else frame
        

        if frame is None:
            break

        frame = imutils.resize(frame, width=1000)
        orig = frame.copy()
        orig_h, orig_w = orig.shape[:2]

        if w is None or h is None:
            h, w = frame.shape[:2]
            ratio_w = w / float(new_w)
            ratio_h = h / float(new_h)

        frame = cv2.resize(frame, (new_w, new_h))

        blob = cv2.dnn.blobFromImage(frame, 1.0, (new_w, new_h), (123.68, 116.78, 103.94),
                                     swapRB=True, crop=False)
        net.setInput(blob)
        scores, geometry = net.forward(layer_names)

        rectangles, confidences = box_extractor(scores, geometry, min_confidence=args['min_confidence'])
        boxes = non_max_suppression(np.array(rectangles), probs=confidences)

        for (start_x, start_y, end_x, end_y) in boxes:

            start_x = int(start_x * ratio_w)
            start_y = int(start_y * ratio_h)
            end_x = int(end_x * ratio_w)
            end_y = int(end_y * ratio_h)

            dx = int((end_x - start_x) * args['padding'])
            dy = int((end_y - start_y) * args['padding'])

            start_x = max(0, start_x - dx)
            start_y = max(0, start_y - dy)
            end_x = min(orig_w, end_x + (dx * 2))
            end_y = min(orig_h, end_y + (dy * 2))

            # regionPlaca
            regionPlaca = orig[start_y:end_y, start_x:end_x]

            # OCR
            config = '-l eng --oem 1 --psm 6'
            text = pytesseract.image_to_string(regionPlaca, config=config)

            if text != "":
                if len(text)==8: 
                    print(f"Placa detectada: {text} \n")
                    with open('placas.txt', 'a', encoding='utf-8') as f:
                        f.write(f"Placa detectada: {text} \n")
                        f.close()
                    cv2.rectangle(orig, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
                    cv2.putText(orig, text, (start_x, start_y - 20),
                                cv2.FONT_HERSHEY_COMPLEX, 1.2, (34, 226, 66), 3)
                break
            break            
        

        fps.update()
        


        cv2.imshow("Deteccion de Placas", orig)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

    fps.stop()
    print(f"[INFO] Tiempo de ejecución: {round(fps.elapsed(), 2)} s")
    print(f"Gracias por utilizar nuestro software!")

    if not args.get('video', False):
        vs.stop()

    else:
        vs.release()

    cv2.destroyAllWindows()
