#! /usr/bin/env python
"""
Dummy extension for Inkscape for experimentation
"""
import inkex

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
        with(open('C:/Users/Owner/Desktop/debug.txt','w')) as _:
            _.write('Number: %d' % count)

# Create effect instance and apply it.
DUMMY_EXTENSION = DummyExtension()
DUMMY_EXTENSION.affect()
