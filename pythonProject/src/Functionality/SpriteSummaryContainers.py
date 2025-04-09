import math
from PIL import Image
from enum import Enum


class FileNameFormat(Enum):
    """
    {frameCounter}_{animationID}_{direction}_{frame}_{offset_x}_{offset_y}
        frameCounter is an incrementing value that indicates the order things should be placed on the sheet
        animation ID is a counter from 0 for distinct animations, must be included to output godot summary file
        direction ID is a counter from 0 for distinct directions, must be included to output godot summary file
        frame ID is a counter from 0 for distinct frames in this animation.direction.frame, must be included to output godot sumamry file
        offset X from the bottom left corner, can be used to draw the sprite sheet w/ correct offset, primarily intended for our godot summary file. Req'd to output godot summary file
        offset Y from the bottom left corner, can be used to draw the sprite sheet w/ correct offset, primarily intended for our godot summary file. Req'd to output godot summary file

    OR

    {frameCounter}
        frameCounter is an incrementing value that indicates the order things should be placed on the sheet

    OR

    {frameCounter}_{offsetX}_{offsetY}
        frameCounter is an incrementing value that indicates the order things should be placed on the sheet
        offset X from the bottom left corner, can be used to draw the sprite sheet w/ correct offset, primarily intended for our godot summary file. Req'd to output godot summary file
        offset Y from the bottom left corner, can be used to draw the sprite sheet w/ correct offset, primarily intended for our godot summary file. Req'd to output godot summary file
    """
    FullyQualified = "{frameNumber}_{spriteid}_{animationID}_{direction}_{offset_x}_{offset_y}"
    Offsets = "{frameCounter}_{offsetX}_{offsetY}"
    FrameCounterOnly = "{frameCounter}"


class SpriteTileAlignment(Enum):
    Center = "Center"
    N = "N"
    NE = "NE"
    E = "E"
    SE = "SE"
    S = "S"
    SW = "SW"
    W = "W"
    NW = "NW"


class SpriteFileInfo:
    """
    A Nice container for each file so we can easily manipulate things w/o having to parse our files more than once
    """
    # If set to false we will ignore it when processing the sprite sheet
    is_valid = True

    # A tuple containing our w,h
    img_width = 0
    img_height = 0
    img_mode = ""
    file_extension = ""
    img_has_transparency_data = False

    # id for this sprite sheet, pulled from filename, likely the same for all sprite files
    sprite_sheet_id = 0

    # sprite sheet positional, required details
    frame_number = 0     # The # of
    file_path = ""
    file_name = ""
    file_name_type = None

    # additional, optional details
    has_animation_details = False
    animation_id = 0
    direction = 0

    has_offset = False
    offset_x = 0
    offset_y = 0

    def __init__(self, path, file_name_format):
        self.file_path = path
        # Read file w/ pil
        self._process_sprite_file(path)
        if not self.is_valid:
            return
        # Break apart the name
        self._process_file_name(file_name_format)

    def __str__(self):
        out_dict = {
            "sprite_sheet_id": self.sprite_sheet_id,
            "img_width": self.img_width,
            "img_height": self.img_height,
            "img_mode": self.img_mode,
            "file_extension": self.file_extension,
            "img_has_transparency_data": self.img_has_transparency_data,
            "frame_number": self.frame_number,
            "file_name": self.file_name,
            "file_name_type": self.file_name_type,
            "has_animation_details": self.has_animation_details,
            "animation_id": self.animation_id,
            "direction": self.direction,
            "has_offset": self.has_offset,
            "offset_x": self.offset_x,
            "offset_y": self.offset_y,
        }
        return str(out_dict)

    def _process_sprite_file(self, path):
        """
        Tries to open the path with PIL and records some basic information
        :param path:
        :return:
        """
        with Image.open(path) as im:
            self.img_width = im.width
            self.img_height = im.height
            self.img_mode = im.mode
            self.img_has_transparency_data = im.has_transparency_data

            path_ = im.filename
            filename_idx = path_.rfind("\\") + 1
            file_parts = path_[filename_idx:].split(".")

            self.file_name = file_parts[0]
            self.file_extension = file_parts[1]

    def _process_file_name(self, file_name_format):
        """
        Break apart the filename and record its secrets
        :param file_name_format: a string representing the value ofa  FileNameFormat enum
        """
        try:
            exploded_filename = self.file_name.split(".")[0].split("_")    # Remove
            if file_name_format == FileNameFormat.FullyQualified.value:
                if len(exploded_filename) != 6:
                    raise Exception(f"Bad Filename [{self.file_name}] for the file format type [{file_name_format}]")
                self.frame_number = int(exploded_filename[0])
                self.sprite_sheet_id = int(exploded_filename[1])
                self.animation_id = int(exploded_filename[2])
                self.direction = int(exploded_filename[3])
                self.offset_x = int(exploded_filename[4])
                self.offset_y = int(exploded_filename[5])
                self.file_name_type = FileNameFormat.FullyQualified
                self.has_animation_details = True
                self.has_offset = True
            elif file_name_format == FileNameFormat.Offsets.value:
                if len(exploded_filename) != 3:
                    raise Exception(f"Bad Filename [{self.file_name}] for the file format type [{file_name_format}]")
                self.frame_number = exploded_filename[0]
                self.offset_x = int(exploded_filename[1])
                self.offset_y = int(exploded_filename[2])
                self.file_name_type = FileNameFormat.Offsets
                self.has_offset = True
            elif file_name_format == FileNameFormat.FrameCounterOnly.value:
                if len(exploded_filename) != 1:
                    raise Exception(f"Bad Filename [{self.file_name}] for the file format type [{file_name_format}]")
                self.frame_number = exploded_filename[0]
                self.file_name_type = FileNameFormat.FrameCounterOnly
            else:
                raise Exception(f"Bad file name format chosen: [{file_name_format}]. HAI8L76J")
        except Exception as e:
            print(f"Unable to parse file name [{e}]. W9JTUO1E")
            self.is_valid = False


class SpriteWorkingFolderInfo:
    """
    Container for some somwe what often referenced data related to the current working folder, and more specifically the fielList that gets
        passed into our constructor
    """
    total_sprites = 0

    min_width = 0
    max_width = 0
    min_height = 0
    max_height = 0

    min_width_with_offset = 0
    max_width_with_offset = 0
    min_height_with_offset = 0
    max_height_with_offset = 0

    min_offset_x = 0
    min_offset_y = 0
    max_offset_x = 0
    max_offset_y = 0


    def __init__(self, fileList):
        self.total_sprites = len(fileList)
        self._calculate_aggregate_sprite_data(fileList)

    def _calculate_aggregate_sprite_data(self, fileList):
        """
        loop over imgs and calculate min/max data, and other thinsg like this
        """
        for sprite in fileList:
            ## min/max height and width
            if sprite.img_width <= self.min_width or self.min_width == 0:
                self.min_width = sprite.img_width
            if sprite.img_width >= self.max_width or self.max_width == 0:
                self.max_width = sprite.img_width
            if sprite.img_height <= self.min_height or self.min_height == 0:
                self.min_height = sprite.img_height
            if sprite.img_height >= self.max_height or self.max_height == 0:
                self.max_height = sprite.img_height

            ## Min/max offsets
            if sprite.has_offset:
                if sprite.offset_x <= self.min_offset_x or self.min_offset_x == 0:
                    self.min_offset_x = sprite.offset_x
                if sprite.offset_x > self.max_offset_x or self.max_offset_x == 0:
                    self.max_offset_x = sprite.offset_x
                if sprite.offset_y <= self.min_offset_y or self.min_offset_y == 0:
                    self.min_offset_y = sprite.offset_y
                if sprite.offset_y > self.max_offset_y or self.min_offset_y == 0:
                    self.max_offset_y = sprite.offset_y

                # calc size while considering offset
                if sprite.img_width + abs(sprite.offset_x) <= self.min_width_with_offset or self.min_width_with_offset == 0:
                    self.min_width_with_offset = sprite.img_width + abs(sprite.offset_x)
                if sprite.img_width + abs(sprite.offset_x) >= self.max_width_with_offset or self.max_width_with_offset == 0:
                    self.min_width_with_offset = sprite.img_width + abs(sprite.offset_x)
                if sprite.img_height + abs(sprite.offset_y) <= self.min_height_with_offset or self.min_height_with_offset == 0:
                    self.min_height_with_offset = sprite.img_height + abs(sprite.offset_y)
                if sprite.img_height + abs(sprite.offset_y) >= self.max_height_with_offset or self.max_height_with_offset == 0:
                    self.min_height_with_offset = sprite.img_height + abs(sprite.offset_y)


class SpriteSheetInfo:
    # If using offset, we need to keep track of the sprite width/height separately. Ends up being max width/height from folder summary, but maybe useful to have here as well
    sprite_width = 0
    sprite_height = 0
    # Req'd because some offsets are negative and our offset origin has to allow that so we dont bleed into another tile
    sprite_origin_offset_x = 0
    sprite_origin_offset_y = 0
    # Tile Info
    tile_width = 0
    tile_height = 0

    # Sprite Sheet Info
    ss_rows = 0
    ss_cols = 0
    ss_width_px = 0
    ss_height_px = 0

    current_settings = None
    current_folder_summary = None

    # Drawing information so that 'next draw position' can be requested from us
    current_row = 0
    current_col = 0

    # handy to keep track of the tile # we are on
    current_tile_count = 0

    # The current position in the sprite sheet (top left corner of tile)  Changes with each request to 'get_next_draw_pos'
    _pos_x = 0
    _pos_y = 0

    # The current draw position. Changes with each request to 'get_next_draw_pos'.
    _draw_x = 0
    _draw_y = 0

    def get_summary(self):
        return_val = {
            "tile_size_px": str((self.tile_width, self.tile_height)),
            "total_tiles": self.current_folder_summary.total_sprites,
            "row_col_counts": str((self.ss_rows, self.ss_cols, )),
            "spite_sheet_size_px": str((self.ss_width_px, self.ss_height_px)),
            "smallest_sprite_size_px": str((self.current_folder_summary.min_width, self.current_folder_summary.min_height,)),
            "largest_sprite_size_px": str((self.current_folder_summary.max_width, self.current_folder_summary.max_height,)),
            "smallest_offsets_x_y": str((self.current_folder_summary.min_offset_x, self.current_folder_summary.min_offset_y)),
            "largest_offsets_x_y": str((self.current_folder_summary.max_offset_x, self.current_folder_summary.max_offset_y,)),
            "sprite_origin": str((self.sprite_origin_offset_x, self.sprite_origin_offset_y)),
        }
        return return_val

    def __init__(self, curr_settings, curr_folder_summary):
        self.current_settings = curr_settings
        self.current_folder_summary = curr_folder_summary

        self.calc_tile_dimensions()
        self.calc_ss_dimensions()

    def get_next_draw_pos(self, spritefile):
        """
        Keeps track of where we are on the sprite sheet file
        This is the draw position after takign into account sprite offset and alignment
        :param spritefile:
        :return:
        """
        # Move our position to the top left of the next tile
        self.increment_tile_position()
        # center, top, top left, etc.
        self.align_spritefile_on_tile(spritefile)
        # Applies any desired offset.
        self.apply_sprite_offset(spritefile)
        return self._draw_x, self._draw_y

    def get_current_tile_position(self):
        """
        Current tile position before considering offset
        :return:
        """
        return self._pos_x, self._pos_y

    def calc_tile_dimensions(self):
        # set/reset some variables
        self.sprite_width = self.current_folder_summary.max_width
        self.sprite_height = self.current_folder_summary.max_height
        self.sprite_origin_offset_x = 0
        self.sprite_origin_offset_y = 0

        # If asked, auto calc tile size, extra considerations if we are applying offsets
        if self.current_settings["SpriteTabSettings"]["TileSizeAutoCalc"]:
            self.tile_width = self.current_folder_summary.max_width
            self.tile_height = self.current_folder_summary.max_height
            if self.current_settings["SpriteTabSettings"]["TileSizeApplyOffset"]:
                self.tile_width = self.current_folder_summary.max_width_with_offset
                self.tile_height = self.current_folder_summary.max_height_with_offset
        else:
            self.tile_width = int(self.current_settings["SpriteTabSettings"]["TileSizeWidth"])
            self.tile_height = int(self.current_settings["SpriteTabSettings"]["TileSizeHeight"])

        if self.current_settings["SpriteTabSettings"]["TileSizeApplyOffset"]:
            if self.current_settings["SpriteTabSettings"]["SpriteOffsetOriginAutoCalc"]:
                # Adjust sprite draw origin (from top left of sprite size) w/in the tile to make sure offset will fit
                self.sprite_origin_offset_x = abs(self.current_folder_summary.min_offset_x)
                self.sprite_origin_offset_y = abs(self.current_folder_summary.min_offset_y)
            else:
                self.sprite_origin_offset_x = int(self.current_settings["SpriteTabSettings"]["SpriteOffsetOriginX"])
                self.sprite_origin_offset_y = int(self.current_settings["SpriteTabSettings"]["SpriteOffsetOriginY"])

        # If someone chooses a discrete tile size and also has 'make sprite sheet square' selected, we might override their choice in favor of being sqr
        if self.current_settings["SpritesheetTabSettings"]["MakeSpriteSheetSquare"]:
            if self.tile_width > self.tile_height:
                self.tile_height = self.tile_width
            else:
                self.tile_width = self.tile_height

    def calc_ss_dimensions(self):
        # Find our sprite sheet dimensions
        if self.current_settings["SpritesheetTabSettings"]["MakeSpriteSheetSquare"]:
            self.ss_rows = math.ceil(math.sqrt(self.current_folder_summary.total_sprites))
            self.ss_cols = self.ss_rows   # make square
        else:
            self.ss_rows = math.ceil(math.sqrt(self.current_folder_summary.total_sprites))
            self.ss_cols = math.floor(math.sqrt(self.current_folder_summary.total_sprites))
        self.ss_width_px = self.ss_rows * self.tile_width
        self.ss_height_px = self.ss_cols * self.tile_height

    def increment_tile_position(self):
        """
        Increments our point on the sprite sheet, tile by tile, setting position,
            keeping the correct number of cols & rows
        """
        # Set our draw position on the sprite sheet
        self._pos_x = self.current_col*self.tile_width
        self._pos_y = self.current_row*self.tile_height
        # Reset our draw position - offset is 0 if no offset, so easier to just always add
        self._draw_x = self._pos_x
        self._draw_y = self._pos_y

        # Calc next col
        if (self.current_col+1) % self.ss_cols == 0 and self.current_col != 0:
            self.current_col = 0
            self.current_row += 1
        else:
            self.current_col += 1

        self.current_tile_count += 1

    def align_spritefile_on_tile(self, spritefile):
        """
        Based on the user's selection we need to correctly calculate a draw position to align the sprite within the tile
        If the sprite is the same size as the tile this doesn't do much.
        :param spritefile: SpriteFileInfo
        """
        # No work to do
        if spritefile.img_width == self.tile_width and spritefile.img_height == self.tile_height:
            return

        # If applying offset, we want to concern the alignment to the individual sprite w/in the max sprite size. If not, w/ want to align within the entire tile
        if self.current_settings["SpriteTabSettings"]["TileSizeApplyOffset"]:
            _working_width = self.sprite_width
            _working_height = self.sprite_height
        else:
            # If not using an offset we want to be able to align the current sprite w/in the tile
            _working_width = self.tile_width
            _working_height = self.tile_height

        # Set our internal 'draw position variables' after aligning them w/in the tile
        if self.current_settings["SpriteTabSettings"]["SpriteAlignmentType"] == SpriteTileAlignment.Center.value:
            self._draw_x += int(round((_working_width-spritefile.img_width)/2, 0))
            self._draw_y += int(round((_working_height-spritefile.img_height)/2, 0))
        elif self.current_settings["SpriteTabSettings"]["SpriteAlignmentType"] == SpriteTileAlignment.N.value:
            self._draw_x += int(round((_working_width-spritefile.img_width)/2, 0))
            self._draw_y = self._draw_y
        elif self.current_settings["SpriteTabSettings"]["SpriteAlignmentType"] == SpriteTileAlignment.NE.value:
            self._draw_x += (_working_width-spritefile.img_width)
            self._draw_y = self._draw_y
        elif self.current_settings["SpriteTabSettings"]["SpriteAlignmentType"] == SpriteTileAlignment.E.value:
            self._draw_x += (_working_width-spritefile.img_width)
            self._draw_y += int(round((_working_height-spritefile.img_height)/2, 0))
        elif self.current_settings["SpriteTabSettings"]["SpriteAlignmentType"] == SpriteTileAlignment.SE.value:
            self._draw_x += (_working_width-spritefile.img_width)
            self._draw_y += (_working_height-spritefile.img_height)
        elif self.current_settings["SpriteTabSettings"]["SpriteAlignmentType"] == SpriteTileAlignment.S.value:
            self._draw_x += int(round((_working_width-spritefile.img_width)/2, 0))
            self._draw_y += (_working_height-spritefile.img_height)
        elif self.current_settings["SpriteTabSettings"]["SpriteAlignmentType"] == SpriteTileAlignment.SW.value:
            self._draw_x = self._draw_x
            self._draw_y += (_working_height-spritefile.img_height)
        elif self.current_settings["SpriteTabSettings"]["SpriteAlignmentType"] == SpriteTileAlignment.W.value:
            self._draw_x = self._draw_x
            self._draw_y += int(round((_working_height-spritefile.img_height)/2, 0))
        elif self.current_settings["SpriteTabSettings"]["SpriteAlignmentType"] == SpriteTileAlignment.NW.value:
            self._draw_x = self._draw_x
            self._draw_y = self._draw_y

    def apply_sprite_offset(self, spritefile):
        """
        Considers if the user wants to apply tile offset, and if the sprite has an offset, and then applies it or not
        can raise and exception for sprites bleeding out of their tiles
        Always acts as offset from the top left
        :param spritefile: SpriteFileInfo
        """
        # Take into account the tile offset
        if spritefile.has_offset and self.current_settings["SpriteTabSettings"]["TileSizeApplyOffset"]:
            # Need to consider offser origin ehre
            self._draw_y += self.sprite_origin_offset_y - spritefile.offset_y
            self._draw_x += self.sprite_origin_offset_x - spritefile.offset_x
            # If the sprite will bleed outside the current tile we will notice
            if self._draw_x > self._pos_x + self.tile_width or self._draw_y > self._pos_y + self.tile_height:
                if not self.current_settings["SpriteTabSettings"]["IgnoreOversizedSprites"]:
                    raise Exception("Tile out of bounds. WWNV6855")
                else:
                    print(f"Ignoring the fact that you're placing a sprite outside of its tile at row: [{self.current_row}] col: [{self.current_col}] QAL90QSA")




