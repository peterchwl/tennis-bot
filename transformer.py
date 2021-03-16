import pandas as pd
import os.path
from os import path
import logging
#yolo

logger = logging.getLogger(__name__)

class transformer:
    def __init__(self, xlsx_file):
        try:
            self.xlsx_file = pd.read_excel(xlsx_file, engine='openpyxl')
            global csvname
            csvname = xlsx_file[:-4] + "csv"
            global dynamic_path
            dynamic_path = os.path.dirname(os.path.abspath(__file__))
        except Exception as e:
            logger.critical("Could not read_excel and/or array positional \
error for xlsx_file[] and/or could not find the dynamic path \
object of which transformer.py is in" + str(e))
        if not path.exists(csvname):
            self.updatecsv()
            self.formatcsv()
        
    def getdata(self):
        try:
            pd.set_option("display.max_rows", None)
            return self.xlsx_file
        except Exception as e:
            logger.critical("Cannot get data. Error: " + str(e))
    
    def setfile(self, xlsx_file):
        self.xlsx_file = pd.read_excel(xlsx_file, engine='openpyxl')
        global csvname
        csvname = xlsx_file[:-4] + "csv"
        global dynamic_path
        dynamic_path = os.path.dirname(os.path.abspath(__file__))
    
    def updatecsv(self):
        self.xlsx_file.to_csv(csvname, index=None, header=True)
    
    def formatcsv(self):
        csv_file = csvname
        pandascsv = pd.read_csv(csv_file, index_col=False)

        pandascsv.columns = ["ID", "None", "LastName", "FirstName"]
        del pandascsv["None"]
        pandascsv["Role"] = "None"
        pandascsv["DiscordID"] = "none"
        pandascsv["inServer"] = "False"
        #data reset problem^
        studentrole = "VG"
        for row in pandascsv.index:
            try:
                id_checker = int(pandascsv["ID"][row])
                pandascsv["Role"][row] = studentrole
            except:
                try:
                    id_checker = str(pandascsv["ID"][row])
                    if id_checker == "JV Girl":
                        studentrole = "JVG"
                    elif id_checker == "Varsity Boy":
                        studentrole = "VB"
                    elif id_checker == "JV Boy":
                        studentrole = "JVB"
                except:    
                    pass
                pandascsv.drop(row, inplace=True)
                
        for row in pandascsv.index:
            namelist = pandascsv["FirstName"][row].split(" ")
            pandascsv["FirstName"][row] = namelist[0]         
                
        pandascsv.set_index("ID", inplace=True)
        pandascsv.to_csv(csv_file)
    
    def getCsvName(self):
        return csvname