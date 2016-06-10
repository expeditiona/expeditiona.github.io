import PIL
import matplotlib.pyplot as plt # single use of plt is commented out
import os.path  
import PIL.ImageDraw            
# gitscrubs
def collage(border_width, border_color, directory=None):
    '''border_width is an integer, in pixels
       border_color is either a 3-tuple or a string representing a color, e.g. "black" or "red"
    '''
    #three_dimensions = [[],[],[]]
    if directory == None:
        directory = os.getcwd()
    try:
        border_width/=2 #if border_width isn't a number, will get a TypeError...
        border_width*=2
    except TypeError:
        border_width = 20 #... and border_width will be set to default of 20
    
    image_list, all_file_list = get_images();  # MAKE SURE IT'S IN THE SAME PLACE AS THE PICS
                                                # also we probably won't even need all_file_list
    
    four_images = []
    
    if len(image_list) == 0:
        return "fail"
    elif len(image_list) == 1:
        four_images = [[[border_width,border_width],[1000-border_width,1000-border_width]]]
    elif len(image_list) == 2:
        four_images =  [[[border_width,border_width],[1000-border_width,500-border_width/2]],
                        [[border_width,500+border_width/2],[1000-border_width,1000-border_width]]]
    elif len(image_list) == 3:
        four_images =  [[[border_width,border_width],[1000-border_width,500-border_width/2]],
                        [[border_width,500+border_width/2],[500-border_width/2,1000-border_width]],
                        [[500+border_width/2,500+border_width/2],[1000-border_width,1000-border_width]]]
    elif len(image_list) == 4:
        four_images = [[[border_width,600+border_width/2],[600-border_width/2,1000-border_width]],
                       [[600+border_width/2,border_width],[1000-border_width,300-border_width/2]],
                       [[border_width,border_width],[600-border_width/2,600-border_width/2]],
                       [[600+border_width/2,300+border_width/2],[1000-border_width,1000-border_width]]]
                       #top left, bottom right corners for 4 rectangles
                       #four_images[a] identifies which rectangle. a ranges from 0 to 3
                       #four_images[a][b] identifies which corner. b is 0 or 1
                       #four_images[a][b][c] identifies x or y coordinate. c is 0 or 1
                       #ascending aspect ratio order
    elif len(image_list) == 5:
        four_images =  [[[400+border_width/2,border_width],[1000-border_width,400-border_width/2]],
                        [[border_width,600+border_width/2],[600-border_width/2,1000-border_width]],
                        [[400+border_width/2,400+border_width/2],[600-border_width/2,600-border_width/2]],
                        [[border_width,border_width],[400-border_width/2,600-border_width/2]],
                        [[600+border_width/2,400+border_width/2],[1000-border_width,1000-border_width]]]
    else:
        return "lel"
    
    #bubble sort algo; sorts images in image_list by aspect ratio, ascending, with aspect ratio = height/width, so long ones are last                                            
    for i in range(len(image_list)):
        for j in range(len(image_list)-1-i):
            if float(image_list[j].size[1])/float(image_list[j].size[0]) > float(image_list[j+1].size[1])/float(image_list[j+1].size[0]):
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
    new_img_list = []
    for img in image_list:
        if float(img.size[1])/float(img.size[0]) > sorted_frame_ratios[i]:   #if img taller than frame                     
            base_height = four_images[i][1][1] - four_images[i][0][1]
            #img = PIL.Image.open(img)
            percent = (float(base_height) / float(img.size[1]))
            wsize = int((float(img.size[0]) * float(percent)))
            img = img.resize((wsize, base_height), PIL.Image.ANTIALIAS)
        else:
            base_width = four_images[i][1][0] - four_images[i][0][0]
            #img = PIL.Image.open(img)
            percent = (float(base_width) / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(percent)))
            img = img.resize((base_width, hsize), PIL.Image.ANTIALIAS)
        new_img_list.append(img)
        i+=1
    
    #aligns images with corners    
    x_offset,y_offset = 0,0
    if len(image_list) == 1:
        if float(new_img_list[0].size[1])/float(new_img_list[0].size[0]) > sorted_frame_ratios[0]:
            x_offset, y_offset = [((four_images[0][1][0]-four_images[0][0][0]) - (new_img_list[0].size[0]))/2], [0]
        else:
            x_offset, y_offset = [0], [((four_images[0][1][1]-four_images[0][0][1]) - (image_list[0].size[1]))/2]
    
    elif len(image_list) == 2:
        x_offset = [((four_images[0][1][0]-four_images[0][0][0]) - (new_img_list[0].size[0]))/2,
                              ((four_images[1][1][0]-four_images[1][0][0]) - (new_img_list[1].size[0]))/2]
        y_offset = [((four_images[0][1][1]-four_images[0][0][1]) - (new_img_list[0].size[1]))/2,
                               ((four_images[1][1][1]-four_images[1][0][1]) - (new_img_list[1].size[1]))/2]
    elif len(image_list) == 3:
        x_offset = [((four_images[2][1][0]-four_images[2][0][0])-(new_img_list[2].size[0]))/2,0,(four_images[2][1][0]-four_images[2][0][0])-(new_img_list[2].size[0])]
        y_offset = [((four_images[2][1][1]-four_images[2][0][1])-(new_img_list[2].size[1]))/2,(four_images[2][1][1]-four_images[2][0][1])-(new_img_list[2].size[1]),(four_images[2][1][1]-four_images[2][0][1])-(new_img_list[2].size[1])]
    elif len(image_list) == 4:
        x_offset = [0,(four_images[1][1][0]-four_images[1][0][0])-(new_img_list[1].size[0]),0,(four_images[3][1][0]-four_images[3][0][0])-(new_img_list[3].size[0])]
        y_offset = [(four_images[0][1][1]-four_images[0][0][1])-(new_img_list[0].size[1]),0,0,(four_images[3][1][1]-four_images[3][0][1])-(new_img_list[3].size[1])]
    elif len(image_list) == 5:
        x_offset = [(four_images[0][1][0]-four_images[0][0][0])-(new_img_list[0].size[0]),0,((four_images[2][1][0]-four_images[2][0][0])-(new_img_list[2].size[0]))/2,0,(four_images[4][1][0]-four_images[4][0][0])-(new_img_list[4].size[0])]
        y_offset = [0,(four_images[1][1][1]-four_images[1][0][1])-(new_img_list[1].size[1]),((four_images[2][1][1]-four_images[2][0][1])-(new_img_list[2].size[1]))/2,0,(four_images[4][1][1]-four_images[4][0][1])-(new_img_list[4].size[1])]
    
    '''image_sizes = [] #sizes of images
    for image in image_list:
        image_sizes.append(image.size)
        
        #center_width1 = ((four_images[0][1][0]-four_images[0][0][0]) - (new_img_list[0].size[0]))/2
        center_width1 = (((four_images[0][1][0]-four_images[0][0][0]) - (new_img_list[0].size[0]))/2)+(four_images[0][1][0]-four_images[0][0][0])
        center_height1 = ((four_images[0][1][1]-four_images[0][0][1]) - (new_img_list[0].size[1]))/2
            
        center_width2 = ((four_images[1][1][0]-four_images[1][0][0]) - (new_img_list[1].size[0]))/2
        center_height2 = ((four_images[1][1][1]-four_images[1][0][1]) - (new_img_list[1].size[1]))/2
            
        center_width3 = ((four_images[2][1][0]-four_images[2][0][0]) - (new_img_list[2].size[0]))/2
        center_height3 = ((four_images[2][1][1]-four_images[2][0][1]) - (new_img_list[2].size[1]))/2
            
        center_width4 = ((four_images[3][1][0]-four_images[3][0][0]) - (new_img_list[3].size[0]))/2
        center_height4 = ((four_images[3][1][1]-four_images[3][0][1]) - (new_img_list[3].size[1]))/2
            
        #print "frame is " + str(four_images[0][1][0]-four_images[0][0][0])
        #print "image is " + str(image_list[0].size[0])
        #print "center is " + str(center_width1)
        #    
        #print "frame is " + str(four_images[0][1][1]-four_images[0][0][1])
        #print "image is " + str(image_list[0].size[1])
        #print "center is " + str(center_height1)

        print "Frame0 " + str(frame_sizes[0][0]) + "," + str(frame_sizes[0][1])
        print "Image0 " + str(new_img_list[0].size[0]) + "," + str(new_img_list[0].size[1])
        print "Frame1 " + str(frame_sizes[1][0]) + "," + str(frame_sizes[1][1])
        print "Image1 " + str(new_img_list[1].size[0]) + "," + str(new_img_list[1].size[1])
        print "Frame2 " + str(frame_sizes[2][0]) + "," + str(frame_sizes[2][1])
        print "Image2 " + str(new_img_list[2].size[0]) + "," + str(new_img_list[2].size[1])
        print "Frame3 " + str(frame_sizes[3][0]) + "," + str(frame_sizes[3][1])
        print "Image3 " + str(new_img_list[3].size[0]) + "," + str(new_img_list[3].size[1])'''
    
    try:
        im_initial = PIL.Image.new('RGB',(1000,1100),border_color) #if border_color isn't a valid color...
    except ValueError:
        im_initial = PIL.Image.new('RGB',(1000,1000),(0,0,0))  #...set border color to default of black 
    print im_initial
    
    for i in range(len(new_img_list)):
        im_initial.paste(new_img_list[i],(four_images[i][0][0]+x_offset[i],four_images[i][0][1]+y_offset[i]))
        
    #im.paste(famlogo.jpg   , (coordinates))
        
    new_directory = os.path.join(directory, 'modified')
    os.mkdir(new_directory)
    new_image = os.path.join(new_directory, 'final.png')
    im_initial.save(new_image)
    
    #UP NEXT:
    #Create new image object (initially all black, or whatever color you want for borders) that will 
    #actually serve as the new image
    #Create mask; draw 4 rectangles corresponding to resized image sizes. area inside frames is TRANSPARENT, NOT OPAQUE
    #Put mask onto the all black image object, this will turn the insides of the frames white
    #(ie where we want to paste the images, those places will be white)
    #Paste resized images into the frames and voila :D 

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
    logo = []
    
    directory_list = os.listdir(directory) # Get list of files
    for entry in directory_list:
        absolute_filename = os.path.join(directory, entry)
        try:
            image = PIL.Image.open(absolute_filename)
            file_list += [entry]
            if entry != 'famlogo.png':
                image_list += [image]
            else:
                image = image
        except IOError:
            pass # do nothing with errors tying to open non-images
    return image_list, file_list