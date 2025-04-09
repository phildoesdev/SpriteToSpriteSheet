import tkinter
from tkinter import *
from tkinter import ttk

class SpriteSheetTab:

    # CB Settings
    MakeSpriteSheetSquare = None
    AddAlphaLayer = None

    # 'Make Alpha' options
    MakeColorsTransparent = None
    MakeColorsTransparentTextbox = None

    def __init__(self, notebookSpriteSheetTabFrame):
        # Top options vars
        self.MakeSpriteSheetSquare = IntVar()
        self.AddAlphaLayer = IntVar()

        self.MakeSpriteSheetSquare.set(True)
        self.AddAlphaLayer.set(True)

        # Make Alpha Options
        self.MakeColorsTransparent = IntVar()
        self.MakeColorsTransparent.set(False)


        spriteSheetFrame = ttk.Frame(notebookSpriteSheetTabFrame, borderwidth=8, relief='ridge')
        spriteSheetFrame.grid(column=0, row=0, columnspan=1, rowspan=1, sticky="nesw")

        self.build_spritesheet_frame(spriteSheetFrame)


    def build_spritesheet_frame(self, spriteSheetFrame):
        spriteSheetCBOptionsFrame = ttk.LabelFrame(spriteSheetFrame, text="Sprite Sheet Options")
        spriteSheetAlphaSettingsFrame = ttk.LabelFrame(spriteSheetFrame, text="SS Alpha Options")

        spriteSheetCBOptionsFrame.grid(column=0, row=0, columnspan=1, rowspan=1, sticky="w")
        # spriteSheetAlphaSettingsFrame.grid(column=0, row=1, columnspan=1, rowspan=1, sticky="w")

        spriteSheetMakeSquareCheckB = ttk.Checkbutton(spriteSheetCBOptionsFrame, variable=self.MakeSpriteSheetSquare, text="Make SS Square")
        spriteSheetAddAlphaLayerCB = ttk.Checkbutton(spriteSheetCBOptionsFrame, variable=self.AddAlphaLayer, text="Add Alpha Layer")

        spriteSheetMakeSquareCheckB.grid(column=0, row=0, columnspan=1, rowspan=1, sticky="e")
        spriteSheetAddAlphaLayerCB.grid(column=1, row=0, columnspan=1, rowspan=1, sticky="e")

        # spriteSheetMakeColorsTransparent = ttk.Checkbutton(spriteSheetAlphaSettingsFrame, variable=self.MakeColorsTransparent, text="Make Colors Transparent")
        # spriteSheetMakeColorsTransparent.grid(column=0, row=0, columnspan=1, rowspan=1, sticky="w")
        #
        # spriteSheetAddColorToAlphaListBoxLabel = ttk.Label(spriteSheetAlphaSettingsFrame, text="Color Tuples to Make trans (R,G,B,A), new line delimited entries")
        # self.MakeColorsTransparentTextbox = tkinter.Text(spriteSheetAlphaSettingsFrame, height=10)
        #
        # spriteSheetAddColorToAlphaListBoxLabel.grid(column=0, row=1, columnspan=4, rowspan=1, sticky="w")
        # self.MakeColorsTransparentTextbox.grid(column=0, row=2, columnspan=4, rowspan=3, sticky="w")

    def export_setting(self):
        return_val = {
                "MakeSpriteSheetSquare": self.MakeSpriteSheetSquare.get(),
                "AddAlphaLayer": self.AddAlphaLayer.get(),
                "MakeColorsTransparent": self.MakeColorsTransparent.get(),
                # "MakeColorsTransparentListVar": self.MakeColorsTransparentTextbox.get("1.0", "end"),
        }
        return return_val

    def import_settings(self, settings):
        try:
            self.MakeSpriteSheetSquare.set(settings["MakeSpriteSheetSquare"])
            self.AddAlphaLayer.set(settings["AddAlphaLayer"])
            self.MakeColorsTransparent.set(settings["MakeColorsTransparent"])
            # self.MakeColorsTransparentTextbox.insert("1.0", settings["MakeColorsTransparentListVar"])
        except Exception as ex:
            print(f"Unable to find key: [{ex}]. WZRGFU1L")
