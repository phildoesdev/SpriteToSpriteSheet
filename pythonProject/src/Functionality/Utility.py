

class UtilityMethods:
    @staticmethod
    def traverse_folders(src_folder_path, callback_mthd, valid_file_extensions=('.bmp', '.jpg', '.png'), is_rec=False):
        """
        Basic method to traverse a folder and do a callback on specific file types.
        Can be recursive
        Originally got split out this way because there was a fair amount of looping to do, less so now, but still keeping
            split out b/c why not.

        :param src_folder_path:
            Wehre to begin our search
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
                SpriteSheetManager.traverse_folders(_f.path, callback_mthd)