from PIL import Image
from dicts import MORSE_DICT, ALPH_DICT
import os

print(MORSE_DICT["A"])

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
        self.choice_loop()
            
    def choice_loop(self):
        match input("Choose operation:\nTitle: input\nConvert Image: convert\nRead Encrypted Image: read\nExit Program: exit\n"):
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
        
    def __init__(self, image_path, text_path):
        self.img_path = image_path
        self.txt_path = text_path
        self.morse_text = ""
        self.img = Image.open(self.img_path).convert("RGBA")
        
    def run(self):
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
        self.img.save(f"output/{input('Please put your Image\'s output name: ')}.png")

class Reader:
    
    def __init__(self, image_path):
        self.img_path = image_path
        self.normal_text = ""
        self.morse_text = ""
    
    def run(self):
        self.load_objects()
        self.read_function()
        self.ender_function()
        self.out = open('output/text.txt', 'a')
        self.out.writelines(self.normal_text)
            
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
    
if __name__ == "__main__":
    Starter = Main()
    iof.close()