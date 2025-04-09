from PIL import Image, ImageDraw, ImageFont
import os
import datetime, time
import json

from Functionality.SpriteSummaryContainers import SpriteWorkingFolderInfo, SpriteFileInfo, SpriteSheetInfo, FileNameFormat


class SpriteSheetManager:
    """
    Does all the heavy lifting of parsing files and creating sprite sheets
    """
    current_settings = None
    # An SpriteWorkingFolderInfo object that acts as a container
    current_folder_summary = None
    current_ss_info = None
    current_file_list = []

    log_to_user_mthd = None

    def __init__(self):
        """
            Going to keep it 'simple to implement', meaning that I am going to roughly keep it as the old one was and try to improve and cleanup
                along the way.
            If something comes off as needing to be split out, I will, otherwise it's functionality is simple enough, even if it's fairly complicated

            Count on a standard filename for sevearl things
        """
        pass

    def set_logger(self, mthd):
        self.log_to_user_mthd = mthd

    def log_to_user(self, msg):
        if self.log_to_user_mthd is None:
            print(msg)
        self.log_to_user_mthd(msg)

    def get_output_dir(self):
        """
        Makes our output dir if it doesnt exist and returns that path
        :return: string
            the path to output folder
        """
        output_dir = f'{self.current_settings["HomeTabSettings"]["DirWorkingFolderPath"]}/_SSout/'
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)
        return output_dir

    def get_output_filename(self, append_ext=True, is_master=False):
        """
        Returns the filename and extension
        :param append_ext: bool, whether we append the file extension to the file name
        :return: String
        """
        out = self.current_settings["HomeTabSettings"]["BaseFileOutName"]
        if is_master:
            out = "master_" + out
        if append_ext:
            out += "." + self.current_settings["InputOutputTabSettings"]["OutFileType"].lower()
        return out

    def clean_sprite_files(self):
        """
        Loops all files in the current_file_list and deletes them from the file system
        """
        for spritefile in self.current_file_list:
            if os.path.exists(spritefile.file_path):
                os.remove(spritefile.file_path)

    def traverse_folders(self, src_folder_path, callback_mthd, valid_file_extensions=('.bmp', '.jpg', '.png'), is_rec=False):
        """
        Basic method to traverse a folder and do a callback on specific file types.
        Can be recursive
        Originally got split out this way because there was a fair amount of looping to do, less so now, but still keeping
            split out b/c why not.

        :param src_folder_path:
            Where to begin our search
        :param callback_mthd:
            The method to call on matching file extensions
        :param valid_file_extensions:
            Valid file extensions is a tuple of strings (file extensions) that we'll call our callback on. "include the dot like .jpg"
        :param is_rec:
            Bool, whether we will recursively dig thru folders starting from the src_folder_path
        """
        files_to_manip = os.scandir(src_folder_path)
        for _f in files_to_manip:
            if _f.is_file() and _f.name.endswith(valid_file_extensions):
                callback_mthd(_f.path)
            elif _f.is_dir() and is_rec:
                self.traverse_folders(_f.path, callback_mthd)

    def process_current_folder(self):
        if self.current_settings is None:
            return
        self.log_to_user(f"\nParsing Folder: \n\t[{self.current_settings['HomeTabSettings']['DirWorkingFolderPath']}]")
        self.traverse_folders(src_folder_path=self.current_settings["HomeTabSettings"]["DirWorkingFolderPath"], callback_mthd=self.build_file_list_cb)
        # purge file list
        self.current_file_list = [x for x in self.current_file_list if x.is_valid]
        # Immediately sort the constructed list by frame count
        self.current_file_list = sorted(self.current_file_list, key=lambda file: int(file.frame_number))

    def build_file_list_cb(self, path):
        # self.log_to_user(f"Parsing file... \n\t[{path}]")
        self.current_file_list.append(SpriteFileInfo(path, FileNameFormat.FullyQualified.value))

    def apply_current_settings(self, curr_settings):
        """
        Only slightly complex because we want to reparse folders and such if the directory has changed
        :param curr_settings:
            dict containing all settings info
        """
        # Originally was only reparsing files if folders or something changed, but more likely that files changed so always reparse
        self.current_settings = curr_settings
        # Reset file list and other settings if we're looking at a new set of imgs or w/e
        self.current_file_list = []
        self.process_current_folder()
        if len(self.current_file_list) == 0:
            return False
        self.current_folder_summary = SpriteWorkingFolderInfo(self.current_file_list)
        return True

    def request_sprite_sheet(self):
        # Create Sprite Sheet
        ss_path = self.construct_sprite_sheet()

        # Create master sprite sheet if requested
        if bool(self.current_settings["InputOutputTabSettings"]["OutputMasterFileCheck"]):
            ms_path = self.construct_sprite_sheet(is_master=True)

        # Try to create
        self.create_summary_file()

        # Remove files if requested
        if self.current_settings["SpriteTabSettings"]["DeleteSpritesWhenComplete"]:
            self.clean_sprite_files()
            self.log_to_user_mthd("\n... Sprite Files Deleted\n")

        self.log_to_user_mthd("==============================================================\n\n")

    def construct_sprite_sheet(self, is_master=False):
        """
        Loops through all sprite files in output folder and creates a sprite sheet with them

        :return: string the path we saved our sprite sheet to
        """
        # Sanity check
        if self.current_settings is None or len(self.current_file_list) == 0 or self.current_folder_summary is None:
            print("Unable to construct sprite sheet w/o required data. A4OX8JZU")
            return

        # Calculate sprite sheet and tile dims, act as a utility to let us easily step thru drawing on our SS file
        self.current_ss_info = SpriteSheetInfo(self.current_settings, self.current_folder_summary)

        # Create our ss, loop imgs and start building
        ss_img_mode = "RGBA" if self.current_settings["SpritesheetTabSettings"]["AddAlphaLayer"] else "RGB"
        with (Image.new(ss_img_mode, (self.current_ss_info.ss_width_px, self.current_ss_info.ss_height_px), (0, 0, 0, 0)) as sprite_sheet):
            for spritefile in self.current_file_list:
                # rely on ss info to calculate where to draw our sprite on the sprite sheet (draws from top left of sprite)
                draw_x, draw_y = self.current_ss_info.get_next_draw_pos(spritefile)
                with Image.open(spritefile.file_path, formats=(spritefile.file_extension,)) as sprite:
                    sprite_sheet.paste(sprite, (draw_x, draw_y))
                if is_master:
                    # draw words on ss
                    pos_x, pos_y = self.current_ss_info.get_current_tile_position()
                    ss_master_draw = ImageDraw.Draw(sprite_sheet)
                    ss_master_draw.font = ImageFont.truetype("Font/ouClassic.ttf",  28)
                    ss_master_draw.text((pos_x, pos_y), str(self.current_ss_info.current_tile_count), fill=(254, 255, 255, 255))
                if self.current_settings["InputOutputTabSettings"]["DrawBoundingBoxCheck"]:
                    ss_master_draw = ImageDraw.Draw(sprite_sheet)
                    pos_x, pos_y = self.current_ss_info.get_current_tile_position()
                    bound_box_list = [(pos_x, pos_y),
                                      (pos_x+self.current_ss_info.tile_width-1, pos_y),
                                      (pos_x+self.current_ss_info.tile_width-1, pos_y+self.current_ss_info.tile_height-1),
                                      (pos_x, pos_y+self.current_ss_info.tile_height-1),
                                      (pos_x, pos_y)]
                    ss_master_draw.line(bound_box_list, fill="Red", width=1)
                if self.current_settings["InputOutputTabSettings"]["DrawSpriteBoundingBoxCheck"]:
                    ss_master_draw = ImageDraw.Draw(sprite_sheet)
                    bound_box_two = [(draw_x, draw_y),
                                     (draw_x+spritefile.img_width-1, draw_y),
                                     (draw_x+spritefile.img_width-1, draw_y+spritefile.img_height-1),
                                     (draw_x, draw_y+spritefile.img_height-1),
                                     (draw_x, draw_y)]
                    ss_master_draw.line(bound_box_two, fill="Green", width=1)

            # Prepare to save sprite sheet
            save_path = self.get_output_dir()

            save_path += self.get_output_filename(is_master=is_master)
            sprite_sheet.save(save_path)
            additional_log_out_txt = ""
            if is_master:
                additional_log_out_txt = "Master "

            self.log_to_user_mthd(f"\n{additional_log_out_txt}Sprite Sheet Saved to: \n\t[{save_path}]")
            return save_path

    def create_master_sheet(self, ss_path):
        self.current_ss_info = SpriteSheetInfo(self.current_settings, self.current_folder_summary)
        with Image.open(ss_path, formats=(self.current_settings["InputOutputTabSettings"]["OutFileType"],)) as master_ss:
            ss_draw = ImageDraw.Draw(master_ss)
            # hard coded font for now

            for spritefile in self.current_file_list:
                # Draw in the section we want
                # would also be nice to be able to choose font size on the gui
                pass

    def create_summary_file(self):
        # Only create it if the people want it
        if not self.current_settings["InputOutputTabSettings"]["OutputSummaryTextCheck"]:
            return
        # Calculate the correct output directory for out files.. create if not exists
        outputdir = self.get_output_dir()
        # Compile our file summary dictionary - can look different depending on avail data and selected options
        file_out = self.get_file_summary()

        # Writing the json animation summary file is straight forward
        output_filename = self.get_output_filename(append_ext=False) + "_meta.json"
        with open(outputdir+output_filename, "wt") as f:
            f.write(json.dumps(file_out))
        self.log_to_user_mthd(f"\nSummary File Written To: \n\t{outputdir+output_filename}")

        # We need to create a human-readable version of our summary file as well if requested
        if self.current_settings["InputOutputTabSettings"]["OutputHumanReadableSummaryFileCheck"]:
            dt_string = (datetime.datetime.now()).strftime("%d/%m/%Y %H:%M:%S")
            output_filename = self.get_output_filename(append_ext=False) + "_summary.txt"
            with open(outputdir+output_filename, "wt") as f:
                f.write("___Sprite Sheet Summary___\n")
                f.write(f"\tName : {file_out['SheetName']}\n")
                f.write(f"\tSS Name : {self.get_output_filename()}\n")
                f.write(f"\tCreated : {dt_string}\n")
                if file_out['SheetID'] != 0:
                    f.write(f"\tSheet_ID : {file_out['SheetID']}\n")

                f.write("\n\n ___ SS Summary ___ \n")
                f.write(f"\t Tile Size (W, H): ({file_out['TileWidth']},{file_out['TileHeight']})\n")
                f.write(f"\t Total Tiles: {file_out['TotalUsedTiles']}\n")
                f.write(f"\t Total (Rows, Cols): ({file_out['Rows']},{file_out['Columns']})\n")
                f.write(f"\t Smallest Width, Smallest Height (Sprites): ({file_out['SmallestSpriteUsedWidth']},{file_out['SmallestSpriteUsedHeight']})\n")
                f.write(f"\t Largest Width, Largest Height (Sprites): ({file_out['LargestSpriteUsedWidth']},{file_out['LargestSpriteUsedHeight']})\n")

                f.write("\n\n ___ User Options ___ \n")
                f.write(f'\t Auto Calc Tile Size: {bool(self.current_settings["SpriteTabSettings"]["TileSizeAutoCalc"])} \n')
                if not bool(self.current_settings["SpriteTabSettings"]["TileSizeAutoCalc"]):
                    f.write(f'\t\t Set Tile Size: ({self.current_settings["SpriteTabSettings"]["TileSizeWidth"]},{self.current_settings["SpriteTabSettings"]["TileSizeHeight"]}) \n')
                f.write(f'\t Apply Offset To Sprite: {bool(self.current_settings["SpriteTabSettings"]["TileSizeApplyOffset"])} \n')
                if bool(self.current_settings["SpriteTabSettings"]["TileSizeApplyOffset"]):
                    f.write(f'\t Auto Calc Offset Origin: {bool(self.current_settings["SpriteTabSettings"]["SpriteOffsetOriginAutoCalc"])} \n')
                    if not self.current_settings["SpriteTabSettings"]["SpriteOffsetOriginAutoCalc"]:
                        f.write(f'\t\t Set Sprite Offset Origin: ({self.current_settings["SpriteTabSettings"]["SpriteOffsetOriginX"]}, {self.current_settings["SpriteTabSettings"]["SpriteOffsetOriginY"]}) \n')
                    else:
                        f.write(f'\t\t Sprite Offset Origin (x,y): ({file_out["SpriteOffsetOriginX"]}, {file_out["SpriteOffsetOriginY"]}) \n')

                f.write(f'\t Make Sprite Sheet Square: {bool(self.current_settings["SpritesheetTabSettings"]["MakeSpriteSheetSquare"])} \n')
                f.write(f'\t Sprite-Tile Alignment: {self.current_settings["SpriteTabSettings"]["SpriteAlignmentType"]} \n')
                f.write(f'\t Filename Pattern Used: {self.current_settings["SpriteTabSettings"]["FileNamePattern"]} \n')

                f.write("\n\n ___ Animation Summary ___ \n")
                for animation_id in sorted(file_out["AnimationSummaries"].keys(), key=lambda ani_id: int(ani_id)):
                    f.write('\t{')
                    f.write(f'\n\t\t AnimationID: {animation_id},')
                    f.write(f'\n\t\t Starting Frame: {file_out["AnimationSummaries"][animation_id]["StartingFrame"]},')
                    f.write(f'\n\t\t Total Directions: {file_out["AnimationSummaries"][animation_id]["TotalDirections"]},')
                    f.write(f'\n\t\t Frames Per Direction: {file_out["AnimationSummaries"][animation_id]["FramesPerDirection"]},')
                    f.write('\n\t\t},\n')

                if len(file_out["FrameSummaryMap"].keys()) != 0:
                    f.write("\n\n ___ Frame Summary ___ \n")
                    f.write("\t{\n")
                    for frameid in sorted(file_out["FrameSummaryMap"].keys(), key=lambda frameidl: int(frameidl)):
                        f.write(f'\t\t"{frameid}": {file_out["FrameSummaryMap"][frameid]},\n')
                    f.write("\t}")
                    f.write("\n\n")
            self.log_to_user_mthd(f"\nSummary File Written To: \n\t{outputdir+output_filename}")

    def get_file_summary(self):
        # Begin building our file
        file_out = {
            "SheetID": 0,
            "SheetName": self.get_output_filename(),
            "CreateTimeEpoch": int(time.time()),
            "TileWidth": self.current_ss_info.tile_width,
            "TileHeight": self.current_ss_info.tile_height,
            "TotalUsedTiles": self.current_folder_summary.total_sprites,
            "Rows": self.current_ss_info.ss_rows,
            "Columns": self.current_ss_info.ss_cols,
            "SmallestSpriteUsedWidth": self.current_folder_summary.min_width,
            "SmallestSpriteUsedHeight": self.current_folder_summary.min_height,
            "LargestSpriteUsedWidth": self.current_folder_summary.max_width,
            "LargestSpriteUsedHeight": self.current_folder_summary.max_height,
            "SpriteOffsetOriginX": self.current_ss_info.sprite_origin_offset_x,
            "SpriteOffsetOriginY": self.current_ss_info.sprite_origin_offset_y,
            "AnimationSummaries": "",
            "FrameSummaryMap": "",
        }

        # Fill out missing structs or w/e where available
        if self.current_settings["SpriteTabSettings"]["FileNamePattern"] in [FileNameFormat.FullyQualified.value, FileNameFormat.Offsets.value]:
            file_out["SheetID"] = int(self.current_file_list[0].sprite_sheet_id)   # should be the same for all files, so pull first value
            # output frame offset list if we have them
            frame_offset_map = {}
            for file in self.current_file_list:
                frame_offset_map[int(file.frame_number)] = {}
                frame_offset_map[int(file.frame_number)]["OffsetX"] = file.offset_x
                frame_offset_map[int(file.frame_number)]["OffsetY"] = file.offset_y
                frame_offset_map[int(file.frame_number)]["Width"] = file.img_width
                frame_offset_map[int(file.frame_number)]["Height"] = file.img_height
            file_out["FrameSummaryMap"] = frame_offset_map

        animation_summary_dict = self.get_animation_summary()
        file_out["AnimationSummaries"] = animation_summary_dict

        return file_out

    def get_animation_summary(self):
        """
        loops through sprites and summarizes them relative to their animations id
        called if needed when writing the summary file
        :return: dict
        """
        animation_summary_dict = {}
        animation_summary_out_dict = {}
        for sprite in self.current_file_list:
            # Past this point is the work required to summarize our animation details
            if not sprite.has_animation_details:
                continue
            # Add this animation ID to out summary list if it doesn't exist yet
            if sprite.animation_id not in animation_summary_dict.keys():
                # Initialize the summary entry and  summarize the previous if appropriate
                animation_summary_dict[sprite.animation_id] = {
                    "starting_frame": int(sprite.frame_number),
                    "total_frames": 0,
                    "total_directions": 0,
                    "equal_frames_per_direction": True,
                    "max_frames_per_direction": 0,
                    "directions_summary": {}
                }
            animation_summary_dict[sprite.animation_id]["total_frames"] += 1

            # if we haven't seen this direction initialize it
            if sprite.direction not in animation_summary_dict[sprite.animation_id]["directions_summary"].keys():
                animation_summary_dict[sprite.animation_id]["total_directions"] += 1
                animation_summary_dict[sprite.animation_id]["directions_summary"][sprite.direction] = {
                    "total_frames": 0,
                }
            animation_summary_dict[sprite.animation_id]["directions_summary"][sprite.direction]["total_frames"] += 1

        # finish summary
        for animation_id in animation_summary_dict.keys():
            # I want to know if all dirs have the same # of frames
            frames_per_dir = -1
            for dir_id in animation_summary_dict[animation_id]["directions_summary"].keys():
                dir_ttl_frames = animation_summary_dict[animation_id]["directions_summary"][dir_id]["total_frames"]
                # If this is the first direction we're looking at we need to set the value
                if frames_per_dir == -1:
                    frames_per_dir = dir_ttl_frames
                # test for any differences
                if dir_ttl_frames != frames_per_dir:
                    animation_summary_dict[animation_id]["equal_frames_per_direction"] = False
                    print(f"{animation_summary_dict[animation_id]['directions_summary']}")
                    raise Exception(f"Not all directions have the same number of frames in animationID: [{animation_id}]")
                if dir_ttl_frames >= animation_summary_dict[animation_id]["max_frames_per_direction"]:
                    animation_summary_dict[animation_id]["max_frames_per_direction"] = dir_ttl_frames

            animation_summary_out_dict[animation_id] = {}
            animation_summary_out_dict[animation_id]["StartingFrame"] = animation_summary_dict[animation_id]["starting_frame"]
            animation_summary_out_dict[animation_id]["TotalDirections"] = animation_summary_dict[animation_id]["total_directions"]
            animation_summary_out_dict[animation_id]["FramesPerDirection"] = animation_summary_dict[animation_id]["max_frames_per_direction"]
        return animation_summary_out_dict


        # Current setting struct

        # self.current_settings["HomeTabSettings"]["BaseFileOutName"]

        # self.current_settings["InputOutputTabSettings"]["DirWorkingFolderPath"]
        # self.current_settings["InputOutputTabSettings"]["OutFileType"]
        # self.current_settings["InputOutputTabSettings"]["OutputSummaryTextCheck"]
        # self.current_settings["InputOutputTabSettings"]["OutputHumanReadableSummaryFileCheck"]
        # self.current_settings["InputOutputTabSettings"]["OutputMasterFileCheck"]

        # self.current_settings["InputOutputTabSettings"]["DrawBoundingBoxCheck"]
        # self.current_settings["InputOutputTabSettings"]["DrawSpriteBoundingBoxCheck"]

        # self.current_settings["SpriteTabSettings"]["TileSizeWidth"]
        # self.current_settings["SpriteTabSettings"]["TileSizeHeight"]
        # self.current_settings["SpriteTabSettings"]["TileSizeAutoCalc"]
        # self.current_settings["SpriteTabSettings"]["SpriteAlignmentType"]
        # self.current_settings["SpriteTabSettings"]["DeleteSpritesWhenComplete"]
        # self.current_settings["SpriteTabSettings"]["IgnoreOversizedSprites"]
        # self.current_settings["SpriteTabSettings"]["FileNamePattern"]
        # self.current_settings["SpriteTabSettings"]["TileSizeApplyOffset"]
        # self.current_settings["SpriteTabSettings"]["SpriteOffsetOriginX"]
        # self.current_settings["SpriteTabSettings"]["SpriteOffsetOriginY"]
        # self.current_settings["SpriteTabSettings"]["SpriteOffsetOriginAutoCalc"]

        # self.current_settings["SpritesheetTabSettings"]["MakeSpriteSheetSquare"]
        # self.current_settings["SpritesheetTabSettings"]["MakeColorsTransparent"]
        # self.current_settings["SpritesheetTabSettings"]["MakeColorsTransparentListVar"]
