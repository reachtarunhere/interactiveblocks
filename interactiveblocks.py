from ipythonblocks import Block, BlockGrid
from IPython.display import HTML, display, clear_output
import time
import __main__

_TDCustom = ('<td title="{0}" style="width: {1}px; height: {1}px;'
       'background-color: {2};" href="#" onclick="alert()"></td>')
_TABLE = ('<style type="text/css">'
          'table.blockgrid {{border: none;}}'
          ' .blockgrid tr {{border: none;}}'
          ' .blockgrid td {{padding: 0px;}}'
          ' #blocks{0} td {{border: {1}px solid white;}}'
          '</style>'
          '<table id="blocks{0}" class="blockgrid"><tbody>{2}</tbody></table>')
_TR = '<tr>{0}</tr>'
_TD = ('<td title="{0}" style="width: {1}px; height: {1}px;'
       'background-color: {2};" data-grid_name="GRID_NAME" data-coordinates="{3},{4}" onclick="click_block(this)"></td>')
_RGB = 'rgb({0}, {1}, {2})'
_TITLE = 'Index: [{0}, {1}]&#10;Color: ({2}, {3}, {4})'

_SINGLE_ITEM = 'single item'
_SINGLE_ROW = 'single row'
_ROW_SLICE = 'row slice'
_DOUBLE_SLICE = 'double slice'

_SMALLEST_BLOCK = 1

_POST_URL = 'http://ipythonblocks.org/post'
_GET_URL_PUBLIC = 'http://ipythonblocks.org/get/{0}'
_GET_URL_SECRET = 'http://ipythonblocks.org/get/secret/{0}'
_JS_MAGIC = '''
<script type="text/Javascript">
    var latest_output_area ="NONE"; // Jquery object for the DOM element of output area which was used most recently
    function handle_output(out, block){
        var output = out.content.data["text/html"];
        latest_output_area.html(output);
    }
    function click_block(block){
        latest_output_area = $(block).parents('.output_subarea');
        var grid_object_name = block.dataset.grid_name;
        var coordinates = block.dataset.coordinates;
        var command = grid_object_name + ".handle_interaction_block((" + coordinates + "))";
        console.log("Executing Command: " + command);
        var kernel = IPython.notebook.kernel;
        var callbacks = { 'iopub' : {'output' : handle_output}};
        kernel.execute(command,callbacks);
    }

</script>
'''

class CustomBlock(Block):
    @property
    def _td(self):
        """
        The HTML for a table cell with the background color of this Block.

        """
        title = _TITLE.format(self._row, self._col,
                              self._red, self._green, self._blue)
        rgb = _RGB.format(self._red, self._green, self._blue)
        return _TD.format(title, self._size, rgb, self._row, self._col)

class CustomGrid(BlockGrid):
        def _initialize_grid(self, fill):
            grid = [[CustomBlock(*fill, size=self._block_size)
                    for col in range(self.width)]
                    for row in range(self.height)]

            self._grid = grid

class Thing(object):

    """This represents any physical object that can appear in an Environment.
    You subclass Thing to get the things you want.  Each thing can have a
    .__name__  slot (used for output only)."""

    def __repr__(self):
        return '<{}>'.format(getattr(self, '__name__',
                                     self.__class__.__name__))

    def is_alive(self):
        "Things that are 'alive' should return true."
        return hasattr(self, 'alive') and self.alive

    def show_state(self):
        "Display the agent's internal state.  Subclasses should override."
        print("I don't know how to show_state.")

    def display(self, canvas, x, y, width, height):
        # Do we need this?
        "Display an image of this Thing on the canvas."
        pass

class GridWorld:
    ''' Heavily borrows ideas from AIMA code's Environment class'''

    def __init__(self, width=10, height=10, fill = (0,0,0), block_size = 25):
        self.time = time.time(),
        self.things = []
        self.grid = CustomGrid(width, height, fill=fill, block_size=block_size)

    def object_name(self):
        globals_in_main = {x:getattr(__main__,x) for x in dir(__main__)}
        # g = locals()
        for x in globals_in_main:
            if isinstance(globals_in_main[x], type(self)):
                if globals_in_main[x].time == self.time:
                    return x

    def move_to(self, thing, destination):
        "Move a thing to a new location."
        # Do in future
        return NotImplementedError

    def list_things_at(self, location, tclass=Thing):
        "Return all things exactly at a given location."
        # Do in future
        return NotImplementedError

    def some_things_at(self, location, tclass=Thing):
        """Return true if at least one of the things at location
        is an instance of class tclass (or a subclass)."""
        # Do in future
        return NotImplementedError

    def add_thing(self, thing, location=None):
        """Add a thing to the environment, setting its location. For
        convenience, if thing is an agent program we make a new agent
        for it. (Shouldn't need to override this."""
        # Do in future
        return NotImplementedError

    def delete_thing(self, thing):
        """Remove a thing from the environment."""
        # Do in future
        return NotImplementedError

    def handle_interaction_block(self, coordinates):
        ''' This method needs to be overriden to handle clicks on the grid.'''
        clicked_block = self.grid[coordinates[0],coordinates[1]]
        return self.show()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 

    def handle_interaction_thing(self, coordinates, thing_type, thing_name, interaction_type):
        ''' Note in case of drag coordinates represents final coordinates. '''
        return NotImplementedError

    def show(self):
        # add js
        # customize replace name of class
        grid_html = self.grid._repr_html_()
        grid_html = grid_html.replace("GRID_NAME",str(self.object_name()))
        total_html = grid_html + _JS_MAGIC
        clear_output(wait=True)
        display(HTML(total_html))

    def total_code(self):
        # add js
        # customize replace name of class
        grid_html = self.grid._repr_html_()
        grid_html = grid_html.replace("GRID_NAME",str(self.object_name()))
        total_html = grid_html + _JS_MAGIC
        return total_html
        # get html from them

    def update_loop(self):
      for i in range(10):
          time.sleep(1)
          clear_output(wait=True)
          display(HTML('<b> Hello  ' + str(i) + '</b>'))