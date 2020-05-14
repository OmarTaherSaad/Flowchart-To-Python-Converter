import pytesseract as tess
from PIL import Image
import numpy as np
import cv2
import sys
from format3 import *
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
np.set_printoptions(threshold=sys.maxsize)


# Function to Get all Contours from the Input Image involving the Flowchart objects and the main Flowchart Figure
# This Function also Sorts these contours in descending order by their areas
def Get_All_Contours_From_Image(img):

    # Image Processing involving Threshold
    img = np.array(img, np.uint8)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    Ret, Threshold = cv2.threshold(gray, 127, 255, 0)

    # Find all contours
    Contours, Hierarchy = cv2.findContours(Threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # List those contours by area in ascending order
    Contours_Sorted = sorted(Contours, key=cv2.contourArea)

    # Inverse the ordered list
    List_Contours = Contours_Sorted[::-1]

    return List_Contours


# Function to Highlight the Flowchart Shapes by Red Color and Flowchart Arrows by Green Color
def Highlight_Shapes_and_Lines(img, List_Contours):

    # A list to return Flowchart Shapes ONLY
    Shapes_Contours = []

    # Draw Thin Green line on the Flowchart Outline
    cv2.drawContours(img, List_Contours, 1, (0, 255, 0), 2)

    # Loop on all Contours List to Get the Flowchart Shapes ONLY and mark them with Think Red line
    for i in range(2, len(List_Contours)):
        if (cv2.contourArea(List_Contours[i]) / cv2.contourArea(List_Contours[1])) > 0.01:
            Shapes_Contours.append(List_Contours[i])
            cv2.drawContours(img, List_Contours, i, (255, 0, 0), 10)

    # Convert the list to a numpy array
    Shapes_Contours = np.array(Shapes_Contours)

    return img, Shapes_Contours


# Function to Search the entire image for the Flowchart Shape containing Start and Save the Contour Index Value of this Shape
def Get_Starting_Shape(img, Shapes_Contours):
    for i in range(0, len(Shapes_Contours)):
        if Contour_To_String(img, Shapes_Contours[i]) == "Start" or \
                Contour_To_String(img, Shapes_Contours[i]) == "start" or \
                Contour_To_String(img, Shapes_Contours[i]) == "begun":
            return i


# Function to extract the text from an Image
def Image_To_String(img):

    # Image Processing involving Threshold
    img = np.array(img, np.uint8)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    val, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Extract Text from image using pytesseract package
    custom_config = r'-l eng+por --psm 6'
    text = tess.image_to_string(Image.fromarray(binary), lang='eng', config=custom_config)

    return text


# Function to extract the text from an Input Contour
def Contour_To_String(img, Contour):
    Image_Copy = img.copy()
    Image_Copy = np.array(Image_Copy, np.uint8)

    # Color all the area outside the contour with white color
    fill_color = [255, 200, 255]
    mask_value = 255
    contours = [Contour]
    stencil = np.zeros(Image_Copy.shape[:-1]).astype(np.uint8)
    cv2.fillPoly(stencil, contours, mask_value)
    sel = stencil != mask_value
    Image_Copy[sel] = fill_color

    Image_Copy = Return_Image_with_Text_Only(Image_Copy)

    return Image_To_String(Image_Copy)


# Function to remove anything except Black Text from an Input Image
def Return_Image_with_Text_Only(img):

    # Detect the range of colors to be removed from the image
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    low = np.array([0, 0, 0])
    high = np.array([255, 255, 254])
    mask = cv2.inRange(hsv, low, high)
    img[mask <= 0] = (255, 255, 255)

    # Erode the text inside the image in order to make the text more thicker
    kernel = np.ones((3, 3), np.uint8)
    img_erosion = cv2.erode(img, kernel, iterations=1)

    return img_erosion


# Function to Search an Input Contour to find the point at which the arrow is emerging from the shape to the next shape
def Find_Emerging_Line(img, Contour, Contours_List):

    # Loop on all the points of the Contour to detect the point at which the line is emerging
    for point in Contour:
        y = point[0][0]
        x = point[0][1]
        Loop_Start_y = y - 9
        Loop_Start_x = x - 9

        # Counter to detect how many Green Pixels where detected
        Green_Count = 0

        # Loop on a region around the Contour Outline point to detect any green pixels
        for i in range(Loop_Start_y, Loop_Start_y + 19):
            for j in range(Loop_Start_x, Loop_Start_x + 19):
                if img[j, i, 1] == 255 and img[j, i, 0] == 0 and img[j, i, 2] == 0:
                    Green_Count = Green_Count + 1

                    if Green_Count >= 20:

                        # Mark this region by a green circle
                        Mark_By_Circle(img, i, j, "green", 20)

                        # Get the point at which the arrow starts first emerging from the Flowchart Outline
                        return Get_Index_From_Contour(Contours_List, x, y)


# Function to check whether the input Contour is a Rhombus or not
def Is_Rhombus(Contour):

    # Get the vertices of the Input Contour
    approx = cv2.approxPolyDP(Contour, 0.01 * cv2.arcLength(Contour, True), True)

    # Check if there are 4 vertices
    if len(approx) == 4:
        x, y, w, h = cv2.boundingRect(approx)

        # Check the Aspect Ratio of the (Width / Height) Calculation
        aspr = float(w) / h
        if 0.6 <= aspr <= 1.4:
            return True
        else:
            return False
    return False


# Function to draw a circle with variable diameter size and color on an Input Image for marking purposes
def Mark_By_Circle(img, x, y, color, rad):

    # Coordinates of the Circle Centre
    center_coordinates = (x, y)

    # Radius of the Circle
    radius = rad

    # Get the color required for the circle
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

    # Thickness of the Circle Outline
    thickness = -1

    # Draw the Circle
    cv2.circle(img, center_coordinates, radius, color, thickness)


# Function to Get the point at which the arrow starts first emerging from the shape
def Get_Index_From_Contour(Contour, x, y):

    # Variable to mark the index to return
    index = 0

    # Loop on the Flowchart Outline Points
    for point in Contour:
        a = point[0][0]
        b = point[0][1]
        if (y - 3) <= a <= (y + 3) and (x - 3) <= b <= (x + 3):
            return index
        else:
            index = index + 1


# Function to Get the index of the Contour representing the next Flowchart Shape connected to the Input Contour
def Index_Next_Contour(img, Index, Contour, List_Contours, Shape):

    # Check for any Condition Statement (Rhombus Shape)
    Check = False

    # Condition to return [Explained in details in main()]
    Condition = "Not Set"

    # Check if the Input Shape is a Rhombus
    if Is_Rhombus(Shape):
        Check = True

    # Variables to start the starting point of the arrow
    x_start = Contour[Index][0][0]
    y_start = Contour[Index][0][1]

    # Variables required for the For Loop to detect whether to increment or decrement in the List
    Start, End, Step = Start_End_Step(img, Index, Contour)

    # Variable to Check for (True / False) Statements
    itr = 0

    # Loop to move on the points of the arrow until it reaches to the next Flowchart Shape
    for point in range(Start, End, Step):
        x = Contour[point][0][0]
        y = Contour[point][0][1]

        # Scan the text written beside the arrow (True / False) in case it is a Conditional Statement
        if Check and (itr % 50) == 0:
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

        # Variable to stop iterating on the Flowchart Outline Points
        Stop = True

        Loop_Start_y = y - 6
        Loop_Start_x = x - 6
        for i in range(Loop_Start_x, Loop_Start_x + 13):
            for j in range(Loop_Start_y, Loop_Start_y + 13):
                if img[j, i, 1] == 255 and img[j, i, 0] == 0 and img[j, i, 2] == 0:
                    Stop = False

        # If the end of the arrow is reached i.e. the next shape in the Flowchart shapes is reached
        if Stop:
            # Mark this point by a bigger red circle
            Mark_By_Circle(img, x_start, y_start, "red", 25)

            # Again Mark the Starting point of the arrow by a red circle to check that it is done
            # As in Rhombus Shape there will be TWO scans on the Emerging Line (One for True and the other for the False)
            Mark_By_Circle(img, x, y, "red", 20)

            return Get_Contour_From_Point(List_Contours, x, y), Condition


# Function to Get the Contour Index from an Input Point present on the contour outline
def Get_Contour_From_Point(List_Contours, x, y):
    for i in range(2, len(List_Contours)):
        if cv2.pointPolygonTest(List_Contours[i], (x + 20, y), False) > 0 \
                or cv2.pointPolygonTest(List_Contours[i], (x, y + 20), False) > 0 \
                or cv2.pointPolygonTest(List_Contours[i], (x, y - 20), False) > 0 \
                or cv2.pointPolygonTest(List_Contours[i], (x - 20, y), False) > 0:
            return i


# Function to find whether to increment or decrement a list of points to move form one Flowchart Shape to Another
def Start_End_Step(img, Index, Contour):

    Index_A = Index
    Index_B = Index

    # Variable to detect whether to increment or decrement in the For Loop
    Step = 0

    while Step == 0:
        if (Index_A + 20) <= len(Contour):
            Index_A = Index_A + 20
        if (Index_B - 20) >= 0:
            Index_B = Index_B - 20

        # Get the Coordinates of 20 Points before the index and 20 Points after the index
        A_x = Contour[Index_A][0][0]
        A_y = Contour[Index_A][0][1]
        B_x = Contour[Index_B][0][0]
        B_y = Contour[Index_B][0][1]

        # According to Green and Red Color detect whether to increment or decrement in the For Loop
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

    # Input Parameter (Image Path) from the Terminal
    argv = sys.argv
    image_path = argv[1]

    # Read the Input Image using cv2
    Flowchart_Image = cv2.imread(image_path)

    # Execute the Image Processing Algorithm and output results in case of no errors
    try:

        # Get all Contours from the Input Image involving the Flowchart objects and the main Flowchart Figure
        # Sort those contours in descending order by their areas
        List_of_Sorted_Contours = Get_All_Contours_From_Image(Flowchart_Image)

        # Highlight the Flowchart Shapes by Red Color and Flowchart Arrows by Green Color
        # List_of_Shapes is a list used to hold the Flowchart Shapes ONLY and not [the arrows or the whole Flowchart Figure]
        Highlighted_Image, List_of_Shapes = Highlight_Shapes_and_Lines(Flowchart_Image, List_of_Sorted_Contours)

        # A List to store the order of the Flowchart instruction in chronological order
        To_Code = []

        '''
        A List to store:
            1) Bool in case the Flowchart Shape is a Rhombus
            2) True in index of the first True instruction in an if/else statement
            3) False in index of the first False instruction in an if/else statement
            4) Not Set in any other case
        '''
        Conditions = ["Not Set"]

        # Search the entire image for the Flowchart Shape containing Start and Save the Contour Index Value of this Shape
        Starting_Contour_Index = Get_Starting_Shape(Highlighted_Image, List_of_Shapes)

        # Raise an error in case the Input Image has no Starting Symbol
        if Starting_Contour_Index is None:
            print('Fail')
            print('Please represent a Starting Symbol in your Flowchart.')
            return

        # This variable represents the outline of the Flowchart i.e. the arrows connecting Flowchart Shapes
        Flowchart_Outerline = List_of_Sorted_Contours[1]

        # Push the Text in the Starting Symbol to To_Code list
        To_Code.append(Contour_To_String(Highlighted_Image, List_of_Shapes[Starting_Contour_Index]))

        # Search the Starting Shape Contour to find the point at which the arrow is emerging from the shape to the next shape
        Index_Follow = Find_Emerging_Line(Highlighted_Image, List_of_Shapes[Starting_Contour_Index], Flowchart_Outerline)

        # Get the index of the Contour representing the next Flowchart Shape connected to the starting symbol
        # State is a variable usd to store the elements of Conditions List as mentioned before
        Get_Index, State = Index_Next_Contour(Highlighted_Image, Index_Follow, Flowchart_Outerline, List_of_Sorted_Contours, List_of_Shapes[Starting_Contour_Index])

        # Push the Text in this Contour to To_Code list
        To_Code.append(Contour_To_String(Highlighted_Image, List_of_Sorted_Contours[Get_Index]))

        # Push the State to Conditions list
        Conditions.append(State)

        # This variable will be used later to detect whether there is a Rhombus Shape in the Input Image at all or no
        # If this variable is < 0 then there is no Rhombus Shape in the Input Image at all
        Conditional_Index = -1

        # Loop for all the Flowchart Shapes remaining in the image
        for i in range(len(List_of_Shapes) - 2):

            # Get the index of the Contour in case its shape was a Rhombus
            if Is_Rhombus(List_of_Sorted_Contours[Get_Index]):
                Conditional_Index = Get_Index

            # In case there was a Rhombus Shape in the Input Image and the current Shape was the End Symbol
            if Conditional_Index > 0 and (Contour_To_String(Highlighted_Image, List_of_Sorted_Contours[Get_Index]) == "End" or
                                          Contour_To_String(Highlighted_Image, List_of_Sorted_Contours[Get_Index]) == "Ena" or
                                          Contour_To_String(Highlighted_Image, List_of_Sorted_Contours[Get_Index]) == "Gud"):
                # Let the Next Contour Index to be processed is the index of the Rhombus Shape
                # This is done to go for the next if/else branch (either True or False) after completing the first branch
                Get_Index = Conditional_Index

            # Search the Current Contour to find the point at which the arrow is emerging from the shape to the next shape
            Index_Follow = Find_Emerging_Line(Highlighted_Image, List_of_Sorted_Contours[Get_Index], Flowchart_Outerline)

            # Get the index of the Contour representing the next Flowchart Shape connected to the Current Contour
            # State is a variable usd to store the elements of Conditions List as mentioned before
            Get_Index, State = Index_Next_Contour(Highlighted_Image, Index_Follow, Flowchart_Outerline, List_of_Sorted_Contours, List_of_Sorted_Contours[Get_Index])

            # Push the Text in the Current Contour to To_Code list
            To_Code.append(Contour_To_String(Highlighted_Image, List_of_Sorted_Contours[Get_Index]))

            # If the Current Contour is a Rhombus, push the string "Bool" to the Conditions list
            if Is_Rhombus(List_of_Sorted_Contours[Get_Index]):
                State = "Bool"

            # Push the State to Conditions list
            Conditions.append(State)

        # Raise an error in case the True and False branches are not clarified
        for item in range(0, len(Conditions)):
            if Conditions[item] == "Bool" and not (Conditions[item + 1] == "True" or Conditions[item + 1] == "False"):
                print('Fail')
                print('Please clarify the True and False labels on the conditional block branches.')
                return

        # Pass the list to the formatting() function to convert the List into a Python Code
        Code_Path = formatting(To_Code, Conditions)

        if len(To_Code) <= 1:
            print('Fail')
            print('Please insert a reliable Flowchart.')
            return

        # Pass the results to the GUI
        print('Success')
        print(Code_Path)

    # Raise an error in case the Input Image doesn't represent a reliable Flowchart
    except Exception:
        print('Fail')
        print('Please insert a reliable Flowchart.')


# Call the main function at the start of the program
if __name__ == "__main__":
    main()
