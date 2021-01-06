import pandas as pd
import os.path


class transformer:
    def __init__(self, xlsx_file):
        self.xlsx_file = pd.read_excel(xlsx_file)
        global csvname
        csvname = xlsx_file[:-4] + "csv"
        global dynamic_path
        dynamic_path = os.path.dirname(os.path.abspath(__file__))
        
    def updatecsv(self):
        self.xlsx_file.to_csv(f"{dynamic_path}\{csvname}", index=None, header=True)
    
    def formatcsv(self):
        csv_file = csvname
        pandascsv = pd.read_csv(csv_file, index_col=False)
        pandascsv.columns = ["ID", "None", "LastName", "FirstName"]
        del pandascsv["None"]
        pandascsv["Role"] = "None"
        pandascsv["DiscordID"] = "none"
        pandascsv["inServer"] = "False"
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
        
        
        
        
    
test = transformer("Tennis Roster Excel.xlsx")
test.updatecsv()
test.formatcsv()