from PIL import Image
import sys

# COMMAND-LINE FORMAT
# python3 imager.py {image_file(required)} {format:ascii(default),color} {width:40(default)}
# EX: python3 imager.py Dont.png ascii 50



# COLORS
BLACK = "\033[37;40m"
RED = "\033[37;41m"
GREEN = "\033[37;42m"
YELLOW = "\033[37;43m"
BLUE = "\033[37;44m"
PURPLE = "\033[37;45m"
CYAN = "\033[37;46m"
WHITE = "\033[37;47m"
RESET_COLOR = "\033[m"

# Display image as ASCII text in terminal
def ascii_show():
    # open image file
    im = Image.open(file)

    # adjust image scale
    size = im.size
    newsize = res_fac, int(size[1]/(size[0]/res_fac))
    im = im.resize(newsize)
    size = im.size

    # convert image to greyscale
    for y in range(size[1]):
        #print(round(y/size[1]*100,2), "%")
        for x in range(size[0]):
            pixel = x, y
            data = im.getpixel(pixel)
            # convert RBG values into single BW value
            avg = int(( data[0] + data[1] + data[2] )/3)
            data = (avg,avg,avg)
            im.putpixel(pixel, data)

    # display pixels based on light-level as symbols
    for y in range(size[1]):
        line = ""
        for x in range(size[0]):
            pixel = x, y
            data = im.getpixel(pixel)
            if data[0] < 35:
                line += "  "
            elif data[0] < 75:
                line += ". "
            elif data[0] < 100:
                line += "- "
            elif data[0] < 150:
                line += "= "
            elif data[0] <= 200:
                line += "# "
            elif data[0] <= 255:
                line += "@ "
        print(line)

# Display image as ASCII text with color background in terminal
def color_show():
    # open image file
    im = Image.open(file)

    # adjust image scale
    size = im.size
    newsize = res_fac, int(size[1]/(size[0]/res_fac))
    im = im.resize(newsize)
    size = im.size

    # display pixels based on color as blocks
    for y in range(size[1]):
        line = ""
        for x in range(size[0]):
            pixel = x, y
            data = im.getpixel(pixel)
            r = round(data[0],-1)
            g = round(data[1],-1)
            b = round(data[2],-1)
            v = round(data[0],-1) + round(data[1],-1) + round(data[2],-1) +1

            # determine color
            color = WHITE
            u_thresh = 55
            l_thresh = 35
            c_r = False
            c_g = False
            c_b = False

            if u_thresh >= round(r/v*100) >= l_thresh:
                c_r = True
            if u_thresh >= round(g/v*100) >= l_thresh:
                c_g = True
            if u_thresh >= round(b/v*100) >= l_thresh:
                c_b = True

            if c_r & c_g & c_b:
                color = WHITE
            elif c_r & ~c_g & ~c_b:
                color = RED
            elif ~c_r & c_g & ~c_b:
                color = GREEN
            elif ~c_r & ~c_g & c_b:
                color = BLUE
            elif c_r & c_g & ~c_b:
                color = YELLOW
            elif c_r & ~c_g & c_b:
                color = PURPLE
            elif ~c_r & c_g & c_b:
                color = CYAN
            else:
                color = BLACK

            # Determine symbol
            avg = int((data[0] + data[1] + data[2]) / 3)
            symbol = " "
            if avg < 35:
                symbol = "  "
            elif avg < 75:
                symbol = ". "
            elif avg < 100:
                symbol = "- "
            elif avg < 150:
                symbol = "= "
            elif avg <= 200:
                symbol = "# "
            elif avg <= 255:
                symbol = "@ "

            line += color + symbol

        print(line + RESET_COLOR)

if __name__ == "__main__":

    # Get command-line arguments
    try:
        file = sys.argv[1]
        disp_form = None
        res_fac = None

        try:
            # attempt getting display form arguement
            disp_form = sys.argv[2]
        except IndexError:
            disp_form = "ascii"

        try:
            # attempt getting size arguement
            res_fac = int(sys.argv[3])
        except IndexError:
            res_fac = 40

        # Display image based on form
        if disp_form == "ascii":
            ascii_show()
        elif disp_form == "color":
            color_show()
    except IndexError:
        print("Unrecognised parameter!\nUse format: python3 imager.py {image_file(required)} {format:ascii(default),color} {width:40(default)}")
    

    
