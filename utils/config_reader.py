from configparser import ConfigParser


class Config:
    path: str


    def __init__(self, path: str=".config.ini"):
        self.path = path
    

    def get(self, section: str, param: str)-> str:
        setting = ConfigParser()
        setting.read(self.path)
        return setting[section][param]