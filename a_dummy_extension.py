#! /usr/bin/env python
"""
Dummy extension for Inkscape for experimentation
"""
import os
import inkex
import subprocess
import imageio
from simplestyle import *
from lxml import etree

'''os.environ["TCL_LIBRARY"] = os.path.join(os.getcwd(), "..\\..\\lib\\python2.7\\tcl\\tcl8.5")
os.environ["TK_LIBRARY"] = os.path.join(os.getcwd(), "..\\..\\lib\\python2.7\\tcl\\tk8.5")

from Tkinter import Tk, Label, Button

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")

        self.label = Label(master, text="This is our first GUI!")
        self.label.pack()

        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def greet(self):
        print("Greetings!")

root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()'''

SVG_FILE = "C:\\Users\\Owner\\Desktop\\ball.svg"
GIF_FILE = "C:\\Users\\Owner\\Desktop\\ball.gif"
PREFIX = "C:\\Users\\Owner\\Desktop\\Output\\"
INKSCAPE_LABEL_TAG = "{http://www.inkscape.org/namespaces/inkscape}label"
ANIMATION_LAYER_PREFIX = "Animation Layer "
LAYER_TAG = "{http://www.w3.org/2000/svg}g"

class DummyExtension(inkex.Effect):
    """
    Main class for extension
    """
    def __init__(self):
        # Call the base class constructor.
        inkex.Effect.__init__(self)

        self.OptionParser.add_option(
            '--count', action='store', type='int',
            dest='count', default=25, help='Dividers (Length axis)')

    def log(self, message):
        with(open('C:/Users/Owner/Desktop/debug.txt', 'w')) as _:
            _.write(message)

    def effect(self):
        count = self.options.count

        # Get access to main SVG document element and get its dimensions.
        root = self.document.getroot()
        children = root.getchildren()

        layers = {}

        for i in range(0, len(children)):
            if children[i].tag != LAYER_TAG:
                    continue

            label = children[i].get(INKSCAPE_LABEL_TAG)
            if ANIMATION_LAYER_PREFIX in label:
                layerNumber = label[len(ANIMATION_LAYER_PREFIX):]
                layers[layerNumber] = i
            
        '''
        Create a png for each layers
        where all the other layers' SVG info is removed
        ''' 
        animationFramePNGs = {}
        # For each animation frame,
        # remove all layers ('g' tags) that aren't 
        # for the current animation frame (i),
        # Save as a PNG image,
        # Store list of all outputted frame PNGs
        
        for frame in range(1, len(layers.keys())+1):
            #Copy root tree
            rootCopy = root.__copy__()

            # Remove SVG for children that are layers and
            # are not the current frame 
            childrenToRemove = []
            for childIndex in range(0, len(rootCopy.getchildren())):
                child = rootCopy.getchildren()[childIndex]

                # If it is a layer
                if child.tag == LAYER_TAG:
                    # And it is NOT the current frame's layer
                    if child != rootCopy.getchildren()[layers[str(frame)]]:
                        childrenToRemove.append(rootCopy.getchildren()[childIndex])

            for child in childrenToRemove:
                rootCopy.remove(child)

            svg_filepath = "%sFrame%s.svg" % (PREFIX, frame)
            png_filepath = "%sFrame%s.png" % (PREFIX, frame)            

            svg_xml = etree.tostring(rootCopy)
            
            self.saveSVG(svg_xml, svg_filepath)
            self.convertSVGtoPNG(svg_filepath, png_filepath)

            animationFramePNGs[frame] = png_filepath

        imageFrames = []
        for frame in animationFramePNGs:
            filepath = animationFramePNGs[frame]
            imageFrames.append(imageio.imread(filepath))
        
        
        imageio.mimsave(GIF_FILE, imageFrames)
        

    def saveSVG(self, svg_xml, output_file):
        with open(output_file, 'w') as f:
            f.write(svg_xml)

    def convertSVGtoPNG(self, svg_file, output_file):
        #exe = "C:\\Program Files\\Inkscape\\inkscape.exe"
        exe = "inkscape"

        command = "%s -D -f \"%s\" -e \"%s\"" % (exe, svg_file, output_file)

        p = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        
        return_code = p.wait()
        f = p.stdout
        err = p.stderr

# Create effect instance and apply it.
DUMMY_EXTENSION = DummyExtension()
DUMMY_EXTENSION.affect()
