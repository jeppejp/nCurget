""" The module creates the different classes supported """

def create_widget(widget_spec, datasource):
    """ creates a widget class from a widget_spec"""
    widget = None
    if widget_spec['_type'].lower() == "string":
        widget = NString()
    if widget_spec['_type'].lower() == "progress":
        widget = NProgress()

    if widget is None:
        raise Exception("Unknown type: "+str(widget_spec['_type']))
    widget.set_from_spec(widget_spec)
    widget.set_datasource(datasource)

    return widget


class NWidget(object):
    """base widget"""
    def __init__(self):
        self.name = ""
        self.xpos = 0
        self.ypos = 0
        self.datasource = None
        self.data_key = None
        self.static_value = None
    def set_datasource(self, dsource):
        """ Set the data source pointer """
        self.datasource = dsource
    def get_value(self):
        """ Get the value based on either static or from the datasource """
        if self.static_value:
            return self.static_value
        if self.datasource is not None:
            return self.datasource.get_value(self.data_key)
    def set_base_from_spec(self, spec):
        """ set the base config for all widgets """
        self.xpos = spec['_xpos']
        self.ypos = spec['_ypos']
        self.name = spec['_name']
        if '_static' in spec:
            self.static_value = spec['_static']
        elif '_datasource' in spec:
            self.data_key = spec['_datasource']
        else:
            raise Exception("Specify either _static or _datasource for an entry")



class NString(NWidget):
    """basic string class"""
    def __init__(self):
        NWidget.__init__(self)
        self.value = ""
    def draw(self, stdscr):
        """draw the widget"""
        stdscr.addstr(self.ypos, self.xpos, str(self.get_value()))
    def set_from_spec(self, spec):
        """ update self based on spec """
        self.set_base_from_spec(spec)


class NProgress(NWidget):
    """ progress bar using pipes ||| """
    def __init__(self):
        NWidget.__init__(self)
        self.width = 0
        self.value = 0
    def set_from_spec(self, spec):
        """ configure the progress bar from spec """
        self.set_base_from_spec(spec)
        self.width = int(spec['_width'])
    def draw(self, stdscr):
        """ draw the progress bar"""
        value = self.get_value()
        if value <= 100:
            bar_width = int(float(value)/(100.0/float(self.width)))
            output = "|"*bar_width
            output += "_"*(self.width-bar_width)
        else:
            output = "|" * self.width
        stdscr.addstr(self.ypos, self.xpos, str(output))
