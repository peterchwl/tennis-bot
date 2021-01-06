import pandas as pd

class data:
    def __init__(self,csv_file):
        self.csv_file = csv_file
        self.roster = pd.read_csv(self.csv_file, index_col=False)
        self.roster.set_index("ID", inplace=True)
        
    def get_data(self):
        pd.set_option("display.max_rows", None)
        return self.roster
        
    def isInServer(self, studentid):
        studentinfo = self.roster.loc[studentid].values.tolist()
        return studentinfo[-1] == "True"
    
    def turnTrue(self, studentid):
        self.roster["inServer"][studentid] != "True"
            
    def auth(self, array):
        if len(array) == 4 and array[0] in self.roster.index:
            try:
                studentinfo = self.roster.loc[array[0]].values.tolist()
            except Exception as e:
                print("Nonexisting StudentID: " + str(e))
            studentinfo.pop()
            studentinfo.pop()
            array.pop(0)
            studentinfo = [x.lower() for x in studentinfo]
            array = [x.lower() for x in array]
            if studentinfo == array:
                return True
            else:
                return False
        else:
            return False



# transformer = transformer.transformer("DoilsRoster (3).xlsx")
data = data("Tennis Roster Excel.csv")
print(data.get_data())

# print(data.isInServer('401488'))
# print(data.auth(["430482", "Cho", "Troy", "JVB"]))
            
            
            
            
            
            
            
            