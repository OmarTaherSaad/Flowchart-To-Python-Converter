import pytesseract as tess
from PIL import Image
import numpy as np
import cv2
import sys
from format3 import *
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
np.set_printoptions(threshold=sys.maxsize)


def Get_All_Contours_From_Image(img):
    img = np.array(img, np.uint8)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    Ret, Threshold = cv2.threshold(gray, 127, 255, 0)
    Contours, Hierarchy = cv2.findContours(
        Threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    Contours_Sorted = sorted(Contours, key=cv2.contourArea)
    List_Contours = Contours_Sorted[::-1]
    return List_Contours


def Highlight_Shapes_and_Lines(img, List_Contours):
    Shapes_Contours = []
    cv2.drawContours(img, List_Contours, 1, (0, 255, 0), 2)
    for i in range(2, len(List_Contours)):
        if (cv2.contourArea(List_Contours[i]) / cv2.contourArea(List_Contours[1])) > 0.01:
            Shapes_Contours.append(List_Contours[i])
            cv2.drawContours(img, List_Contours, i, (255, 0, 0), 10)

    Shapes_Contours = np.array(Shapes_Contours)
    return img, Shapes_Contours


def Get_Starting_Shape(img, Shapes_Contours):
    for i in range(0, len(Shapes_Contours)):
        if Contour_To_String(img, Shapes_Contours[i]) == "Start" or \
                Contour_To_String(img, Shapes_Contours[i]) == "start" or \
                Contour_To_String(img, Shapes_Contours[i]) == "begun":
            return i


def Image_To_String(img):
    img = np.array(img, np.uint8)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    val, binary = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    custom_config = r'-l eng+por --psm 6'
    text = tess.image_to_string(Image.fromarray(
        binary), lang='eng', config=custom_config)
    return text


def Contour_To_String(img, Contour):
    Image_Copy = img.copy()
    Image_Copy = np.array(Image_Copy, np.uint8)
    fill_color = [255, 200, 255]
    mask_value = 255
    contours = [Contour]
    stencil = np.zeros(Image_Copy.shape[:-1]).astype(np.uint8)
    cv2.fillPoly(stencil, contours, mask_value)
    sel = stencil != mask_value
    Image_Copy[sel] = fill_color

    Image_Copy = Return_Image_with_Text_Only(Image_Copy)

    return Image_To_String(Image_Copy)


def Return_Image_with_Text_Only(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    brown_lo = np.array([0, 0, 0])
    brown_hi = np.array([255, 255, 254])
    mask = cv2.inRange(hsv, brown_lo, brown_hi)
    img[mask <= 0] = (255, 255, 255)

    kernel = np.ones((3, 3), np.uint8)
    img_erosion = cv2.erode(img, kernel, iterations=1)

    return img_erosion


def Find_Emerging_Line(img, Contour, Contours_List):
    for point in Contour:
        y = point[0][0]
        x = point[0][1]
        Loop_Start_y = y - 9
        Loop_Start_x = x - 9
        Green_Count = 0
        for i in range(Loop_Start_y, Loop_Start_y + 19):
            for j in range(Loop_Start_x, Loop_Start_x + 19):
                if img[j, i, 1] == 255 and img[j, i, 0] == 0 and img[j, i, 2] == 0:
                    Green_Count = Green_Count + 1

                    if Green_Count >= 20:
                        Mark_By_Circle(img, i, j, "green", 20)
                        return Get_Index_From_Contour(Contours_List, x, y)


def Is_Rhombus(Contour):
    approx = cv2.approxPolyDP(
        Contour, 0.01 * cv2.arcLength(Contour, True), True)
    if len(approx) == 4:
        x, y, w, h = cv2.boundingRect(approx)
        aspr = float(w) / h
        if 0.6 <= aspr <= 1.4:
            return True
        else:
            return False
    return False


def Mark_By_Circle(img, x, y, color, rad):
    center_coordinates = (x, y)
    radius = rad

    if color == "red":
        color = (255, 0, 0)
    elif color == "green":
        color = (0, 255, 0)
    elif color == "blue":
        color = (0, 0, 255)
    elif color == "black":
        color = (0, 0, 0)
    elif color == "white":
        color = (255, 255, 255)

    thickness = -1
    cv2.circle(img, center_coordinates, radius, color, thickness)


def Get_Index_From_Contour(Contour, x, y):
    i = 0
    for point in Contour:
        a = point[0][0]
        b = point[0][1]
        if (y - 3) <= a <= (y + 3) and (x - 3) <= b <= (x + 3):
            return i
        else:
            i = i + 1


def Index_Next_Contour(img, Index, Contour, List_Contours, Shape):
    Check = False
    Condition = "Not Set"

    if Is_Rhombus(Shape):
        Check = True

    x_start = Contour[Index][0][0]
    y_start = Contour[Index][0][1]

    Start, End, Step = Start_End_Step(img, Index, Contour)

    itr = 0

    for point in range(Start, End, Step):
        x = Contour[point][0][0]
        y = Contour[point][0][1]

        if Check and (itr % 20) == 0:
            Crop_x1 = x - 110
            Crop_y1 = y - 70
            Crop_x2 = x + 110
            Crop_y2 = y + 70

            Copy_Image = img.copy()

            Cropped_Image = Copy_Image[Crop_y1:Crop_y2, Crop_x1:Crop_x2]

            Cropped_Image = Return_Image_with_Text_Only(Cropped_Image)

            word = Image_To_String(Cropped_Image)

            if word == "True" or word == "False":
                Condition = word
                Check = False

        itr = itr + 1
        Stop = True
        Loop_Start_y = y - 6
        Loop_Start_x = x - 6
        for i in range(Loop_Start_x, Loop_Start_x + 13):
            for j in range(Loop_Start_y, Loop_Start_y + 13):
                if img[j, i, 1] == 255 and img[j, i, 0] == 0 and img[j, i, 2] == 0:
                    Stop = False

        if Stop:
            Mark_By_Circle(img, x_start, y_start, "red", 25)
            Mark_By_Circle(img, x, y, "red", 20)
            return Get_Contour_From_Point(List_Contours, x, y), Condition


def Get_Contour_From_Point(List_Contours, x, y):
    for i in range(2, len(List_Contours)):
        if cv2.pointPolygonTest(List_Contours[i], (x + 20, y), False) > 0 \
                or cv2.pointPolygonTest(List_Contours[i], (x, y + 20), False) > 0 \
                or cv2.pointPolygonTest(List_Contours[i], (x, y - 20), False) > 0 \
                or cv2.pointPolygonTest(List_Contours[i], (x - 20, y), False) > 0:
            return i


def Start_End_Step(img, Index, Contour):

    Index_A = Index
    Index_B = Index

    Step = 0

    while Step == 0:
        if (Index_A + 20) <= len(Contour):
            Index_A = Index_A + 20
        if (Index_B - 20) >= 0:
            Index_B = Index_B - 20

        A_x = Contour[Index_A][0][0]
        A_y = Contour[Index_A][0][1]
        B_x = Contour[Index_B][0][0]
        B_y = Contour[Index_B][0][1]

        if img[A_y, A_x, 1] == 0 and img[A_y, A_x, 0] == 255 and img[A_y, A_x, 2] == 0 and \
                img[B_y, B_x, 1] == 255 and img[B_y, B_x, 0] == 0 and img[B_y, B_x, 2] == 0:
            Step = -1
        elif img[A_y, A_x, 1] == 255 and img[A_y, A_x, 0] == 0 and img[A_y, A_x, 2] == 0 and \
                img[B_y, B_x, 1] == 0 and img[B_y, B_x, 0] == 255 and img[B_y, B_x, 2] == 0:
            Step = 1

    if Step == 1:
        return Index, len(Contour), Step
    elif Step == -1:
        return Index, 0, Step


def main():
    argv = sys.argv
    image_path = argv[1]
    Flowchart_Image = cv2.imread(image_path)

    try:
        List_of_Sorted_Contours = Get_All_Contours_From_Image(Flowchart_Image)
        Highlighted_Image, List_of_Shapes = Highlight_Shapes_and_Lines(
            Flowchart_Image, List_of_Sorted_Contours)
        To_Code = []
        Conditions = ["Not Set"]

        Starting_Contour_Index = Get_Starting_Shape(
            Highlighted_Image, List_of_Shapes)
        if Starting_Contour_Index is None:
            print('Fail')
            print('Please represent a Starting Symbol in your Flowchart.')
            return

        Flowchart_Outerline = List_of_Sorted_Contours[1]
        To_Code.append(Contour_To_String(Highlighted_Image,
                                         List_of_Shapes[Starting_Contour_Index]))

        Index_Follow = Find_Emerging_Line(
            Highlighted_Image, List_of_Shapes[Starting_Contour_Index], Flowchart_Outerline)
        Get_Index, State = Index_Next_Contour(
            Highlighted_Image, Index_Follow, Flowchart_Outerline, List_of_Sorted_Contours, List_of_Shapes[Starting_Contour_Index])
        To_Code.append(Contour_To_String(Highlighted_Image,
                                         List_of_Sorted_Contours[Get_Index]))
        Conditions.append(State)

        Conditional_Index = -1

        for i in range(len(List_of_Shapes) - 2):
            if Is_Rhombus(List_of_Sorted_Contours[Get_Index]):
                Conditional_Index = Get_Index

            if Conditional_Index > 0 and (Contour_To_String(Highlighted_Image, List_of_Sorted_Contours[Get_Index]) == "End" or
                                          Contour_To_String(Highlighted_Image, List_of_Sorted_Contours[Get_Index]) == "Ena" or
                                          Contour_To_String(Highlighted_Image, List_of_Sorted_Contours[Get_Index]) == "Gud"):
                Get_Index = Conditional_Index

            Index_Follow = Find_Emerging_Line(
                Highlighted_Image, List_of_Sorted_Contours[Get_Index], Flowchart_Outerline)
            Get_Index, State = Index_Next_Contour(
                Highlighted_Image, Index_Follow, Flowchart_Outerline, List_of_Sorted_Contours, List_of_Sorted_Contours[Get_Index])
            To_Code.append(Contour_To_String(Highlighted_Image,
                                             List_of_Sorted_Contours[Get_Index]))

            if Is_Rhombus(List_of_Sorted_Contours[Get_Index]):
                State = "Bool"

            Conditions.append(State)

        for item in range(0, len(Conditions)):
            if Conditions[item] == "Bool" and not (Conditions[item + 1] == "True" or Conditions[item + 1] == "False"):
                print('Fail')
                print(
                    'Please clarify the True and False labels on the conditional block branches.')
                return

        Code_Path = formatting(To_Code, Conditions)

        if len(To_Code) <= 1:
            print('Fail')
            print('Please insert a reliable Flowchart.')
            return

        print('Success')
        print(Code_Path)

    except Exception:
        print('Fail')
        print('Please insert a reliable Flowchart.')


if __name__ == "__main__":
    main()
