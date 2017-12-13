#! /usr/bin/env python
"""
Dummy extension for Inkscape for experimentation
"""
import os
import inkex
from simplestyle import *

os.environ["TCL_LIBRARY"] = os.path.join(os.getcwd(), "..\\..\\lib\\python2.7\\tcl\\tcl8.5")
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
root.mainloop()


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

    def effect(self):
        count = self.options.count
        
        with(open('C:/Users/Owner/Desktop/debug.txt', 'w')) as _:
            _.write('Number: %d\n' % count)

        # Get access to main SVG document element and get its dimensions.
        svg = self.document.getroot()

        # Get the attributes:
        width  = self.unittouu(svg.get('width'))
        height = self.unittouu(svg.attrib['height'])

        # Create a new layer.
        layer = inkex.etree.SubElement(svg, 'g')
        layer.set(inkex.addNS('label', 'inkscape'), 'newlayer')
        layer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')

        # Create an SVG text element
        text = inkex.etree.Element(inkex.addNS('text','svg'))
        text.text = 'Hello %s!' % (count)

        # Position text in center of document
        text.set('x', str(width / 2))
        text.set('y', str(height / 2))

        # Set 'text-align' property on text
        style = {'text-align' : 'center', 'text-anchor' : 'middle'}
        text.set('style', formatStyle(style))

        layer.append(text)

# Create effect instance and apply it.
DUMMY_EXTENSION = DummyExtension()
DUMMY_EXTENSION.affect()
