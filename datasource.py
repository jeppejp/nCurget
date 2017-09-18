""" The data source - key value lookup tbd """

class Datasource(object):
    """ tdb """
    def __init__(self):
        self.value = 0
        self.values = {}
    def get_value(self, key):
        """ return a value based on key """
        if key in self.values:
            return self.values[key]
        return self.value
    def set_value(self, key, value):
        """ set the value of a key """
        self.values[key] = value
