from tkinter import *
from tkinter import ttk
import os

from TabGroups.HomeTab import HomeTab
from TabGroups.InputOutputTab import InputOutputTab
from TabGroups.SpriteTab import SpriteTab
from TabGroups.SpriteSheetTab import SpriteSheetTab

from Functionality.StateManager import StateManager
from Functionality.SpriteSheetManager import SpriteSheetManager

class SpriteToSpriteSheet:
    # State mgmt related members
    StateManagerObj = None
    StateFileDir = "./"

    MakeSpriteSheetObj = None

    ### GUI related members
    # Root TK node
    RootNode = None
    # Book && Tabs
    MainWindowNotebook = None
    # Frame and reference to our class
    NotebookHomeTabFrame = None
    NotebookHomeTabObj = None
    # Frame and reference to our class
    NotebookOutputTabFrame = None
    NotebookOutputTabObj = None
    # Frame and reference to our class
    NotebookSpriteTabFrame = None
    NotebookSpriteTabObj = None
    # Frame and reference to our class
    NotebookSpriteSheetTabFrame = None
    NotebookSpriteSheetTabObj = None

    def __init__(self):
        # Create references to our different classes
        self.StateManagerObj = StateManager(self.StateFileDir)
        self.MakeSpriteSheetObj = SpriteSheetManager()
        # GUI related tasks
        self.construct_gui()

    def run(self):
        # TK work
        self.RootNode.mainloop()

    ###########################
    ## Tkinter gui construction
    ###########################
    def construct_gui(self):
        # Construct the TK related
        self.RootNode = Tk()
        self.RootNode.columnconfigure(0, weight=1)
        self.RootNode.title("Sprite To Sprite Sheet")

        s = ttk.Style()
        s.theme_use("winnative")

        # Create the notebook all things will be created w/in
        self.create_main_window(self.RootNode)

        # Build out Home Tab and store a reference to our custom 'home tab' object
        self.NotebookHomeTabObj = HomeTab(self.NotebookHomeTabFrame)
        self.NotebookInputOutputTabObj = InputOutputTab(self.NotebookOutputTabFrame)
        self.NotebookSpriteTabObj = SpriteTab(self.NotebookSpriteTabFrame)
        self.NotebookSpriteSheetTabObj = SpriteSheetTab(self.NotebookSpriteSheetTabFrame)

        self.MakeSpriteSheetObj.set_logger(self.NotebookHomeTabObj.writeToLog)

        # Load last input settings from saved file
        self.load_settings()

    def create_main_window(self, root):
        """
        Creates main window and the notebook all the menus are in
        :param root:
        :return:
        """
        # Create notebook and set appropriate settings
        self.MainWindowNotebook = ttk.Notebook(root)

        # Any grid information will be setup in a class corresponding to each tab group
        self.NotebookHomeTabFrame = ttk.Frame(self.MainWindowNotebook)
        self.NotebookOutputTabFrame = ttk.Frame(self.MainWindowNotebook)
        self.NotebookSpriteTabFrame = ttk.Frame(self.MainWindowNotebook)
        self.NotebookSpriteSheetTabFrame = ttk.Frame(self.MainWindowNotebook)

        # Set up relevant listeners
        self.MainWindowNotebook.bind("<<NotebookTabChanged>>", self.save_settings_to_state_file)
        # self.NotebookHomeTabFrame.bind("<<FolderSummaryRequested>>", self.request_folder_summary)
        self.NotebookHomeTabFrame.bind("<<CreateSSRequested>>", self.request_create_ss)
        self.NotebookHomeTabFrame.bind("<<CreateSSRecRequested>>", self.request_create_ss_recursive)


        self.MainWindowNotebook.grid(column=0, row=0, columnspan=1, rowspan=1, sticky="nsew")
        self.MainWindowNotebook.columnconfigure(index=0, weight=1)

        self.MainWindowNotebook.add(self.NotebookHomeTabFrame, text="Home", sticky="nsew")
        self.MainWindowNotebook.add(self.NotebookOutputTabFrame, text="Input/Output", sticky="nsew")
        self.MainWindowNotebook.add(self.NotebookSpriteTabFrame, text="Sprite", sticky="nsew")
        self.MainWindowNotebook.add(self.NotebookSpriteSheetTabFrame, text="Sprite Sheet", sticky="nsew")

    def get_settings_from_tabs(self):
        settings_outs = {
            "HomeTabSettings": self.NotebookHomeTabObj.export_setting(),
            "InputOutputTabSettings": self.NotebookInputOutputTabObj.export_setting(),
            "SpriteTabSettings": self.NotebookSpriteTabObj.export_setting(),
            "SpritesheetTabSettings": self.NotebookSpriteSheetTabObj.export_setting(),
        }
        return settings_outs

    def load_settings(self):
        """
        Load settings from file,
        :return:
        """
        tmpSettings = self.StateManagerObj.load()
        if tmpSettings == None or len(tmpSettings) == 0:
            print("No settings to load")
            return
        self.NotebookHomeTabObj.import_settings(tmpSettings["HomeTabSettings"])
        self.NotebookInputOutputTabObj.import_settings(tmpSettings["InputOutputTabSettings"])
        self.NotebookSpriteTabObj.import_settings(tmpSettings["SpriteTabSettings"])
        self.NotebookSpriteSheetTabObj.import_settings(tmpSettings["SpritesheetTabSettings"])

    ####################
    ## Tkinter callbacks
    ####################
    def save_settings_to_state_file(self, e):
        """
        Callback for the 'noteback tab changed' event on our main display notebook.
        A simple, non-invasive way to trigger a save
        :param e: event info from tkinter
        """
        self.StateManagerObj.save(self.get_settings_from_tabs())

    # def request_folder_summary(self, e):
    #     print("Folder Summary Requested")
    #     self.MakeSpriteSheetObj.get_folder_summary()

    def request_create_ss(self, e):
        """
        Someone clicked the btn to create a ss
        :param e:
        :return:
        """
        self.save_settings_to_state_file("")
        print("Create SS Requested")
        has_files = self.MakeSpriteSheetObj.apply_current_settings(self.get_settings_from_tabs())
        if not has_files:
            self.MakeSpriteSheetObj.log_to_user("\nNo files to process in directory, no work to do.\n")
            return
        self.MakeSpriteSheetObj.request_sprite_sheet()


    def request_create_ss_recursive(self, e):
        self.save_settings_to_state_file("")
        print("Create SS Requested - Recursive")
        settings = self.get_settings_from_tabs()

        contents_of_dir = os.scandir(settings["HomeTabSettings"]["DirWorkingFolderPath"])
        for _f in contents_of_dir:
            if _f.is_dir():
                settings["HomeTabSettings"]["DirWorkingFolderPath"] = _f.path
                settings["HomeTabSettings"]["BaseFileOutName"] = _f.name
                has_files = self.MakeSpriteSheetObj.apply_current_settings(settings)
                if not has_files:
                    self.MakeSpriteSheetObj.log_to_user("\nNo files to process in directory, no work to do.\n")
                    return
                self.MakeSpriteSheetObj.request_sprite_sheet()

if __name__ == "__main__":
    SpriteToSheetObj = SpriteToSpriteSheet()
    SpriteToSheetObj.run()


    # Events example
    # root = Tk()
    # l = ttk.Label(root, text="Starting...")
    # l.grid()
    # l.bind('<Enter>', lambda e: l.configure(text='Moved mouse inside'))
    # l.bind('<Leave>', lambda e: l.configure(text='Moved mouse outside'))
    # l.bind('<ButtonPress-1>', lambda e: l.configure(text='Clicked left mouse button'))
    # l.bind('<3>', lambda e: l.configure(text='Clicked right mouse button'))
    # l.bind('<Double-1>', lambda e: l.configure(text='Double clicked'))
    # l.bind('<B3-Motion>', lambda e: l.configure(text='right button drag to %d,%d' % (e.x, e.y)))
    # root.mainloop()
