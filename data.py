import pandas as pd

class data:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.roster = pd.read_csv(self.csv_file, index_col=False)
        self.roster.set_index("ID", inplace=True)
        
    def getdata(self):
        pd.set_option("display.max_rows", None)
        return self.roster
    
    def setdata(self, csv_file):
        self.csv_file = csv_file
        self.roster = pd.read_csv(self.csv_file, index_col=False)
        self.roster.set_index("ID", inplace=True)
        self.roster.to_csv(self.csv_file)
    
    def isInServer(self, studentid):
        studentinfo = self.roster.loc[studentid].values.tolist()
        return str(studentinfo[len(studentinfo)-1]) == "True"
    
    # def turnTrue(self, studentid):
    #     self.roster["inServer"][studentid] != "True"

    def auth(self, message):
        return message in self.roster.index
            
    def addDiscordId(self, studentid, author):
        self.roster.at[studentid, "DiscordID"] = author
        self.roster.to_csv(self.csv_file)

    def addToServer(self, studentid):
        self.roster.at[studentid, "inServer"] = True
        self.roster.to_csv(self.csv_file)
        
    def discordidexists(self, author):
        self.roster = pd.read_csv(self.csv_file, index_col=False)
        self.roster.set_index("ID", inplace=True)
        return author in self.roster["DiscordID"].tolist()
    
    def removediscordid(self, author):
        self.roster["DiscordID"].replace(str(author), "none", inplace=True)
        self.roster.to_csv(self.csv_file)
    
    def removeInServer(self, author):
        authorindex = self.roster.index[self.roster['DiscordID'] == str(author)].tolist()[0]
        self.roster.at[authorindex, "inServer"] = False
        self.roster.to_csv(self.csv_file)
        
    def getStuArray(self, studentid):
        studentinfo = self.roster.loc[studentid].values.tolist()
        return studentinfo

    def getFullName(self, studentid):
        studentinfo = self.roster.loc[studentid].values.tolist()
        return studentinfo[1] + " " + studentinfo[0]