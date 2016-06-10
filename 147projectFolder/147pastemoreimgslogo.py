import PIL
import matplotlib.pyplot as plt # single use of plt is commented out
import os.path  
import PIL.ImageDraw
import PIL.ImageFont 
import textwrap        
# gitscrubs
def collage(border_width, border_color, text, text_color, directory=None):
    '''border_width- in pixels; is an integer
       border_color- either RGB 3-tuple or a string representing a color, e.g. "black" or "red"
       text- any string
       text_color- RGB 3-tuple
    '''
    #finds directory
    if directory == None:
        directory = os.getcwd()
    
    #wraps text string so it all can fit in the final collage
    #if text isn't a string, assign it the value of "" (empty string)
    wrapped = []
    if text != "":
        try:
            wrapped = textwrap.wrap(text,28)
        except AttributeError:
            text = ""
    
    #sets border width in pixels. if it's a valid number the math under try: will do nothing, otherwise sets it to 20    
    try:
        border_width/=2 #if border_width isn't a number, will get a TypeError...
        border_width*=2
    except TypeError:
        border_width = 20 
    
    #gets images and puts them in image_list.
    image_list = get_images(); 
    
    #defines dimensions of frames of design based on # of images found, max 6
    #top left, bottom right corners for 4 rectangles
            #layout[a] identifies which rectangle. a ranges from 0 to (# of images - 1)
            #layout[a][b] identifies which corner. b is 0 or 1; 0 is top left, 1 is bottom right
            #layout[a][b][c] identifies x or y coordinate. c is 0 or 1; 0 is x, 1 is y
            #ascending aspect ratio order
    layout = [] 
    if len(image_list) == 0:
        return "I got nothing to work off of fam! Please put images in the current working directory."
    elif len(image_list) == 1:
        layout = [[[border_width,border_width],[1000-border_width,1000-border_width]]]
    elif len(image_list) == 2:
        layout =  [[[border_width,border_width],[1000-border_width,500-border_width/2]],
                        [[border_width,500+border_width/2],[1000-border_width,1000-border_width]]]
    elif len(image_list) == 3:
        layout =  [[[border_width,border_width],[1000-border_width,500-border_width/2]],
                        [[border_width,500+border_width/2],[500-border_width/2,1000-border_width]],
                        [[500+border_width/2,500+border_width/2],[1000-border_width,1000-border_width]]]
    elif len(image_list) == 4:
        layout = [[[border_width,600+border_width/2],[600-border_width/2,1000-border_width]],
                       [[600+border_width/2,border_width],[1000-border_width,300-border_width/2]],
                       [[border_width,border_width],[600-border_width/2,600-border_width/2]],
                       [[600+border_width/2,300+border_width/2],[1000-border_width,1000-border_width]]]
    elif len(image_list) == 5:
        layout =  [[[400+border_width/2,border_width],[1000-border_width,400-border_width/2]],
                        [[border_width,600+border_width/2],[600-border_width/2,1000-border_width]],
                        [[400+border_width/2,400+border_width/2],[600-border_width/2,600-border_width/2]],
                        [[border_width,border_width],[400-border_width/2,600-border_width/2]],
                        [[600+border_width/2,400+border_width/2],[1000-border_width,1000-border_width]]]
    elif len(image_list) == 6:
        layout = [[[border_width,border_width],[700-border_width/2,400-border_width/2]],
                       [[400+border_width/2,800+border_width/2],[750-border_width/2,1000-border_width]],
                       [[400+border_width/2,400+border_width/2],[1000-border_width,800-border_width/2]],
                       [[750+border_width/2,800+border_width/2],[1000-border_width,1000-border_width]],
                       [[700+border_width/2,border_width],[1000-border_width,400-border_width/2]],
                       [[border_width,400+border_width/2],[400-border_width/2,1000-border_width]]]
    else:
        return "TMI (too many images)"
    
    #bubble sort algo; sorts images in image_list by aspect ratio, ascending, with aspect ratio = height/width, so tall images are last                                            
    for i in range(len(image_list)):
        for j in range(len(image_list)-1-i):
            if float(image_list[j].size[1])/float(image_list[j].size[0]) > float(image_list[j+1].size[1])/float(image_list[j+1].size[0]):
                image_list[j], image_list[j+1] = image_list[j+1], image_list[j]
    
    #collects frame sizes
    frame_sizes = [] 
    for frame in layout:
        frame_sizes.append((frame[1][0]-frame[0][0],frame[1][1]-frame[0][1])) # x, y dimensions of frames
    
    #creates sorted aspect ratio list of the frames. used to compare to image aspect ratios to determine
    #what to resize to
    sorted_frame_ratios = []
    for size in frame_sizes:
        sorted_frame_ratios.append(float(size[1])/float(size[0]))
    
    #this loop resizes images to fit frames of design
    i=0
    new_img_list = []
    for img in image_list:
        if float(img.size[1])/float(img.size[0]) > sorted_frame_ratios[i]:   #if img taller than frame                     
            base_height = layout[i][1][1] - layout[i][0][1]
            percent = (float(base_height) / float(img.size[1]))
            wsize = int((float(img.size[0]) * float(percent)))
            img = img.resize((wsize, base_height), PIL.Image.ANTIALIAS)
        else:
            base_width = layout[i][1][0] - layout[i][0][0]
            percent = (float(base_width) / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(percent)))
            img = img.resize((base_width, hsize), PIL.Image.ANTIALIAS)
        new_img_list.append(img)
        i+=1
    
    #assigns x and y offset values that will be used to make the images line up with the edges of the collage   
    x_offset,y_offset = 0,0
    if len(image_list) == 1:
        if float(new_img_list[0].size[1])/float(new_img_list[0].size[0]) > sorted_frame_ratios[0]:
            x_offset, y_offset = [((layout[0][1][0]-layout[0][0][0]) - (new_img_list[0].size[0]))/2], [0]
        else:
            x_offset, y_offset = [0], [((layout[0][1][1]-layout[0][0][1]) - (image_list[0].size[1]))/2]
    
    elif len(image_list) == 2:
        x_offset = [((layout[0][1][0]-layout[0][0][0]) - (new_img_list[0].size[0]))/2,
                              ((layout[1][1][0]-layout[1][0][0]) - (new_img_list[1].size[0]))/2]
        y_offset = [((layout[0][1][1]-layout[0][0][1]) - (new_img_list[0].size[1]))/2,
                               ((layout[1][1][1]-layout[1][0][1]) - (new_img_list[1].size[1]))/2]
    elif len(image_list) == 3:
        x_offset = [((layout[0][1][0]-layout[0][0][0])-(new_img_list[0].size[0]))/2,0,(layout[2][1][0]-layout[2][0][0])-(new_img_list[2].size[0])]
        y_offset = [((layout[0][1][1]-layout[0][0][1])-(new_img_list[0].size[1]))/2,(layout[1][1][1]-layout[1][0][1])-(new_img_list[1].size[1]),(layout[2][1][1]-layout[2][0][1])-(new_img_list[2].size[1])]
    elif len(image_list) == 4:
        x_offset = [0,(layout[1][1][0]-layout[1][0][0])-(new_img_list[1].size[0]),0,(layout[3][1][0]-layout[3][0][0])-(new_img_list[3].size[0])]
        y_offset = [(layout[0][1][1]-layout[0][0][1])-(new_img_list[0].size[1]),0,0,(layout[3][1][1]-layout[3][0][1])-(new_img_list[3].size[1])]
    elif len(image_list) == 5:
        x_offset = [(layout[0][1][0]-layout[0][0][0])-(new_img_list[0].size[0]),0,((layout[2][1][0]-layout[2][0][0])-(new_img_list[2].size[0]))/2,0,(layout[4][1][0]-layout[4][0][0])-(new_img_list[4].size[0])]
        y_offset = [0,(layout[1][1][1]-layout[1][0][1])-(new_img_list[1].size[1]),((layout[2][1][1]-layout[2][0][1])-(new_img_list[2].size[1]))/2,0,(layout[4][1][1]-layout[4][0][1])-(new_img_list[4].size[1])]
    elif len(image_list) == 6:
        x_offset = [0,((layout[1][1][0]-layout[1][0][0])-(new_img_list[1].size[0]))/2,(layout[2][1][0]-layout[2][0][0])-(new_img_list[2].size[0]),(layout[3][1][0]-layout[3][0][0])-(new_img_list[3].size[0]),(layout[4][1][0]-layout[4][0][0])-(new_img_list[4].size[0]),0]
        y_offset = [0,(layout[1][1][1]-layout[1][0][1])-(new_img_list[1].size[1]),((layout[2][1][1]-layout[2][0][1])-(new_img_list[2].size[1]))/2,(layout[3][1][1]-layout[3][0][1])-(new_img_list[3].size[1]),0,(layout[4][1][1]-layout[4][0][1])-(new_img_list[4].size[1])]
    
    #intializes final image object
    try:
        im_initial = PIL.Image.new('RGB',(1000,1000+(len(wrapped)*100)),border_color) #if border_color isn't a valid color...
    except ValueError:
        im_initial = PIL.Image.new('RGB',(1000,1000+(len(wrapped)*100)),(0,0,0))  #...set border color to default of black 
        border_color = "black"
    #pastes in images
    for i in range(len(new_img_list)):
        im_initial.paste(new_img_list[i],(layout[i][0][0]+x_offset[i],layout[i][0][1]+y_offset[i]))

    #pastes words below collage
    font = PIL.ImageFont.truetype("ostrich-regular.ttf",100)
    #if text != "":
    for line in wrapped:
        words = PIL.Image.new("RGB",(1000,100),border_color)
        draw = PIL.ImageDraw.Draw(words)
        w,h = draw.textsize(line, font=font)
        try:
            draw.text(((1000-w)/2,0),line,text_color,font=font)       #if text_color not valid color...
        except ValueError:
            draw.text(((1000-w)/2,0),line,(255,255,255),font=font)      #... set it to white
        im_initial.paste(words,(0,1000+(100*wrapped.index(line))))
    
    #puts final image, called final.png, in folder called 'final' that's a subfolder of working directory
    new_directory = os.path.join(directory, 'final')
    os.mkdir(new_directory)
    new_image = os.path.join(new_directory, 'final.png')
    im_initial.save(new_image)

#taken from PLTW Activity 1.4.5, removed file_list
def get_images(directory=None):
    """ Returns PIL.Image objects for all the images in directory.
    
    If directory is not specified, uses current directory.
    Returns a 2-tuple containing 
    a list with a  PIL.Image object for each image file in root_directory, and
    a list with a string filename for each image file in root_directory
    """
    
    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
        
    image_list = [] # Initialize aggregator
    
    directory_list = os.listdir(directory) # Get list of files
    for entry in directory_list:
        absolute_filename = os.path.join(directory, entry)
        try:
            image = PIL.Image.open(absolute_filename)
            image_list += [image]
        except IOError:
            pass # do nothing with errors tying to open non-images
    return image_list