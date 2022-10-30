import cv2
import numpy as np

def apply_brightness_contrast(input_img, brightness, contrast):
    # brightness = map(brightness, 0, 510, -255, 255)
    # contrast = map(contrast, 0, 254, -127, 127)
    # input_img = cv2.imdecode(input_img, flags=1)
    
    # print(brightness)
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow)/255
        gamma_b = shadow
        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()
    if contrast != 0:
        f = float(131 * (contrast + 127)) / (127 * (131 - contrast))
        alpha_c = f
        gamma_c = 127*(1-f)
        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)
    # cv2.putText(buf,'B:{},C:{}'.format(brightness,contrast),(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    # print(buf.shape)
    return buf

# def map(x, in_min, in_max, out_min, out_max):
#     return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)