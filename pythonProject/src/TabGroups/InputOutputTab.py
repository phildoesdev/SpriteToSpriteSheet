from tkinter import *
from tkinter import ttk


class InputOutputTab:
    # It is useful to have a reference to our parent
    NotebookOutputTabFrame = None

    # The filetype the person is requesting for the main sprite sheet (outvar for combobox)
    OutFileType = None
    OutFileTypeComboBoxItems = ['PNG', 'BMP']
    # Additional Output Files Checkbox Vars
    OutputSummaryTextCheck = None
    OutputHumanReadableSummaryFileCheck = None
    OutputMasterFileCheck = None

    # Additional settings
    DrawBoundingBoxCheck = None
    DrawSpriteBoundingBoxCheck = None

    # Master File Font Color
    MasterFileFontColorR = None
    MasterFileFontColorG = None
    MasterFileFontColorB = None

    def __init__(self, notebookOutputTabFrame):
        if notebookOutputTabFrame is None:
            raise Exception("Can't initialize on non-screen")

        # Create permanent reference
        self.NotebookOutputTabFrame = notebookOutputTabFrame

        # Outpath for different gui elements
        self.OutFileType = StringVar()
        self.OutFileType.set("PNG")

        # Additional Output Files
        self.OutputSummaryTextCheck = IntVar()
        self.OutputHumanReadableSummaryFileCheck = IntVar()
        self.OutputMasterFileCheck = IntVar()
        self.OutputSummaryTextCheck.set(True)
        self.OutputHumanReadableSummaryFileCheck.set(False)
        self.OutputMasterFileCheck.set(True)
        self.DrawBoundingBoxCheck = IntVar()
        self.DrawBoundingBoxCheck.set(False)
        self.DrawSpriteBoundingBoxCheck = IntVar()
        self.DrawSpriteBoundingBoxCheck.set(False)



        # Font RGB Selection
        self.MasterFileFontColorR = IntVar()
        self.MasterFileFontColorG = IntVar()
        self.MasterFileFontColorB = IntVar()
        self.MasterFileFontColorR.set(100)      # Needs to be pulled from config
        self.MasterFileFontColorG.set(100)      # Needs to be pulled from config
        self.MasterFileFontColorB.set(100)      # Needs to be pulled from config

        # Containing Frames
        outputFrame = ttk.Frame(self.NotebookOutputTabFrame, borderwidth=8, relief='ridge')
        outputFrame.grid(column=0, row=0, sticky="nsew")
        self.NotebookOutputTabFrame.columnconfigure(index=0, weight=1)

        # Build menus
        self.build_output_label_frame(outputFrame)

    def build_output_label_frame(self, outputFrame):
        """
        Create & Draw main frame and all components
        Also binds events and such
        :param outputFrame: the frame to add this content to
        """
        # Organiziational Frames
        fileInfoFrame = ttk.Frame(outputFrame)
        fileAdditionalOutputsFrame = ttk.LabelFrame(outputFrame, text="Additional Output Files")
        fileAdditionalSettingsFrame = ttk.LabelFrame(outputFrame, text="Additional Settings")
        # masterFileFontFrame = ttk.LabelFrame(outputFrame, text="Master File Font Options")

        fileInfoFrame.grid(column=0, row=0, columnspan=1, rowspan=1, sticky="w")
        fileAdditionalOutputsFrame.grid(column=0, row=2, columnspan=1, rowspan=1, sticky="w", pady=10)
        fileAdditionalSettingsFrame.grid(column=0, row=3, columnspan=1, rowspan=1, sticky="w", pady=10)
        # masterFileFontFrame.grid(column=0, row=3, columnspan=1, rowspan=1, sticky="w", ipady=10, ipadx=10)

        # Filetype combobox
        outputFileTypeLabel = ttk.Label(fileInfoFrame, text="SpriteSheet Out File Type")
        outputFileTypeCombobox = ttk.Combobox(fileInfoFrame, state="readonly", textvariable=self.OutFileType, values=self.OutFileTypeComboBoxItems, width=22)

        outputFileTypeLabel.grid(column=0, row=0, columnspan=1, rowspan=1, sticky="w")
        outputFileTypeCombobox.grid(column=1, row=0, columnspan=1, rowspan=1, sticky="w")

        # Extra Files Checkboxes
        outputSummaryFileCheck = ttk.Checkbutton(fileAdditionalOutputsFrame, variable=self.OutputSummaryTextCheck, text="Output Summary File")
        outputMasterFileCheck = ttk.Checkbutton(fileAdditionalOutputsFrame, variable=self.OutputMasterFileCheck, text="Ouput Master Sprite Sheet")
        outputHumanReadableSummaryFileCheck = ttk.Checkbutton(fileAdditionalOutputsFrame, variable=self.OutputHumanReadableSummaryFileCheck, text="Output Human Readable Summary File")

        outputSummaryFileCheck.grid(column=0, row=0, columnspan=1, rowspan=1, sticky="w")
        outputMasterFileCheck.grid(column=0, row=1, columnspan=1, rowspan=1, sticky="w")
        outputHumanReadableSummaryFileCheck.grid(column=0, row=2, columnspan=1, rowspan=1, sticky="w")

        # Addtional options
        drawBoundBoxCheck = ttk.Checkbutton(fileAdditionalSettingsFrame, variable=self.DrawBoundingBoxCheck, text="Draw Bounding Box On Tile")
        drawSpriteBoundBoxCheck = ttk.Checkbutton(fileAdditionalSettingsFrame, variable=self.DrawSpriteBoundingBoxCheck, text="Draw Bounding Box On Sprite")
        drawBoundBoxCheck.grid(column=0, row=0, columnspan=1, rowspan=1, sticky="w")
        drawSpriteBoundBoxCheck.grid(column=0, row=1, columnspan=1, rowspan=1, sticky="w")


        # Color Chooser
        # masterFileFontColorRLabel = ttk.Label(masterFileFontFrame, text="R")
        # masterFileFontColorRSB = ttk.Spinbox(masterFileFontFrame, from_=0.0, to=255.0, increment=1.0, width=4, textvariable=self.MasterFileFontColorR, command=self.notReal)
        #
        # masterFileFontColorGLabel = ttk.Label(masterFileFontFrame, text="G")
        # masterFileFontColorGSB = ttk.Spinbox(masterFileFontFrame, from_=0.0, to=255, increment=1.0, width=4, textvariable=self.MasterFileFontColorG, command=self.notReal)
        #
        # masterFileFontColorBLabel = ttk.Label(masterFileFontFrame, text="B")
        # masterFileFontColorBSB = ttk.Spinbox(masterFileFontFrame, from_=0.0, to=255.0, increment=1.0, width=4, textvariable=self.MasterFileFontColorB, command=self.notReal)
        #
        # masterFileFontColorModalBtn = ttk.Button(masterFileFontFrame, text="Choose Font Color", command=self.choose_color_btn_press)
        #
        # masterFileFontColorRLabel.grid(column=0, row=0, columnspan=1, rowspan=1, sticky="")
        # masterFileFontColorRSB.grid(column=1, row=0, columnspan=1, rowspan=1, sticky="")
        #
        # masterFileFontColorGLabel.grid(column=2, row=0, columnspan=1, rowspan=1, sticky="")
        # masterFileFontColorGSB.grid(column=3, row=0, columnspan=1, rowspan=1, sticky="")
        #
        # masterFileFontColorBLabel.grid(column=4, row=0, columnspan=1, rowspan=1, sticky="")
        # masterFileFontColorBSB.grid(column=5, row=0, columnspan=1, rowspan=1, sticky="")
        # masterFileFontColorModalBtn.grid(column=6, row=0, columnspan=1, rowspan=1, sticky="")

    # def choose_color_btn_press(self):
    #     """
    #     Pop colorpicker and save the selected rgb
    #     :return:
    #     """
    #     output = colorchooser.askcolor(initialcolor=(self.MasterFileFontColorR.get(), self.MasterFileFontColorG.get(), self.MasterFileFontColorB.get(),))
    #     # If someone closes the modal w/o making a choice it returns none
    #     if output is None:
    #         return
    #
    #     output_rgb = output[0]
    #     self.MasterFileFontColorR.set(output_rgb[0])
    #     self.MasterFileFontColorG.set(output_rgb[1])
    #     self.MasterFileFontColorB.set(output_rgb[2])


    def notReal(self):
        print("NOT IMPLEMENTED!!!")
        pass

    def export_setting(self):
        return_val = {
            "OutFileType": self.OutFileType.get(),
            "OutputSummaryTextCheck": self.OutputSummaryTextCheck.get(),
            "OutputHumanReadableSummaryFileCheck": self.OutputHumanReadableSummaryFileCheck.get(),
            "OutputMasterFileCheck": self.OutputMasterFileCheck.get(),
            "DrawBoundingBoxCheck": self.DrawBoundingBoxCheck.get(),
            "DrawSpriteBoundingBoxCheck": self.DrawSpriteBoundingBoxCheck.get(),
            # "MasterFileFontColorR": self.MasterFileFontColorR.get(),
            # "MasterFileFontColorG": self.MasterFileFontColorG.get(),
            # "MasterFileFontColorB": self.MasterFileFontColorB.get(),
        }
        return return_val

    def import_settings(self, settings):
        try:
            self.OutFileType.set(settings["OutFileType"])
            self.OutputSummaryTextCheck.set(settings["OutputSummaryTextCheck"])
            self.OutputHumanReadableSummaryFileCheck.set(settings["OutputHumanReadableSummaryFileCheck"])
            self.OutputMasterFileCheck.set(settings["OutputMasterFileCheck"])
            self.DrawBoundingBoxCheck.set(settings["DrawBoundingBoxCheck"])
            self.DrawSpriteBoundingBoxCheck.set(settings["DrawSpriteBoundingBoxCheck"])

            # self.MasterFileFontColorR.set(settings["MasterFileFontColorR"])
            # self.MasterFileFontColorG.set(settings["MasterFileFontColorG"])
            # self.MasterFileFontColorB.set(settings["MasterFileFontColorB"])
        except Exception as ex:
            print(f"Unable to find key: [{ex}]. ITUR6GZ0")

