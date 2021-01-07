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
            
    def auth(self, array):
        temparray = array[:]
        # try:
        #     temparray[0] = int(temparray[0])
        # except Exception as e:
        #     print("User ID not an int: " + str(e))
        if len(temparray) == 4 and temparray[0] in self.roster.index:
            try:
                studentinfo = self.roster.loc[temparray[0]].values.tolist()
            except Exception as e:
                print("Nonexisting StudentID: " + str(e))
            studentinfo.pop()
            studentinfo.pop()
            temparray.pop(0)
            studentinfo = [x.lower() for x in studentinfo]
            temparray = [x.lower() for x in temparray]
            if studentinfo == temparray:
                return True
            else:
                return False
        else:
            return False
    
    def adddiscordid(self, studentid, author):
        self.roster.at[int(studentid), "DiscordID"] = author
        self.roster.to_csv(self.csv_file)

    def addToServer(self, studentid):
        self.roster.at[int(studentid), "inServer"] = True
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
        
        # dfb = int(df[df['A']==5].index[0])
        # dfbb = int(df[df['A']==8].index[0])

        # self.roster.at[author, "inServer"] = False
        # self.roster[]
# transformer = transformer.transformer("CV_Tennis_Roster.xlsx")
# transformer.updatecsv()
# transformer.formatcsv()
# data = data("CV_Tennis_Roster.csv")
# print(data.getdata())
# data.removeInServer(790687692752945194)
# print(data.getdata())
# data.adddiscordid(401488, 554442369831796740)
# print(data.getdata())
# # 
# # # print(data.isInServer('401488'))
# message = "402075, Valerie, Arrieta Hidalgo, JVG"
# message_words = message.lower().split(",")
# message_words[1], message_words[2] = message_words[2].capitalize(), message_words[1].capitalize()
# message_words[3] = message_words[3].upper()
# for i in range(len(message_words)):
#     message_words[i] = message_words[i].strip()
# print(message_words)
# 
# print(data.auth(message_words))
            
            
            
            
            
            
            