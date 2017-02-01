# Get data from excel form

import Scr01_Initialization
from Scr01_Initialization import *

def getXlsxData() :
    os.chdir(directoryPath)
    folder_list = os.listdir(directoryPath)
    for folders, sub_folders, file in os.walk(directoryPath):
        for name in file :
            if name.endswith(".xlsx") :
                filename = os.path.join(folders, name)
                wb = openpyxl.load_workbook(filename, data_only=True)
                return wb

if  __name__ == "__main__" :
    os.system("python Scr01_Initialization.py")
    getXlsxData()
    print ("Get data from xlsx file successfully!")