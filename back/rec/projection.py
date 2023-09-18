import cv2


def preprocess(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    Blur = cv2.GaussianBlur(gray, (5, 5), 1)
    Canny = cv2.Canny(Blur, 10, 50)

    return Canny


def find_max_rectangle(img):
    contours = cv2.findContours(img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)[0]
    max_area = -1

    for contour in contours:
            epsilon = 0.05*cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            if len(approx) == 4 and cv2.contourArea(contour) > max_area:
                max_cont = contour
                max_area = cv2.contourArea(contour)
                max_approx = cv2.approxPolyDP(contour, epsilon, True)

    return max_cont, max_approx


def cut_roi(img, contour):
    cv2.boundingRect()


def show_contours(img, contours):
    for idx in range(len(contours[0])):
        contour = contours[0][idx:idx+2]
        cv2.drawContours(img, [contour], -1, (0, 255, 0), 2)
        cv2.imshow('Image rects', img)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


def main():
    img = cv2.imread("./test_data/test_1.jpg")
    processed_img = preprocess(img)
    contour, approx = find_max_rectangle(processed_img)
    show_contours(img, [approx])


if __name__ == "__main__":
    main()
