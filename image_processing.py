
import cv2
import numpy as np

def process_grid(image_path, grid_size):
    img = cv2.imread(image_path)
    if img.all() == None:
        raise ValueError("File path does not lead to an image")

    # grayscale then binary (black and white) so contours can be found (only takes binary images)
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY_INV)

    # contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise ValueError("No grid detected")
    x,y,w,h = cv2.boundingRect(max(contours, key=cv2.contourArea)) # x and y are the top left corner of the square, w and h are the width an heigt of the square, which would be the same
    
    # crop grid and split grid into a set of equal sized tiles
    cropped = img[y:y+h, x:x+w]
    tile_height = h // grid_size
    tile_width = w // grid_size

    tiles = {} # stores (x,y):color pairs as to allow the creation of a 2D array in the other file

    for i in range(grid_size):
        for j in range(grid_size):
            tile =  cropped[
                i * tile_height : (i+1) * tile_height,
                j * tile_width : (j+1) * tile_width
            ]


            # Zooms in on each tile to isolate color such that the range of colors is thinner. Prevents tiles from containing bits of color from other tiles
            h, w = tile.shape[:2]
            margin_h, margin_w = int(h*0.1), int(w*0.1)
            enhanced_tile = tile[margin_h:h-margin_h, margin_w:w-margin_w]

            dominant_color = tuple(np.mean(enhanced_tile, axis=(0,1)).astype(int))
            tiles[(i,j)] = dominant_color
    return tiles


# takes two rbg values (ex. [150, 199, 255]), rgb_val being the value we are checking with and comparison being what we are checking against. This only checks one rgb value to another, so I need to use this iteratively
def similar(rgb_val, comparison):
    return all(abs(rgb_val[i] - comparison[i]) < 20 for i in range(3))

# Want to build a 2D array using the rgb values and storing them in a dictionary with a letter assigned to them as a value. These will be used later for returning an char grid to work in the other file as input
def build_2Darray(tile_dict, grid_size):
    chars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    count = 0
    new_2Darray = []
    letter_pairs = {}
    for i in range(grid_size):
        temp = []
        for j in range(grid_size):
            current_rgb = tile_dict[(i,j)]
            assigned_char = None

            #checking if rgb already in letter_pairs
            for rgb in letter_pairs:
                if similar(current_rgb, rgb):
                    assigned_char = letter_pairs[rgb]
                    break
            
            # if current_rgb doesn't have any similar rgb values in letter_pairs, make a new char for this new rgb value
            if assigned_char is None:
                assigned_char = chars[count]
                letter_pairs[current_rgb] = assigned_char
                count += 1
            
            temp.append(assigned_char)
        new_2Darray.append(temp)
    
    return new_2Darray, [chars[i] for i in range(count)]

if __name__ == "__main__":
    t = process_grid("queens1.png", 9)
    build_2Darray(t, 9)