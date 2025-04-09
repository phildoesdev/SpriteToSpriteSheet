import tkinter.ttk
from tkinter import *
from tkinter import ttk
from Functionality.SpriteSummaryContainers import SpriteTileAlignment, FileNameFormat

class SpriteTab:

    # Tile Size outvars
    TileSizeWidth = None
    TileSizeHeight = None
    TileSizeAutoCalc = None # Auto calcs based on largest sprite in folder

    SpriteOffsetOriginX = None
    SpriteOffsetOriginY = None
    SpriteOffsetOriginAutoCalc = None

    # Sprite alignment ComboBox vars
    SpriteAlignmentType = None
    SpriteAlignmentComboBoxItems = []

    # Error option CheckButt vars
    DeleteSpritesWhenComplete = None
    IgnoreOversizedSprites = None


    def __init__(self, notebookSpriteTabFrame):
        # Tile Size Out Variables
        self.TileSizeWidth = StringVar()
        self.TileSizeHeight = StringVar()
        self.TileSizeAutoCalc = IntVar()
        self.TileSizeWidth.set("0")
        self.TileSizeHeight.set("0")
        self.TileSizeAutoCalc.set(True)

        self.SpriteOffsetOriginX = StringVar()
        self.SpriteOffsetOriginY = StringVar()
        self.SpriteOffsetOriginAutoCalc = IntVar()
        self.SpriteOffsetOriginX.set("0")
        self.SpriteOffsetOriginY.set("0")
        self.SpriteOffsetOriginAutoCalc.set(True)

        for option in SpriteTileAlignment:
            self.SpriteAlignmentComboBoxItems.append(option.value)
        # Alignment vars
        self.SpriteAlignmentType = StringVar()
        self.SpriteAlignmentType.set('SW')

        # filename
        self.FileNamePatternCBItems = []
        for fileNameType in list(FileNameFormat):
            self.FileNamePatternCBItems.append(fileNameType.value)
        self.FileNamePattern = StringVar()
        self.TileSizeApplyOffset = IntVar()
        self.FileNamePattern.set(FileNameFormat.FullyQualified.value)
        self.TileSizeApplyOffset.set(False)

        # Error CB Options vars
        self.IgnoreOversizedSprites = IntVar()
        self.DeleteSpritesWhenComplete = IntVar()
        self.DeleteSpritesWhenComplete.set(False)
        self.IgnoreOversizedSprites.set(False)

        spriteFrame = ttk.LabelFrame(notebookSpriteTabFrame, borderwidth=8, relief='ridge', text="Sprite Options")
        spriteFrame.grid(column=0, row=0, columnspan=1, rowspan=1, sticky="w")
        notebookSpriteTabFrame.columnconfigure(index=0, weight=1)

        self.build_tilesize_frame(spriteFrame)

    def build_tilesize_frame(self, spriteFrame):
        fileFormatFrame = ttk.Frame(spriteFrame)

        fileOffsetOriginFrame = ttk.LabelFrame(spriteFrame, text="Sprite Offset Settings")
        tileSizeFrame = ttk.Frame(spriteFrame)
        tileAlignmentFrame = ttk.Frame(spriteFrame)
        tileOtherOptionsFrame = ttk.Frame(spriteFrame)

        fileFormatFrame.grid(column=0, row=0, columnspan=1, rowspan=1, sticky="w")
        fileOffsetOriginFrame.grid(column=0, row=1, columnspan=1, rowspan=1, pady=10, sticky="w")
        tileSizeFrame.grid(column=0, row=2, columnspan=1, rowspan=1, sticky="w", pady=10)
        tileAlignmentFrame.grid(column=0, row=3, columnspan=1, rowspan=1, sticky="w", pady=10)
        tileOtherOptionsFrame.grid(column=0, row=4, columnspan=1, rowspan=1, sticky="w", pady=10)

        # Input File names
        fileNamePatternLabel = ttk.Label(fileFormatFrame, text="Sprite Naming Format")
        fileNamePatternCB = ttk.Combobox(fileFormatFrame, state="readonly", textvariable=self.FileNamePattern, values=self.FileNamePatternCBItems, width=75)

        fileNamePatternLabel.grid(column=0, row=0, columnspan=1, rowspan=1, sticky="w")
        fileNamePatternCB.grid(column=0, row=1, columnspan=4, rowspan=1, sticky="")

        # Offset options
        tileSizeApplyOffsetToSS = ttk.Checkbutton(fileOffsetOriginFrame, variable=self.TileSizeApplyOffset, text="Apply Offsets To Sprites.")
        tileSizeApplyOffsetToSS.grid(column=0, row=1, columnspan=4, rowspan=1, sticky="w")

        spriteOffsetOriginLabel = ttk.Label(fileOffsetOriginFrame, text="Sprite Offset Origin")
        spriteOffsetOriginLabelX = ttk.Label(fileOffsetOriginFrame, text="X")
        spriteOffsetOriginEntryX = ttk.Entry(fileOffsetOriginFrame, textvariable=self.SpriteOffsetOriginX, width=5)
        spriteOffsetOriginLabelY = ttk.Label(fileOffsetOriginFrame, text="Y")
        spriteOffsetOriginEntryY = ttk.Entry(fileOffsetOriginFrame, textvariable=self.SpriteOffsetOriginY, width=5)
        spriteOffsetOriginAutoCalcCB = ttk.Checkbutton(fileOffsetOriginFrame, variable=self.SpriteOffsetOriginAutoCalc, text="Auto Calculate")

        spriteOffsetOriginLabel.grid(column=0, row=3, columnspan=5, rowspan=1, sticky="w")
        spriteOffsetOriginLabelX.grid(column=0, row=4, columnspan=1, rowspan=1, sticky="w")
        spriteOffsetOriginEntryX.grid(column=1, row=4, columnspan=1, rowspan=1, sticky="w")
        spriteOffsetOriginLabelY.grid(column=2, row=4, columnspan=1, rowspan=1, sticky="w")
        spriteOffsetOriginEntryY.grid(column=3, row=4, columnspan=1, rowspan=1, sticky="w")
        spriteOffsetOriginAutoCalcCB.grid(column=4, row=4, columnspan=2, rowspan=1, sticky="w")

        tileAlignmentLabel = ttk.Label(tileSizeFrame, text="Tile Size & Alignment", underline=0)
        tileAlignmentLabel.grid(column=0, row=0, columnspan=5, rowspan=1, sticky="w")

        tileSizeWidthLabel = ttk.Label(tileSizeFrame, text="Width")
        tileSizeWidthEntry = ttk.Entry(tileSizeFrame, textvariable=self.TileSizeWidth, width=5)
        tileSizeWidthLabel.grid(column=0, row=1, columnspan=1, rowspan=1, sticky="e")
        tileSizeWidthEntry.grid(column=1, row=1, columnspan=1, rowspan=1, sticky="w")

        tileSizeHeightLabel = ttk.Label(tileSizeFrame, text="Height")
        tileSizeHeightEntry = ttk.Entry(tileSizeFrame, textvariable=self.TileSizeHeight, width=5)
        tileSizeHeightLabel.grid(column=2, row=1, columnspan=1, rowspan=1, pady=5, sticky="e")
        tileSizeHeightEntry.grid(column=3, row=1, columnspan=1, rowspan=1, pady=5, sticky="w")

        tileSizeAutoCalcCB = ttk.Checkbutton(tileSizeFrame, variable=self.TileSizeAutoCalc, text="Auto Calculate")
        tileSizeAutoCalcCB.grid(column=4, row=1, columnspan=1, rowspan=1, pady=5, sticky="w")

        tileAlignmentCBLabel = ttk.Label(tileAlignmentFrame, text="Sprite Alignment. Behaves differently if applying offsets- aligns before offset tile size is calc'd.")
        tileAlignmentCB = ttk.Combobox(tileAlignmentFrame, state='readonly', textvariable=self.SpriteAlignmentType, values=self.SpriteAlignmentComboBoxItems)

        tileAlignmentCBLabel.grid(column=0, row=0, columnspan=5, rowspan=1, sticky="e")
        tileAlignmentCB.grid(column=0, row=1, columnspan=3, rowspan=1, sticky="w")

        tileOptionsLabel = ttk.Label(tileOtherOptionsFrame, text="Other Options", underline=0)
        tileDeleteSpritesWhenCompleteCB = ttk.Checkbutton(tileOtherOptionsFrame, variable=self.DeleteSpritesWhenComplete, text="Delete Sprites When Complete")
        tileIgnoreOversizedSpritesCB = ttk.Checkbutton(tileOtherOptionsFrame, variable=self.IgnoreOversizedSprites, text="Ignore Oversized Error")
        # tileIgnoreOversizedSpritesCB = ttk.Checkbutton(tileOtherOptionsFrame, variable=self.IgnoreOversizedSprites, text="Draw Sprite Bounding Box")

        tileOptionsLabel.grid(column=0, row=0, columnspan=1, rowspan=1, sticky="w")
        tileIgnoreOversizedSpritesCB.grid(column=0, row=1, columnspan=1, rowspan=1, sticky="w")
        tileDeleteSpritesWhenCompleteCB.grid(column=0, row=2, columnspan=1, rowspan=1, sticky="w")

    def notReal(self):
        print("NOT IMPLEMENTED!!!")
        pass

    def export_setting(self):
        return_val = {
            "TileSizeWidth": self.TileSizeWidth.get(),
            "TileSizeHeight": self.TileSizeHeight.get(),
            "TileSizeAutoCalc": self.TileSizeAutoCalc.get(),
            "SpriteAlignmentType": self.SpriteAlignmentType.get(),
            "IgnoreOversizedSprites": self.IgnoreOversizedSprites.get(),
            "FileNamePattern": self.FileNamePattern.get(),
            "TileSizeApplyOffset": self.TileSizeApplyOffset.get(),
            "DeleteSpritesWhenComplete": self.DeleteSpritesWhenComplete.get(),
            "SpriteOffsetOriginX": self.SpriteOffsetOriginX.get(),
            "SpriteOffsetOriginY": self.SpriteOffsetOriginY.get(),
            "SpriteOffsetOriginAutoCalc": self.SpriteOffsetOriginAutoCalc.get(),
        }
        return return_val

    def import_settings(self, settings):
        try:
            self.TileSizeWidth.set(settings["TileSizeWidth"])
            self.TileSizeHeight.set(settings["TileSizeHeight"])
            self.TileSizeAutoCalc.set(settings["TileSizeAutoCalc"])
            self.SpriteAlignmentType.set(settings["SpriteAlignmentType"])
            self.IgnoreOversizedSprites.set(settings["IgnoreOversizedSprites"])
            self.FileNamePattern.set(settings["FileNamePattern"])
            self.TileSizeApplyOffset.set(settings["TileSizeApplyOffset"])
            self.DeleteSpritesWhenComplete.set(settings["DeleteSpritesWhenComplete"])
            self.SpriteOffsetOriginX.set(settings["SpriteOffsetOriginX"])
            self.SpriteOffsetOriginY.set(settings["SpriteOffsetOriginY"])
            self.SpriteOffsetOriginAutoCalc.set(settings["SpriteOffsetOriginAutoCalc"])
        except Exception as ex:
            print(f"Unable to find key: [{ex}]. CR5GPGA0")

