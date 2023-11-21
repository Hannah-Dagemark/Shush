from PIL import Image
from math import ceil
from Dicts import MORSE_DICT, ALPH_DICT
import os

print(MORSE_DICT["A"])

class Func:
    
    def __init__(self,):
        if os.path.exists("error.txt"):
            os.remove("error.txt")
        self.errortext = open('error.txt', 'a')
        self.errortext.writelines("INITIATING\n")
        
    def output(self, string, mode):
        string = str(string)
        if mode == "T" or mode == "B": print(string)
        self.errortext = open('error.txt', 'a')
        if mode == "F" or mode == "B": self.errortext.writelines(string + "\n")
iof = Func()

class Main:
    
    def __init__(self):
        self.intro()
        
    def intro(self):
        self.choice_loop()
            
    def choice_loop(self):
        print("Choose operation:\nTitle: input\nConvert Image: convert\nRead Encrypted Image: read\nExit Program: exit\n")
        match input():
            case "convert":
                print("Welcome to the Shush Converter\nPlease enter the name of your image, including the extension")
                self.path_img = "./input/" + input()
                print("Please enter the name of text file, including the extension")
                self.path_txt = "./input/" + input()
                print("Current path is: " + self.path_img + " and: " + self.path_txt)
                self.converter = Converter(self.path_img, self.path_txt)
                self.converter.run()
            case "read":
                print("Welcome to the Shush Reader\nPlease enter the name of your image, including the extension")
                self.path_img = "./input/" + input()
                self.reader = Reader(self.path_img)
                self.reader.run()
            case "exit":
                exit()
            case _:
                print("Invalid Input. Please make sure you spelled correctly, and used lower case letters thoughout.")
        


class Converter:
    
    def run(self):
        self.loadObjects()
        self.convertFunction()
        
    def __init__(self, image_path, text_path):
        self.img_path = image_path
        self.txt_path = text_path
        self.morse_text = ""
        self.img = Image.open(self.img_path).convert("RGB")
    
    def loadObjects(self):
        self.imagewidth, self.imageheight = self.img.size
        with open(self.txt_path) as x:
            self.raw_text = x.readlines()
            iof.output(self.raw_text, "B")
        for line in self.raw_text:
            for letter in line:
                self.morse_text += (MORSE_DICT[letter.upper()] + " ")
            iof.output(self.morse_text, "B")
        
    def convertFunction(self):
        incrementer,x,y = 0,0,0
        for letter in self.morse_text:
            incrementer += 1
            if x < self.imagewidth - 1:
                x += 1
            else:
                y += 1
                x = 0
            match letter:
                case ".":
                    self.img.putpixel((x,y), (0, 0, 0))
                case "-":
                    self.img.putpixel((x,y), (255, 255, 255))
                case " ":
                    continue
                case "|":
                    continue
            iof.output(str(incrementer/len(self.morse_text)*100) + "%", "F")
        self.img.save("converted_image.png")

class Reader:
    def run(self):
        self.loadObjects()
        self.readFunction()
        self.out = open('output/text.txt', 'a')
        self.out.writelines(self.normal_text)

    def __init__(self, image_path):
        self.img_path = image_path
        self.normal_text = ""
        self.morse_text = ""
        
    def loadObjects(self):
        self.img = Image.open(self.img_path).convert("RGB")
        self.imagewidth, self.imageheight = self.img.size
        
    def readFunction(self):
        escaperange = 0
        ended = False
        for y in range(self.imageheight):
            for x in range(self.imagewidth):
                if not ended == True:
                    iof.output("At pixel: " + str(x) + "," + str(y) + "\nWith color: " + str(self.img.getpixel((x,y))), "F")
                    
                    match self.img.getpixel((x,y)):
                        case (0,0,0):
                            iof.output("Found black", "B")
                            self.morse_text += "."
                        case (255,255,255):
                            iof.output("Found white", "B")
                            self.morse_text += "-"
                        case _:
                            if escaperange == 0:
                                ii = self.futurecheck(x,y)
                                if ii == 2:
                                    escaperange = 2
                                    self.morse_text += " | "
                                elif ii == 1:
                                    self.morse_text += " "
                                else:
                                    ended = True
                                    iof.output("Ended at: " + str(x) + "," + str(y), "B")
                            else:
                                escaperange -= 1
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
        iof.output(self.normal_text, "F")
                
                            
    def futurecheck(self,x,y):
        endchecker = 0
        a = 0
        b = 0
        while a + b <= 10:
            if x + a < self.imagewidth:
                if self.img.getpixel((x + a, y)) != (0,0,0) and self.img.getpixel((x + a, y)) != (255,255,255):
                    endchecker += 1
                    iof.output("Endchecker at: " + str(endchecker) + "\nUsing pixel: " + str(self.img.getpixel((x + a, y))) + "\nAt position: " + str(x+a) + "," + str(y), "F")
                    a += 1
                else:
                    a = 11
            else:
                if self.img.getpixel((b, y + 1)) != (0,0,0) and self.img.getpixel((b, y + 1)) != (255,255,255):
                    endchecker += 1
                    iof.output("Endchecker at: " + str(endchecker) + "\nUsing pixel: " + str(self.img.getpixel((b, y + 1))) + "\nAt position: " + str(b) + "," + str(y+1), "F")
                    b += 1
                else:
                    b = 11
                
        if endchecker > 9:
            return 10
        if x + 2 <= self.imagewidth:
            iof.output("Using one-line space checking method", "F")
            if self.img.getpixel((x + 1, y)) != (0,0,0) and self.img.getpixel((x + 1, y)) != (255,255,255):
                iof.output("Adding space", "F")
                return 2
            else:
                iof.output("Adding letter separation", "F")
                return 1
        else:
            if self.img.getpixel((0, y+1)) != (0,0,0) and self.img.getpixel((0, y+1)) != (255,255,255):
                iof.output("Adding space", "F")
                return 2
            else:
                iof.output("Adding letter separation", "F")
                return 1
    
    
Starter = Main()
Starter.intro()