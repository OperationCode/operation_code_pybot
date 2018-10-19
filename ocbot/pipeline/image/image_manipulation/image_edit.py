import cv2
import numpy as np


def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged


def find_white_pixels(canny_image):
    return np.argwhere(canny_image == 255)
    # reduce top, left, rigth and bottom size until we find the rectangular bound.


def min_max_values(coord_list):
    coord_dict = {'min_row': float('inf'),
                  'max_row': float('-inf'),
                  'min_col': float('inf'),
                  'max_col': float('-inf'),
                  }
    for coord in coord_list:
        if coord[0] < coord_dict['min_row']:
            coord_dict['min_row'] = coord[0]

        if coord[0] > coord_dict['max_row']:
            coord_dict['max_row'] = coord[0]

        if coord[1] < coord_dict['min_col']:
            coord_dict['min_col'] = coord[1]
        if coord[1] > coord_dict['max_col']:
            coord_dict['max_col'] = coord[1]

    return coord_dict


def retain_aspect_scale(width, height, max_dim):
    largest_dim = max(width, height)

    ratio = max_dim/largest_dim
    return ratio



def change_background(cropped_img):

    no_transparency =  cv2.cvtColor(cropped_img, cv2.COLOR_BGRA2BGR)
    print(no_transparency.shape)
    mask = cv2.cvtColor(no_transparency, cv2.COLOR_BGR2GRAY)
    _, alpha = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY)

    img_tuple = cv2.split(no_transparency)

    b, g, r = img_tuple

    #rgba = [b, g, r, alpha]
    rgba = [b, g, r, alpha]
    dst = cv2.merge(rgba, 3)
    print('show')
    cv2.imshow("image", dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print('shown')
    #dst= cv2.cvtColor(dst, cv2.COLOR_BGRA2BGR)

    cv2.imwrite("test.png", dst)
    return dst


def pad_image(corrected_image, max_size):
    old_size = corrected_image.shape[:2]


    delta_w = max_size - old_size[1]
    delta_h = max_size - old_size[0]


    top, bottom = delta_h // 2, delta_h - (delta_h // 2)
    left, right = delta_w // 2, delta_w - (delta_w // 2)

    color = [255, 255, 255, 255]
    new_im = cv2.copyMakeBorder(corrected_image, top, bottom, left, right, cv2.BORDER_CONSTANT,
                                value=color)

    cv2.imwrite("test.png", new_im)

    img = cv2.imread('test.png')
    blur = cv2.bilateralFilter(img, 9,75,75)

    cv2.imwrite("test.png", new_im)

    #return new_im
    cv2.imshow("image", blur)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main(img_input):
    img = cv2.imread(img_input, 0)

    edges = auto_canny(img)
    min_bound = find_white_pixels(edges)

    bound = min_max_values(min_bound)

    img = cv2.imread(img_input, cv2.IMREAD_UNCHANGED)

    crop_img = img[bound['min_row']:bound['max_row'], bound['min_col']: bound['max_col']]
    scale_factor = retain_aspect_scale(bound['max_row'] - bound['min_row'], bound['max_col'] - bound['min_col'],
                                       200 - 30)


    scaled = cv2.resize(crop_img, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)

    corrected_image = change_background(scaled)
    pad_image(corrected_image, 200)

    # cv2.imshow("cropped", scaled)
    #
    # cv2.waitKey(0)


if __name__ == '__main__':
    imarr = ['1.png', '1.jpg', '2.png']

    #imarr = ['ccamp.png', 'firehouse.png', 'guild.jpg']
    for img in imarr:
        main(img)
