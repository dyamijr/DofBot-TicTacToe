import cv2
import numpy as np

# contour analysis
def recognize_x_o(cell):
    # Threshold the cell image to binary
    #_, binary = cv2.threshold(cell, 128, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours
    contours, _ = cv2.findContours(cell, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        # Approximate the contour shape
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        if len(approx) > 8:  # Circle-like contour (O)
            return "O"
        elif len(approx) == 4 or len(approx) > 4:  # Likely intersecting lines (X)
            return "X"
    return None
#template matching
def recognize_x_o_template(cell):
    # Load templates for X and O
    template_x = cv2.imread("template_x.jpg", 0)
    template_o = cv2.imread("template_o.jpg", 0)
    
    # Resize the cell to match the template size
    cell_resized = cv2.resize(cell, template_x.shape[::-1])
    
    # Match the cell with templates
    match_x = cv2.matchTemplate(cell_resized, template_x, cv2.TM_CCOEFF_NORMED)
    match_o = cv2.matchTemplate(cell_resized, template_o, cv2.TM_CCOEFF_NORMED)
    
    if cv2.minMaxLoc(match_x)[1] > cv2.minMaxLoc(match_o)[1]:
        return "X"
    else:
        return "O"
    
def recognize_x_o_base(cell):
    # Analyze the cell to determine if it's empty, X, or O
    # Example: Use contours or template matching
    contours, _ = cv2.findContours(cell, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        # Analyze contours to distinguish between X and O
        return "X" if some_logic() else "O"
    return None  # Empty cell


def preprocess_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # Apply edge detection
    edges = cv2.Canny(blurred, 50, 150)
    return edges

def find_largest_square(contours):
    largest_contour = None
    max_area = 0

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            # Approximate the contour to reduce number of points
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            if len(approx) == 4:  # Check if contour is a quadrilateral
                largest_contour = approx
                max_area = area

    return largest_contour

def extract_cells(grid_image):
    # Divide the grid into 9 cells (3x3)
    height, width = grid_image.shape[:2]
    cell_height = height // 3
    cell_width = width // 3

    cells = []
    for i in range(3):
        for j in range(3):
            x_start, y_start = j * cell_width, i * cell_height
            x_end, y_end = x_start + cell_width, y_start + cell_height
            cells.append(grid_image[y_start:y_end, x_start:x_end])

    return cells

# Load the image
image = cv2.imread("tictactoe.jpg")

# Preprocess the image
edges = preprocess_image(image)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Find the largest square (Tic Tac Toe grid)
largest_square = find_largest_square(contours)

if largest_square is not None:
    # Warp the perspective to get a straight grid
    points = largest_square.reshape(4, 2)
    rect = np.zeros((4, 2), dtype="float32")

    # Order the points for perspective transform
    s = points.sum(axis=1)
    rect[0] = points[np.argmin(s)]
    rect[2] = points[np.argmax(s)]

    diff = np.diff(points, axis=1)
    rect[1] = points[np.argmin(diff)]
    rect[3] = points[np.argmax(diff)]

    (tl, tr, br, bl) = rect
    width_a = np.linalg.norm(br - bl)
    width_b = np.linalg.norm(tr - tl)
    height_a = np.linalg.norm(tr - br)
    height_b = np.linalg.norm(tl - bl)

    max_width = max(int(width_a), int(width_b))
    max_height = max(int(height_a), int(height_b))

    dst = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]], dtype="float32")

    matrix = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, matrix, (max_width, max_height))

    # Split the grid into cells
    cells = extract_cells(cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY))

    # Analyze each cell
    board = []
    for cell in cells:
        content = recognize_x_o(cell)
        board.append(content if content else " ")

    print("Detected Board:")
    print(board[:3])
    print(board[3:6])
    print(board[6:])

    # Show the result
    cv2.imshow("Warped Grid", warped)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()
else:
    print("Tic Tac Toe grid not found.")
