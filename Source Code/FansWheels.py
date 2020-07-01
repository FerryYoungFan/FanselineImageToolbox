import cv2
import numpy as np


def cv_imread(filepath):
    cv_img = cv2.imdecode(np.fromfile(filepath, dtype=np.uint8), -1)
    return cv_img


def cv_imsave(img, filepath, jpgq=100):
    filetype = "." + filepath.split(".")[-1]
    if filetype == ".jpg" or filetype == ".jpeg":
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), jpgq]
        cv2.imencode(".jpg", img, encode_param)[1].tofile(filepath)
    else:
        cv2.imencode(filetype, img)[1].tofile(filepath)


def cv_imshow(image, name="Testout"):
    print("cv2 shows an image {0}".format(name))
    cv2.namedWindow(name)
    cv2.imshow(name, image)
    cv2.waitKey()


def blend_3c(img):
    """
    convert image to 3-channel image
    :param img: image with 1,3 or 4 channels
    :return: image with 3 channels (bg color: white)
    """
    if len(img.shape) == 2:
        return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    elif img.shape[2] == 4:
        return cv2.merge((img[:, :, 0], img[:, :, 1], img[:, :, 2]))
    elif img.shape[2] == 3:
        return img
    else:
        print("Error occurs when converting to 3-channel image")


def blend_4c(img, mask=None):
    """
    convert image to 4-channel image (alpha channel)
    :param img: image with 1,3 or 4 channels
    :param mask: alpha mask
    :return: image with 4 channels
    """
    if mask is None:
        mask = np.uint8(np.ones((img.shape[0], img.shape[1])) * 255)

    if len(img.shape) == 2:
        return cv2.merge((img, img, img, mask))
    elif img.shape[2] == 4:
        b, g, r, a = img[:, :, 0], img[:, :, 1], img[:, :, 2], img[:, :, 3]
        na = np.uint8((a / 255) * mask)
        return cv2.merge((b, g, r, na))
    elif img.shape[2] == 3:
        b, g, r = img[:, :, 0], img[:, :, 1], img[:, :, 2]
        return cv2.merge((b, g, r, mask))
    else:
        print("Error occurs when converting to 4-channel image")


def blend_combine(imgf, imgb):
    fg = blend_4c(imgf)
    bg = blend_4c(imgb)
    bf, gf, rf, af = fg[:, :, 0], fg[:, :, 1], fg[:, :, 2], fg[:, :, 3]
    bb, gb, rb, ab = bg[:, :, 0], bg[:, :, 1], bg[:, :, 2], bg[:, :, 3]
    fcoeff = (af / 255)
    bcoeff = (1 - fcoeff) * (ab / 255)
    bn = np.uint8(bf * fcoeff + bb * bcoeff)
    gn = np.uint8(gf * fcoeff + gb * bcoeff)
    rn = np.uint8(rf * fcoeff + rb * bcoeff)
    an = np.uint8((fcoeff + bcoeff)*255)
    img_4c = cv2.merge((bn, gn, rn, an))
    return img_4c


def preview_mask(img, mask, maskcolor=(0, 0, 255), maskalpha=0.35):
    # fg_b = np.uint8(np.ones((img.shape[0], img.shape[1])) * maskcolor[0])
    # fg_g = np.uint8(np.ones((img.shape[0], img.shape[1])) * maskcolor[1])
    # fg_r = np.uint8(np.ones((img.shape[0], img.shape[1])) * maskcolor[2])
    # fg = cv2.merge((fg_b, fg_g, fg_r))
    # mask_view = blend_combine(blend_4c(fg, mask), img, maskalpha)
    fg_b = np.asarray(mask / 255.0 * maskcolor[0], np.uint8)
    fg_g = np.asarray(mask / 255.0 * maskcolor[1], np.uint8)
    fg_r = np.asarray(mask / 255.0 * maskcolor[2], np.uint8)
    return cv2.addWeighted(blend_3c(img), 1-maskalpha, cv2.merge((fg_b, fg_g, fg_r)), maskalpha, 0)


def getHist(img=None):
    height = 100
    truncate = 200
    cb = np.ones((height, 256), dtype=np.uint8) * 16
    cg = np.ones((height, 256), dtype=np.uint8) * 16
    cr = np.ones((height, 256), dtype=np.uint8) * 16
    if img is not None:
        thumb = blend_3c(cv2.resize(img, (100, 100)))
        b, g, r = thumb[:, :, 0], thumb[:, :, 1], thumb[:, :, 2]
        hist_b, binedge_b = np.histogram(b, bins=range(257))
        hist_g, binedge_g = np.histogram(g, bins=range(257))
        hist_r, binedge_r = np.histogram(r, bins=range(257))
        hist_b[hist_b > truncate] = truncate
        hist_g[hist_g > truncate] = truncate
        hist_r[hist_r > truncate] = truncate
        maxnum = max([max(hist_b), max(hist_g), max(hist_r)])
        for i in range(256):
            len_b = int(round((hist_b[i] / maxnum) * height))
            len_g = int(round((hist_g[i] / maxnum) * height))
            len_r = int(round((hist_r[i] / maxnum) * height))
            cv2.line(cb, (i, height - 1), (i, height - 1 - len_b), 255, 1)
            cv2.line(cg, (i, height - 1), (i, height - 1 - len_g), 255, 1)
            cv2.line(cr, (i, height - 1), (i, height - 1 - len_r), 255, 1)
    result = cv2.merge((cb, cg, cr))
    result = cv2.resize(result, (160, 80))
    return result

def resize_max(img,maxlength):
    ratio = maxlength / max(img.shape[0],img.shape[1])
    newh = int(round(img.shape[0]*ratio))
    neww = int(round(img.shape[1] * ratio))
    return cv2.resize(img,(neww,newh))

def showSize(img):
    h,w = str(img.shape[0]),str(img.shape[1])
    return " ("+w+"x"+h+") "