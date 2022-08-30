from datetime import date

class File:
    def __init__(self, file_name: str, isBorrowed: bool = False, date: str = None, user: str = None):
        self.file_name = file_name
        self.isBorrowed = isBorrowed
        self.date = date
        self.user = user
    
    def getFileName(self):
        return self.file_name

    def getIsBorrowed(self):
        return self.isBorrowed

    def getDate(self):
        return self.date

    def getUser(self):
        return self.user
            
    def toggleIsBorrowed(self):
        self.isBorrowed = not self.isBorrowed
    
    def returnFile(self):
        if self.isBorrowed == True:
            today = date.today()
            currDate = today.strftime('%m/%d/%Y')
            self.date = "Returned:"+currDate
            self.user = ""
            self.toggleIsBorrowed()
        else:
            print("Unable to complete action, file is already returned")

    def borrowFile(self, user: str):
        if self.isBorrowed == False:
            today = date.today()
            currDate = today.strftime('%m/%d/%Y')
            self.date = "Borrowed:"+currDate
            self.user = user
            self.toggleIsBorrowed()
        else:
            print("Unable to complete action, file is already borrowed.")

    def __str__(self):
        return f"File Name: {self.getFileName()}    isBorrowed: {self.getIsBorrowed()}   Date: {self.getDate()}  User: {self.getUser()}"

    def recordString(self):
        return f"{self.getFileName()},{self.getIsBorrowed()},{self.getDate()},{self.getUser()}"


# Write/Overwrite a file with the information
with open("file_logs.txt", "r") as rf:
    
    # Search for file, problem if not exact FileName.
    print("Enter the file name you are looking for. (No spaces)")
    search = input("File Name: ").strip()
    file_found = False
    data = rf.readlines()
    index, foundData = None, None

    print(f"All Data: {data}")

    for line in range(len(data)):
        if search in data[line]:
            foundData = data[line].split(",")
            index = line
            file_found = True
            print(f"Found Data: {foundData}")

    if file_found == True:
            print(f"File '{search}' exists. What would you like to do?")
            print("0) Cancel")
            print("1) Borrow")
            print("2) Return")
    else:
            print(f"File '{search}' doesn't exist. What would you like to do?")
            print("0) Cancel")
            print("1) Create record and borrow")
            print("2) Create record and return")

    action = input("Action: ")

    while action.strip().isdigit() == False or (int(action) < 0 or int(action) > 2):
        print("Invalid input.")
        print("0) Cancel")
        print("1) Borrow")
        print("2) Return")
        action = input("Action: ")
    
    if int(action) == 0:
        exit()

    # Create file object
    # ['c-4694', 'False', 'Returned:08/30/2022', 'Tim\n']

    if file_found:
        fileName = foundData[0]
        fileBorrowed = (foundData[1] == "True") # If foundData[1] == "True", returns bool
        fileDate = foundData[2]
        fileUser = foundData[3].removesuffix("\n")
        newFile = File(fileName, fileBorrowed, fileDate, fileUser)

        print(f"File found new file: {newFile}")
    else:
        newFile = File(search)
        print(f"No found new file: {newFile}")

    if int(action) == 1 and file_found:
        print("Who is borrowing the file?")
        name = input("Name: ")
        newFile.borrowFile(name)
        data[index] = newFile.recordString()+"\n"
        print(f"Before Writing: {data}")

    if int(action) == 1 and not file_found:
        print("Who is borrowing the file?")
        name = input("Name: ")
        newFile.borrowFile(name)
        data[len(data)-1] = data[len(data)-1].removesuffix("\n") +"\n" # Update last index with new line
        data.append(newFile.recordString()+"\n")
        print(f"Before Writing: {data}")

    if int(action) == 2 and file_found:
        newFile.returnFile()
        data[index] = newFile.recordString()+"\n"
        print(f"Before Writing: {data}")

    if int(action) == 2 and not file_found:
        newFile.toggleIsBorrowed()
        newFile.returnFile()
        data[len(data)-1] = data[len(data)-1].removesuffix("\n")+"\n" # Update last index with new line
        data.append(newFile.recordString()+"\n")
        print(f"Before Writing: {data}")

     
    
    with open("file_logs.txt", "w") as wf:
        wf.writelines(data)
    rf.seek(0)
    print(f"After Writing: {rf.readlines()}")

