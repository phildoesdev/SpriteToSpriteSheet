from os import path
import json
import time


class StateManager:
    """
    Manages the state file that remembers all settings. Very nice.
    """
    # Default state file location
    StateFileDirPath = ""
    StateFileName = "settings.state"

    CurrentState = {}

    # last unix timestamp we saved
    LastUpdated = 0

    IsSaving = False


    def __init__(self, stateFileDir="./"):
        if not path.exists(stateFileDir):
            return
        self.StateFileDirPath = stateFileDir

    def save(self, settings):
        self.CurrentState = settings
        self._save_state_to_file()
        self.LastUpdated = time.time()

    def load(self):
        return self._load_state_from_file()

    def _save_state_to_file(self):
        # if self.IsSaving:
        #     return
        self.IsSaving = True
        with open(self.StateFileDirPath+self.StateFileName, mode="w") as sf:
            json.dump(self.CurrentState, sf)
        self.IsSaving = False

    def _load_state_from_file(self):
        filePath = self.StateFileDirPath+self.StateFileName
        if not path.isfile(filePath):
            return None

        with open(filePath, mode="r") as sf:
            output = json.load(sf)
        return output
