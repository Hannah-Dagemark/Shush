<<<<<<< Updated upstream:main.py
from PIL import Image
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import sv_ttk
=======
import tkinter
import PIL
>>>>>>> Stashed changes:Main/main.py
import os
import time
from PIL import Image
from tkinter import filedialog
from dicts import MORSE_DICT, ALPH_DICT


MORSE_DICT = { 'A':'.-', 'B':'-...',
               'C':'-.-.', 'D':'-..', 'E':'.',
               'F':'..-.', 'G':'--.', 'H':'....',
               'I':'..', 'J':'.---', 'K':'-.-',
               'L':'.-..', 'M':'--', 'N':'-.',
               'O':'---', 'P':'.--.', 'Q':'--.-',
               'R':'.-.', 'S':'...', 'T':'-',
               'U':'..-', 'V':'...-', 'W':'.--',
               'X':'-..-', 'Y':'-.--', 'Z':'--..',
               '1':'.----', '2':'..---', '3':'...--',
               '4':'....-', '5':'.....', '6':'-....',
               '7':'--...', '8':'---..', '9':'----.',
               '0':'-----', ',':'--..--', '.':'.-.-.-',
               '?':'..--..', '/':'-..-.', '-':'-....-',
               '(':'-.--.', ')':'-.--.-', ' ': '|',
               '\n': '.-.-.-.'}
ALPH_DICT = {v: k for k, v in MORSE_DICT.items()}

#window
window = tk.Tk()
window.title('Shush')
window.geometry('700x400')
#window.configure(background='gray60')

entryImg = tk.StringVar()
entryImg.set("Path/To/Image")
entryTxt = tk.StringVar()
entryTxt.set("Path/To/Text/file")


readImg = tk.StringVar()
readImg.set("Path/To/Image")
errorTxt = tk.StringVar()

class Func:
    
    def __init__(self):
        if os.path.exists("error.txt"):
            os.remove("error.txt")
        self.errortext = open('error.txt', 'a')
        self.errortext.write("INITIATING\n")
        
    def output(self, string, mode):
        string = str(string)
        if mode == "T" or mode == "B": print(string)
        if mode == "F" or mode == "B": self.errortext.writelines(string + "\n")
    
    def close(self):
        self.errortext.close()
        
iof = Func()

class Main:
    
    def __init__(self):
        #self.choice_loop()
        self.something = 0
            
    def choice_loop(self):
        match input("Choose operation:\n\"Title\": \"input\"\nConvert Image: convert\nRead Encrypted Image: read\nExit Program: exit\n"):
            case "convert":
                print("Welcome to the Shush Converter\nPlease select your image file in the popup explorer window.")
                time.sleep(2)
                self.path_img = tkinter.filedialog.askopenfilename()
                print("Please select your text file in the popup explorer window.")
                time.sleep(2)
                self.path_txt = tkinter.filedialog.askopenfilename()
                print("Current path is: " + self.path_img + "\nand: " + self.path_txt)
                self.converter = Converter(self.path_img, self.path_txt)
                self.converter.run()
            case "read":
                print("Welcome to the Shush Reader\nPlease select your image file in the popup explorer window.")
                self.path_img = tkinter.filedialog.askopenfilename()
                self.reader = Reader(self.path_img)
                self.reader.run()
            case "exit":
                exit()
            case _:
                print("Invalid Input. Please make sure you spelled correctly, and used lower case letters thoughout.")

class Converter:        
    def __init__(self):
        self.morse_text = ""
        
    def add_img_path(self):
        image_path = filedialog.askopenfilename(initialdir="..", title="Select Your Image File")
        if str(image_path.split(".")[1]) == "png" or str(image_path.split(".")[1]) == "jpg" or str(image_path.split(".")[1]) == "jpeg":
            self.img_path = image_path
            entryImg.set(str(image_path))
            if errorTxt.get() == "Error loading Image file path":
                errorTxt.set("")
        else:
            errorTxt.set("Error loading Image file path")
        
    def add_text_path(self):
        text_path = filedialog.askopenfilename(initialdir="..", title="Select Your Text File")
        if str(text_path.split(".")[1]) == "txt":
            self.txt_path = text_path
            entryTxt.set(str(text_path))
            if errorTxt.get() == "Error loading Text file path":
                errorTxt.set("")
        else:
            errorTxt.set("Error loading Text file path")
    
    def add_output_path(self):
        woo = 0
        
    def run(self):
        self.img = Image.open(self.img_path).convert("RGBA")
        self.load_objects()
        self.convert_function()
    
    def load_objects(self):
        self.imagewidth, self.imageheight = self.img.size
        with open(self.txt_path) as x:
            self.raw_text = x.readlines()
            iof.output(self.raw_text, "B")
        for line in self.raw_text:
            self.morse_text += " ".join(MORSE_DICT[letter.upper()] for letter in line) + " "
            iof.output(self.morse_text, "B")
    def convert_function(self):
        x, y = 0, 0
        for incrementer, letter in enumerate(self.morse_text):
            if x < self.imagewidth - 1:
                x += 1
            else:
                y += 1
                x = 0
            self.R, self.G, self.B, _ = self.img.getpixel((x,y))
            match letter:
                case ".":
                    self.img.putpixel((x,y), (self.R, self.G, self.B, 254))
                case "-":
                    self.img.putpixel((x,y), (self.R, self.G, self.B, 253))
                case " ":
                    continue
                case "|":
                    continue
            iof.output(f"{self.img.getpixel((x,y))}", "F")
            iof.output(f"{incrementer/len(self.morse_text)*100}%", "F")
        filename = ""
        while filename == "":
            filename = filedialog.asksaveasfilename(filetypes = (('JPEG', ('*.jpg','*.jpeg','*.jpe','*.jfif')),('PNG', '*.png'),('BMP', ('*.bmp','*.jdib')),('GIF', '*.gif')), defaultextension=".png")
            if filename.split('.')[1] != "png":
                filename = ""
                errorTxt.set("Wrong filetype! Needs to be .png")
        print(filename)
        self.img.save(filename)
        errorTxt.set("")

class Reader:
    
    def __init__(self):
        self.normal_text = ""
        self.morse_text = ""
    
    def add_img_path(self):
        image_path = filedialog.askopenfilename(initialdir="..", title="Select Your Image File")
        if str(image_path.split(".")[1]) == "png":
            self.img_path = image_path
            readImg.set(str(image_path))
            if errorTxt.get() == "Error loading Image file path":
                errorTxt.set("")
        else:
            errorTxt.set("Error loading Image file path")
    
    def run(self):
        self.load_objects()
        self.read_function()
        self.ender_function()
            
    def load_objects(self):
        self.img = Image.open(self.img_path).convert("RGBA")
        self.imagewidth, self.imageheight = self.img.size
        
    def read_function(self):
        escaperange = 0
        for y in range(self.imageheight):
            for x in range(self.imagewidth):
                iof.output(f"At pixel: {x},{y}\nWith color: {self.img.getpixel((x,y))}", "F")
                match self.img.getpixel((x,y))[3]:
                    case 254:
                        iof.output("Found .", "B")
                        self.morse_text += "."
                    case 253:
                        iof.output("Found -", "B")
                        self.morse_text += "-"
                    case _:
                        if escaperange == 0:
                            ii = self.future_check(x,y)
                            if ii == 2:
                                escaperange = 2
                                self.morse_text += " | "
                            elif ii == 1:
                                self.morse_text += " "
                            else:
                                iof.output(f"Ended at: {x},{y}", "B")
                                return
                        else:
                            escaperange -= 1
    
    def ender_function(self):
        iof.output(self.morse_text, "B")
        sequence = ""
        for letter in self.morse_text:
            if letter != " ":
                sequence += letter
            else:
                if letter == "|":
                    self.normal_text += " "
                elif letter == " " and sequence != "":
                    self.normal_text += ALPH_DICT[sequence]
                    sequence = ""
        iof.output(self.normal_text, "B")
        
        filename = ""
        while filename == "":
            filename = filedialog.asksaveasfilename(filetypes = (('text files', '*.txt'),), defaultextension=".txt")
            if filename.split('.')[1] != "txt":
                filename = ""
                errorTxt.set("Wrong filetype! Needs to be .txt")
        print(filename)
        errorTxt.set("")
        
        self.out = open(str(filename), 'w')
        self.out.writelines(self.normal_text)
        self.out.close()
                
                            
    def future_check(self,x,y):
        endchecker = 0
        a = 0
        b = 0
        while a + b <= 10:
            if x + a < self.imagewidth:
                if self.img.getpixel((x + a, y))[3] == 255:
                    endchecker += 1
                    iof.output(f"Endchecker at: {endchecker}\nUsing pixel: {self.img.getpixel((x + a, y))}\nAt position: {x+a},{y}", "F")
                    a += 1
                else:
                    a = 11
            else:
                if self.img.getpixel((b, y + 1))[3] == 255:
                    endchecker += 1
                    iof.output(f"Endchecker at: {endchecker}\nUsing pixel: {self.img.getpixel((b, y + 1))}\nAt position: {b},{y+1}", "F")
                    b += 1
                else:
                    b = 11
                
        if endchecker > 9:
            return 10
        if x + 2 <= self.imagewidth:
            iof.output("Using one-line space checking method", "F")
            if self.img.getpixel((x + 1, y))[3] == 255:
                iof.output("Adding space", "F")
                return 2
            else:
                iof.output("Adding letter separation", "F")
                return 1
        else:
            if self.img.getpixel((0, y+1))[3] == 255:
                iof.output("Adding space", "F")
                return 2
            else:
                iof.output("Adding letter separation", "F")
                return 1

starter = Main()
convert = Converter()
read = Reader()



#title
title_label = ttk.Label(master = window, text = "Shush, The Text-Image encryption tool", font = 'Times_New_Roman 24 italic')
error_label = ttk.Label(master=window, text="yea", font="Times_New_Roman 18 bold", textvariable = errorTxt)
title_label.pack()

#style

#style = ttk.Style()

#style.configure('BW.TLabel', foreground="gray90", background="gray50")

#input field

main_frame = ttk.Frame(master = window)
top_frame = ttk.Frame(master=main_frame)
read_frame = ttk.Frame(master = main_frame)
read_img_frame = ttk.Frame(master = read_frame)
convert_frame = ttk.Frame(master = main_frame)
img_frame = ttk.Frame(master = convert_frame)
txt_frame = ttk.Frame(master = convert_frame)

convertButton = ttk.Button(master = top_frame, text = "Encrypt Text Into Image", command = convert.run)
convertButtonImg = ttk.Button(master = img_frame, text = "Add Image Path", command = convert.add_img_path)
convertButtonTxt = ttk.Button(master = txt_frame, text = "Add Text Path", command = convert.add_text_path)
convertImgLabel = ttk.Label(master = img_frame, text = "Image Filepath", font = "Times_New_Roman 8", textvariable = entryImg)
convertTxtLabel = ttk.Label(master = txt_frame, text = "Text Filepath", font = "Times_New_Roman 8", textvariable = entryTxt)

readButton = ttk.Button(master = top_frame, text = "Decrypt Text From Image", command = read.run)
readButtonImg = ttk.Button(master = read_img_frame, text = "Add Image Path", command = read.add_img_path)
readImgLabel = ttk.Label(master = read_img_frame, text = "Image Filepath", font = "Times_New_Roman 8", textvariable = readImg)

error_label.pack()

convertButton.pack(side = "left", padx=30)
convertButtonImg.pack(side = "left")
convertImgLabel.pack(side = "right")
convertButtonTxt.pack(side = "left")
convertTxtLabel.pack(side = "right")

readButton.pack(side = "right")
readButtonImg.pack(side = "left")
readImgLabel.pack(side = "right")

main_frame.pack(pady = 10)
top_frame.pack()
read_frame.pack(side = "right")
read_img_frame.pack()
convert_frame.pack(side = "left")
img_frame.pack()
txt_frame.pack()

sv_ttk.set_theme("dark")

#run
window.mainloop()