import PIL
import matplotlib.pyplot as plt # single use of plt is commented out
import os.path  
import PIL.ImageDraw            
# gitscrubs
def collage(border_width, border_color):
    #three_dimensions = [[],[],[]]
    try:
        border_width/=2 #if border_width isn't a number, will get a TypeError...
        border_width*=2
    except TypeError:
        border_width = 20 #... and border_width will be set to default of 20
                       
    four_images = [[[border_width,600+border_width/2],[600-border_width/2,1000-border_width]],
                       [[600+border_width/2,border_width],[1000-border_width,300-border_width/2]],
                       [[border_width,border_width],[600-border_width/2,600-border_width/2]],
                       [[600+border_width/2,300+border_width/2],[1000-border_width,1000-border_width]]]
                       #top left, bottom right corners for 4 rectangles
                       #four_images[a] identifies which rectangle. a ranges from 0 to 3
                       #four_images[a][b] identifies which corner. b is 0 or 1
                       #four_images[a][b][c] identifies x or y coordinate. c is 0 or 1
                       #ascending aspect ratio order
    
    image_list, all_file_list = get_images();  # MAKE SURE IT'S IN THE SAME PLACE AS THE PICS
                                                # also we probably won't even need all_file_list
    
    #bubble sort algo; sorts images in image_list by aspect ratio, ascending, with aspect ratio = height/width, so long ones are last                                            
    for i in range(len(image_list)):
        for j in range(len(image_list)-1-i):
            if float(image_list[j].size[1])/float(image_list[j].size[0]) < float(image_list[j+1].size[1])/float(image_list[j+1].size[0]):
                image_list[j], image_list[j+1] = image_list[j+1], image_list[j]
    
    frame_sizes = [] #sizes of frames defined by collage design
    for frame in four_images:
        frame_sizes.append((frame[1][0]-frame[0][0],frame[1][1]-frame[0][1])) # x, y dimensions of frames
    #print frame_sizes
    #print float(frame_sizes[3][1])/float(frame_sizes[3][0]) #LOL REMEMBER TO FLOAT STUFF
    
    frame_ratios = []
    for size in frame_sizes:
        frame_ratios.append(float(size[1])/float(size[0]))
    sorted_frame_ratios=sorted(frame_ratios)
    
    #this loop resizes images to fit frames of design
    i=0
    for img in image_list:
        if float(img.size[1])/float(img.size[0]) > sorted_frame_ratios[i]:                        
            base_height = four_images[i][1][1] - four_images[i][0][1]
            #img = PIL.Image.open(img)
            percent = (float(base_height) / float(img.size[0]))
            wsize = int((float(img.size[0]) * float(percent)))
            img = img.resize((base_height, wsize), PIL.Image.ANTIALIAS)
        else:
            base_width = four_images[i][1][0] - four_images[i][0][0]
            #img = PIL.Image.open(img)
            percent = (float(base_width) / float(img.size[1]))
            hsize = int((float(img.size[1]) * float(percent)))
            img = img.resize((base_width, hsize), PIL.Image.ANTIALIAS)
        i+=1
    
    try:
        im_initial = PIL.Image.new('RGB',(1000,1000),border_color) #if border_color isn't a valid color...
    except ValueError:
        im_initial = PIL.Image.new('RGB',(1000,1000),(0,0,0))  #...set border color to default of black 
    print im_initial
    
    for img in image_list:
        
    
    #UP NEXT:
    #Create new image object (initially all black, or whatever color you want for borders) that will 
    #actually serve as the new image
    #Create mask; draw 4 rectangles corresponding to resized image sizes. area inside frames is TRANSPARENT, NOT OPAQUE
    #Put mask onto the all black image object, this will turn the insides of the frames white
    #(ie where we want to paste the images, those places will be white)
    #Paste resized images into the frames and voila :D

    '''image_sizes = [] #sizes of images
    for image in image_list:
        image_sizes.append(image.size)
    
    frame_sizes = [] #sizes of frames defined by collage design
    for frame in four_images:
        frame_sizes.append((frame[1][0]-frame[0][0],frame[1][1]-frame[0][1])) # x, y dimensions of frames
    #print frame_sizes
    #print float(frame_sizes[3][1])/float(frame_sizes[3][0]) #LOL REMEMBER TO FLOAT STUFF
    
    frame_ratios = []
    for size in frame_sizes:
        frame_ratios.append(float(size[1])/float(size[0]))
    sorted_frame_ratios=sorted(frame_ratios)
    print sorted_frame_ratios
    
    image_ratios = []
    for size in image_sizes:
        image_ratios.append(float(size[1])/float(size[0]))
    sorted_img_ratios = sorted(image_ratios)
    print image_ratios
    print sorted_img_ratios
    
    ratio_placement = []
    for sir in sorted_img_ratios:
        ratio_placement.append(sir)
        
    mask = PIL.Image.new('RGBA', (width, height), (255,255,255,255))
    drawing_layer = PIL.ImageDraw.Draw(mask)
    #rectangles
    drawing_layer.polygon([(0,height),(width-radius,0),
                            (width-radius,height),(radius,height)],
                            fill=(127,0,127,255))     '''   











def round_corners(original_image, percent_of_side):
    """ Rounds the corner of a PIL.Image
    
    original_image must be a PIL.Image
    Returns a new PIL.Image with rounded corners, where
    0 < percent_of_side < 1
    is the corner radius as a portion of the shorter dimension of original_image
    """
    #set the radius of the rounded corners
    width, height = original_image.size
    radius = int(percent_of_side * min(width, height)) # radius in pixels
    
    ###
    #create a mask
    ###
    
    #start with transparent mask
    rounded_mask = PIL.Image.new('RGBA', (width, height), (127,0,127,0))
    drawing_layer = PIL.ImageDraw.Draw(rounded_mask)
    
    # Overwrite the RGBA values with A=255.
    # The 127 for RGB values was used merely for visualizing the mask
    
    # Draw two rectangles to fill interior with opaqueness
    drawing_layer.polygon([(radius,0),(width-radius,0),
                            (width-radius,height),(radius,height)],
                            fill=(127,0,127,255))
    drawing_layer.polygon([(0,radius),(width,radius),
                            (width,height-radius),(0,height-radius)],
                            fill=(127,0,127,255))

    #Draw four filled circles of opaqueness
    drawing_layer.ellipse((0,0, 2*radius, 2*radius), 
                            fill=(0,127,127,255)) #top left
    drawing_layer.ellipse((width-2*radius, 0, width,2*radius), 
                            fill=(0,127,127,255)) #top right
    drawing_layer.ellipse((0,height-2*radius,  2*radius,height), 
                            fill=(0,127,127,255)) #bottom left
    drawing_layer.ellipse((width-2*radius, height-2*radius, width, height), 
                            fill=(0,127,127,255)) #bottom right
                         
    # Uncomment the following line to show the mask
    # plt.imshow(rounded_mask)
    
    # Make the new image, starting with all transparent
    result = PIL.Image.new('RGBA', original_image.size, (0,0,0,0))
    result.paste(original_image, (0,0), mask=rounded_mask)
    return result
    
def get_images(directory=None):
    """ Returns PIL.Image objects for all the images in directory.
    
    If directory is not specified, uses current directory.
    Returns a 2-tuple containing 
    a list with a  PIL.Image object for each image file in root_directory, and
    a list with a string filename for each image file in root_directory
    """
    
    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
        
    image_list = [] # Initialize aggregaotrs
    file_list = []
    
    directory_list = os.listdir(directory) # Get list of files
    for entry in directory_list:
        absolute_filename = os.path.join(directory, entry)
        try:
            image = PIL.Image.open(absolute_filename)
            file_list += [entry]
            image_list += [image]
        except IOError:
            pass # do nothing with errors tying to open non-images
    return image_list, file_list

def round_corners_of_all_images(directory=None):
    """ Saves a modfied version of each image in directory.
    
    Uses current directory if no directory is specified. 
    Places images in subdirectory 'modified', creating it if it does not exist.
    New image files are of type PNG and have transparent rounded corners.
    """
    
    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
        
    # Create a new directory 'modified'
    new_directory = os.path.join(directory, 'modified')
    try:
        os.mkdir(new_directory)
    except OSError:
        pass # if the directory already exists, proceed  
    
    #load all the images
    image_list, file_list = get_images(directory)  

    #go through the images and save modified versions
    for n in range(len(image_list)):
        # Parse the filename
        filename, filetype = file_list[n].split('.')
        
        # Round the corners with radius = 30% of short side
        new_image = round_corners(image_list[n],.30)
        #save the altered image, suing PNG to retain transparency
        new_image_filename = os.path.join(new_directory, filename + '.png')
        new_image.save(new_image_filename)    