""" The main entry """
import curses
import json
import widgets
import datareceiver


class NCurget:
    def __init__(self):
        self.created_widgets = []
        self.key = 0
        self.datasource = datareceiver.ThreadedReceiver('127.0.0.1',9530)
        self.datasource.start()
    def draw(self, stdscr):
        curses.curs_set(0)
        curses.halfdelay(1)

        while self.key != 'q':
            for widget in self.created_widgets:
                widget.draw(stdscr)
            stdscr.refresh()
            try:
                self.key = stdscr.getkey()
            except:
                pass
        self.datasource.stop_receiver()

    def setup(self):
        """ Setup widgets based on config json """
        with open("setup.json") as fptr:
            config = json.load(fptr)

        for entry in config:
            self.created_widgets.append(widgets.create_widget(entry, self.datasource))

    


if __name__ == '__main__':
    ncurget = NCurget()
    ncurget.setup()
    curses.wrapper(ncurget.draw)
    print ncurget.key
