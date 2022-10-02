import tkinter as tk
from tkinter import filedialog
from skimage.transform import resize
import PIL.Image, PIL.ImageTk , PIL.ImageOps
import cv2
import numpy as np
import os

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        global screen_height
        global screen_width
        screen_width= self.winfo_screenwidth()
        screen_height= self.winfo_screenheight()
        self.title("Edwin Jaya's Photo Editor Very Free 1.0")
        self.initUI()
        print("Width : {} , Height : {}".format(screen_width,screen_height))
    
    def initUI(self):
        global editorFrame
        global photoFrame
        self.state("zoomed")
        mainPanel = tk.Frame(self,bg="Blue")
        mainPanel.pack(fill=tk.BOTH,expand=1)
        mainPanel.grid_rowconfigure(0, weight=1)
        mainPanel.grid_columnconfigure(1, weight=1)   
        editorFrame = tk.Frame(mainPanel,bg="#282a30",width=screen_width/2,height=screen_height)
        editorFrame.grid(row=0,column=1,sticky=tk.W)
        photoFrame = tk.Frame(mainPanel,bg="#2B2B2B",width=screen_width/2+250,height=screen_height)
        photoFrame.grid(row=0,column=2,sticky=tk.E)
        self.editorFrameUI()
        self.photoFrameUI()
    
    def photoFrameUI(self):
        global photoCanvas
        global addPicButton
        photoCanvas = tk.Canvas(photoFrame,height=600,width=600,bg="White",cursor="tcross")
        photoCanvas.place(relx=0.5,rely=0.5,anchor="center")
        addPicButton = tk.Button(photoFrame,text="Add Image",command=self.image_browse)
        addPicButton.place(relx=0.5,rely=0.5,anchor="center")

    
    def button_icon(self,path):
        icon=PIL.ImageTk.PhotoImage(PIL.Image.open(path).resize((45,45), PIL.Image.ANTIALIAS))
        
        return icon
    
    def create_button(self,frame,image,command,rely):
        button = tk.Button(frame,image=image, bg="#040405",borderwidth=0,command=command)
        button.image = image
        button.place(relx=0.5, rely=rely, anchor="center") 
    
        return button

    def editorFrameUI(self):
        global editorSetting
        editorFrame.grid_rowconfigure(0,weight=1)
        editorFrame.grid_columnconfigure(1,weight=1)
        editorBar = tk.Frame(editorFrame,bg="#040405",width=80,height=screen_height)
        editorBar.grid(row=0,column=1,sticky=tk.E)
        editorSetting = tk.Frame(editorFrame,bg="#2B2B2B",width=300,height=screen_height)
        editorSetting.grid(row=0,column=2,sticky=tk.W)

        # ! Brightness
        brightness_icon=self.button_icon('./images/brightness.png')
        self.create_button(editorBar,brightness_icon,self.create_brightness_editor,0.25)

        # ! Contrast
        contrast_icon=self.button_icon('./images/contrast.png')
        self.create_button(editorBar,contrast_icon,self.create_contrast_editor,0.35)

        # ! Color Filter
        color_icon=self.button_icon('./images/color.png')
        self.create_button(editorBar,color_icon,self.create_color_filter_editor,0.45)

        # ! Save Button
        save_icon=self.button_icon('./images/save.png')
        self.create_button(editorBar,save_icon,self.create_save_image,0.55)

    def image_browse(self):
        try:
            img_file=filedialog.askopenfilename(initialdir="/",title="Select An Image",filetypes=[("All files", "*.*")] )
            print(img_file)
            self.load_image(img_file)
            addPicButton.destroy()
        except Exception as e:
            print(e)            
        
        return img_file

    def load_image(self,img_file):
        global img
        global image_real_width
        global image_real_height 
        global image_real_color_channel
        try:
            img=cv2.cvtColor(cv2.imread(img_file), cv2.COLOR_RGB2BGR) 
            (image_real_width, image_real_height, image_real_color_channel) = img.shape
            print(img.shape)
            image_in_canvas_width = 600
            image_in_canvas_height = 600
            dimension=(image_in_canvas_width, image_in_canvas_height)
            img = cv2.resize(img, dimension)
            convert_image=self.convert_image_from_array(img)
            self.create_canvas_image(convert_image)
        except Exception as e:
            print(e)
        
        return convert_image

    def convert_image_from_array(self,image):
        converted_image=PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(image))
        print(type(converted_image))
        
        return converted_image
    
    def create_canvas_image(self,image):
        photoCanvas.create_image(0,0,image=image,anchor=tk.NW)
        photoCanvas.image=image

        return image
    
    def convert_image_to_uint(self,image):
        converted_uint_image=PIL.Image.fromarray((image * 255).astype(np.uint8))
        
        return converted_uint_image
    
    def saving_image(self,image,fileName):
        image.save(fileName)

        return image

    def get_save_image(self,image):
        try:
            image = resize(image, (image_real_width, image_real_height))
            print(image.shape)
            convert_image=self.convert_image_to_uint(image)
            self.saving_image(convert_image,"Result.png")
        except Exception as e:
            print(e)
        
        return convert_image
            
    def create_save_image(self):
        global new_img
        global img
        try:
            self.get_save_image(new_img)
            print("Save succeed")
        except:
            self.get_save_image(img)
            print("Save succeed")

    def update_image(self,image):
        try:
            image = resize(image, (image_real_width, image_real_height))
            print(image.shape)
            convert_image=self.convert_image_to_uint(image)
            self.saving_image(convert_image,"Testing.png")
            self.load_image("./Testing.png")
            print("Img updated!")
        except Exception as e:
            print(e)

        return
    
    def create_contrast_editor(self):
        global contrast_window
        global blend_contrast
        contrast_window=cv2.namedWindow("Contrast")
        cv2.createTrackbar("Contrast","Contrast",127,2*127,\
            self.contrast_trackbar)
        cv2.waitKey(0)
        self.update_image(blend_contrast)

        return

    def contrast_trackbar(self,contrast=0):
        global contrast_window
        contrast = cv2.getTrackbarPos("Contrast","Contrast")
        print("Contrast : {}".format(contrast))
        try:
            self.contrast_trackbar_controller(new_img,contrast)
        except:
            self.contrast_trackbar_controller(img,contrast)

    def contrast_trackbar_controller(self,img,contrast=127):
        global blend_contrast
        contrast = int((contrast - 0) * (127 - (-127)) / (254 - 0) + (-127))
        if contrast != 0:
            Alpha = float(131 * (contrast + 127)) / (127 * (131 - contrast))
            Gamma = 127 * (1 - Alpha)
            blend_contrast = cv2.addWeighted(img, Alpha,
                                img, 0, Gamma)
        else:
            blend_contrast = img
        show_changes_image_on_canvas=self.convert_image_from_array(blend_contrast)
        self.create_canvas_image(show_changes_image_on_canvas)
        self.update_idletasks()
        self.update()
        
        return blend_contrast

    def create_brightness_editor(self):
        global brightness_window
        global blend_brightness
        brightness_window=cv2.namedWindow("Brightness")
        cv2.createTrackbar("Brightness","Brightness",255,2*255,\
            self.brightness_trackbar)
        cv2.waitKey(0)
        self.update_image(blend_brightness)
        
        return
    
    def brightness_trackbar(self,brightness=0):
        global brightness_window
        brightness = cv2.getTrackbarPos("Brightness","Brightness")
        print("Brightness : {}".format(brightness))
        try:
            self.brightness_trackbar_controller(new_img,brightness)
        except:
            self.brightness_trackbar_controller(img,brightness)
    
    def brightness_trackbar_controller(self,img,brightness=255):
        global blend_brightness
        brightness = int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255))
        if brightness != 0:
            if brightness > 0:
                shadow = brightness
                max = 255
            else:
                shadow = 0
                max = 255 + brightness
            al_pha = (max - shadow) / 255
            ga_mma = shadow
            blend_brightness = cv2.addWeighted(img, al_pha,
                                img, 0, ga_mma)
        else:
            blend_brightness = img
        
        show_changes_image_on_canvas=self.convert_image_from_array(blend_brightness)
        self.create_canvas_image(show_changes_image_on_canvas)
        self.update_idletasks()
        self.update()
        
        return blend_brightness
    
    def create_color_filter_editor(self):
        global color_overlay
        global color_filter_blend
        global color_filter_window
        color_overlay = np.zeros((600, 600, 3),np.uint8)
        color_filter_window=cv2.namedWindow("Color Filter")
        cv2.createTrackbar("R","Color Filter",0,255,self.color_filter_trackbar)
        cv2.createTrackbar("G","Color Filter",0,255,self.color_filter_trackbar)
        cv2.createTrackbar("B","Color Filter",0,255,self.color_filter_trackbar)
        cv2.waitKey(0)
        self.update_image(color_filter_blend)

    def color_filter_trackbar(self,R=0,G=0,B=0):
        global color_filter_window
        R =cv2.getTrackbarPos("R","Color Filter")
        G =cv2.getTrackbarPos("G","Color Filter")
        B =cv2.getTrackbarPos("B","Color Filter")
        print("R : {}".format(R))
        print("G : {}".format(G))
        print("B : {}".format(B))
        try:
            self.color_control_trackbar_controller(new_img,B,G,R)
        except:
            self.color_control_trackbar_controller(img,B,G,R)
        
    def color_control_trackbar_controller(self,img,B,G,R):
        global color_filter_blend
        global color_overlay
        color_overlay[:]=[B,G,R]
        color_filter_blend=cv2.addWeighted(img,0.8,color_overlay,0.6,0)
        show_changes_image_on_canvas=self.convert_image_from_array(color_filter_blend)
        self.create_canvas_image(show_changes_image_on_canvas)
        self.update_idletasks()
        self.update()
        
        return color_filter_blend


if __name__ == "__main__":
    a = App()
    a.mainloop()
    try:
        os.remove("./Testing.png")
    except:
        pass