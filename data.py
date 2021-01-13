import pandas as pd
import logging

# logging
logger = logging.getLogger(__name__)

class data:
    def __init__(self, csv_file):
        try:
            self.csv_file = csv_file
            self.roster = pd.read_csv(self.csv_file, index_col=False)
            self.roster.set_index("ID", inplace=True)
        except Exception as e:
            logger.critical('''Csv was not read and/or "ID" index was not set Error: ''' + str(e))
        
    def getdata(self):
        try:
            pd.set_option("display.max_rows", None)
            return self.roster
        except Exception as e:
            logger.critical("Cannot display data. Error: " + str(e))
    
    def setdata(self, csv_file):
        try:
            self.csv_file = csv_file
            self.roster = pd.read_csv(self.csv_file, index_col=False)
            self.roster.set_index("ID", inplace=True)
            self.roster.to_csv(self.csv_file)
        except Exception as e:
            logger.critical("Cannot set data. Error: " + str(e))
    
    def isInServer(self, studentid):
        try:
            studentinfo = self.roster.loc[studentid].values.tolist()
            return str(studentinfo[len(studentinfo)-1]) == "True"
        except Exception as e:
            logger.critical("Cannot get inServer. Error: " + str(e))

    def auth(self, message):
        try:
            return message in self.roster.index
        except Exception as e:
            logger.critical("Cannot authenticate. Error: " + str(e))
            
    def addDiscordId(self, studentid, author):
        try:
            self.roster.at[studentid, "DiscordID"] = author
            self.roster.to_csv(self.csv_file)
        except Exception as e:
            logger.critical("Cannot add DiscordID. Error: " + str(e))

    def addToServer(self, studentid):
        try:
            self.roster.at[studentid, "inServer"] = True
            self.roster.to_csv(self.csv_file)
        except Exception as e:
            logger.critical("Cannot add to inServer. Error: " + str(e))
            
    def discordidexists(self, author):
        try:
            self.roster = pd.read_csv(self.csv_file, index_col=False)
            self.roster.set_index("ID", inplace=True)
            return author in self.roster["DiscordID"].tolist()
        except Exception as e:
            logger.critical("Cannot get if DiscordID exists. Error: " + str(e))
    
    def removediscordid(self, author):
        try:
            self.roster["DiscordID"].replace(str(author), "none", inplace=True)
            self.roster.to_csv(self.csv_file)
        except Exception as e:
            logger.critical("Could not remove DiscordID from database. Error: " + str(e))
    
    def removeInServer(self, author):
        try:
            authorindex = self.roster.index[self.roster['DiscordID'] == str(author)].tolist()[0]
            self.roster.at[authorindex, "inServer"] = False
            self.roster.to_csv(self.csv_file)
        except Exception as e:
            logger.critical("Cannot remove inServer. Error: " + str(e))
        
    def getStuArray(self, studentid):
        try:
            studentinfo = self.roster.loc[studentid].values.tolist()
            return studentinfo
        except Exception as e:
            logger.critical("Could not get the array of StudentID row info and return it. Error: " + str(e))

    def getFullName(self, studentid):
        try:
            studentinfo = self.roster.loc[studentid].values.tolist()
            return studentinfo[1] + " " + studentinfo[0]
        except Exception as e:
            logger.critical("Cannot get full name. Error: " + str(e))