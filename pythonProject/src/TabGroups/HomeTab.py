from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import colorchooser


class HomeTab:
    DefaultPathSeparator = "/"

    # It is useful to have a reference to our parent
    NotebookHomeTabFrame = None
    HomeTabOutputText = None

    # The base filename for the sprite sheet and other files  (outvar for entry)
    BaseFileOutName = None

    # the directory we're going to dump files to (outvar for entry)
    DirWorkingFolderPath = None

    def __init__(self, notebookHomeTabFrame):
        if notebookHomeTabFrame is None:
            raise Exception("Can't initialize on non-screen")
        self.NotebookHomeTabFrame = notebookHomeTabFrame

        self.BaseFileOutName = StringVar()
        self.BaseFileOutName.set("Spritesheet")

        self.DirWorkingFolderPath = StringVar()
        self.DirWorkingFolderPath.set("../outputfolder")  # This will have to be set/loaded from some sort of config file at some point

         # Containing Frames
        homeFrame = ttk.Frame(self.NotebookHomeTabFrame, borderwidth=8, relief='ridge')
        homeFrame.grid(column=0, row=0, sticky="nsew")
        self.NotebookHomeTabFrame.columnconfigure(index=0, weight=1)

        # Build menus
        self.build_home_frame(homeFrame)

    def build_home_frame(self, homeFrame):
        # containing frames
        btnFrame = ttk.Frame(homeFrame, borderwidth=4, relief="ridge")
        txtBoxFrame = ttk.Frame(homeFrame)

        # Add containers to screen
        btnFrame.grid(column=0, row=0, columnspan=1, rowspan=1, sticky="nsew")
        txtBoxFrame.grid(column=1, row=0, columnspan=2, rowspan=1, sticky="nsew")

        # Buttons for btn frame
        createSpriteSheetButton = ttk.Button(btnFrame, text="Create Sprite Sheet", command=self.request_create_ss)
        createSpriteSheetRecursiveButton = ttk.Button(btnFrame, text="Create Sprite Sheet\n Recursive", command=self.request_create_ss_rec)

        # Output File Name
        outputFileNameBaseLabel = ttk.Label(btnFrame, text="Output File Name Base")
        outputFileNameBaseEntry = ttk.Entry(btnFrame, textvariable=self.BaseFileOutName, width=25)

        outputFileNameBaseLabel.grid(column=0, row=1, columnspan=3, rowspan=1, sticky="w")
        outputFileNameBaseEntry.grid(column=0, row=2, columnspan=3, rowspan=1, sticky="w")

        # File Path
        filePathLabel = ttk.Label(btnFrame, text="Working Folder")
        filePathEntry = ttk.Entry(btnFrame, state="readonly", textvariable=self.DirWorkingFolderPath, width=25)
        filePathBtn = ttk.Button(btnFrame, text="Find Dir", command=self.find_dir_btn_press)

        filePathLabel.grid(column=0, row=3, columnspan=1, rowspan=1, pady=5, sticky="w")
        filePathEntry.grid(column=0, row=4, columnspan=4, rowspan=1, sticky="w")
        filePathBtn.grid(column=0, row=5, columnspan=1, rowspan=1, sticky="w")

        createSpriteSheetButton.grid(column=0, row=7, columnspan=2,  ipadx=10, pady=5, stick="w")
        createSpriteSheetRecursiveButton.grid(column=0, row=8, columnspan=2, ipadx=10, stick="w")

        # Txt box for txt box frame (and its scrollbars)
        self.HomeTabOutputText = Text(txtBoxFrame, state="disabled", width=80, height=24)
        # Add log
        self.HomeTabOutputText.grid(sticky="nsew")


    def writeToLog(self, msg):
        # text.tag_add('highlightline', '5.0', '6.0') // highlight something. neat
        # text.tag_configure('highlightline', background='yellow', font='TkFixedFont', relief='raised')

        numlines = int(self.HomeTabOutputText.index('end - 1 line').split('.')[0])
        self.HomeTabOutputText['state'] = 'normal'
        # if numlines==24:
        #     self.HomeTabOutputText.delete(1.0, 2.0)
        if self.HomeTabOutputText.index('end-1c')!='1.0':
            self.HomeTabOutputText.insert('end', '\n')
        self.HomeTabOutputText.insert('end', msg)
        self.HomeTabOutputText['state'] = 'disabled'
        self.HomeTabOutputText.see('end')

    def wipeLog(self):
        # self.HomeTabOutputText.delete(1.0, 'end')
        print("Broke")

    # def request_folder_summary(self):
    #     self.NotebookHomeTabFrame.event_generate("<<FolderSummaryRequested>>")

    def request_create_ss(self):
        self.NotebookHomeTabFrame.event_generate("<<CreateSSRequested>>")
    def request_create_ss_rec(self):
        self.NotebookHomeTabFrame.event_generate("<<CreateSSRecRequested>>")

    def export_setting(self):
        return_val = {
            "BaseFileOutName": self.BaseFileOutName.get(),
            "DirWorkingFolderPath": self.DirWorkingFolderPath.get(),
        }
        return return_val

    def import_settings(self, settings):
        try:
            self.BaseFileOutName.set(settings["BaseFileOutName"])
            self.DirWorkingFolderPath.set(settings["DirWorkingFolderPath"])
        except Exception as ex:
            print(f"Unable to find key: [{ex}]. I2R6333")

    def find_dir_btn_press(self):
        output = filedialog.askdirectory(parent=self.NotebookHomeTabFrame, mustexist=True, title="Choose an output directiony", initialdir=self.DirWorkingFolderPath.get())  # Initial dir will have to be loaded/saved from a config file or w/e at some point
        if output != '':
            self.DirWorkingFolderPath.set(output)
            if True:
                self.BaseFileOutName.set(output[(output.rfind(self.DefaultPathSeparator)+1):])
