#AH Computing project main script
#Hashim Iqbal

#This file acts as the front-end of the implementation for the app, while the Weather module acts as the back-end process.

'''
Dependencies:
   Tkinter for creating the GUI and all its associated elements.
   Weather class to call methods and separate code more distinctly (The 'back-end' of the implementation)
'''
import time
from tkinter import *
from tkinter import messagebox, filedialog
from PIL import ImageTk, Image
from weather import Weather

#Our Application class which will handle the UI and all other front-end processes.
#This will hold the main method, mainScreen(), as well as all the button functions.
class Application:
    #Our constructor method will take an argument for the tkinter window, and initialise the general attributes of the window, which won't really be changed.
    #This will also instantiate our weather object, giving us access to the methods within the class.
    def __init__(self, master):
        self.master = master
        self.master.geometry('450x350')
        self.master.resizable(0, 0)
        self.master.title('AH Computing Project - Weather app')
        self.master.configure(bg='#181818')
        self.master.iconbitmap('./AppIcon.ico')

        #Create weather object and pass our tkinter object as the parameter.
        self.weather = Weather()

        #Create our frame, where all our elements will be rendered.
        self.MainFrame = Frame(self.master, width=200, height=200, bg='#181818')
        self.MainFrame.pack()

    #Method to display the welcome screen and the entry fields for fetchData() method.
    def mainScreen(self):

        for child in self.MainFrame.winfo_children():
            child.destroy()

        self.title = Label(self.MainFrame, text='Weather Information Interface', bg='#181818', fg='White', font=('Calibri', 25, 'bold'))
        self.title.pack(pady=(15, 0))

        self.subtitle = Label(self.MainFrame, text='Created by Hashim Iqbal', bg='#181818', fg='White', font=('Calibri', 12, 'italic'))
        self.subtitle.pack(pady=(5, 105))

        self.RequestButton = Button(self.MainFrame, text='Fetch Weather for a city', command=self.entryScreen, height=3, width=20)
        self.RequestButton.pack(pady=(0, 15))

        self.DatabaseButton = Button(self.MainFrame, text='Database connection', command=self.Setup, height=3, width=20)
        self.DatabaseButton.pack()


    #This screen will be for entering in the city for which we want weather info.
    def entryScreen(self):

        #Clear frame of mainscreen elements.
        for child in self.MainFrame.winfo_children():
            child.destroy()

        self.CityLabel = Label(self.MainFrame, text='Please enter the name of the city you want weather for.', bg='#181818', fg='White')
        self.CityLabel.pack(pady=(15, 10))

        self.CityEntry = Entry(self.MainFrame, font=('Calibri', 14, 'bold'), bd=3)
        self.CityEntry.pack(pady=(0, 115))

        self.SubmitButton = Button(self.MainFrame, text='Submit', command=self.postData, width=20, height=3)
        self.SubmitButton.pack(pady=(0, 15))

        self.backHome = Button(self.MainFrame, text='Back to home page', command=self.mainScreen, width=20, height=3)
        self.backHome.pack()


    #Button method to invoke our method from the other script and pass the data we've entered.
    def postData(self):

        #Invoke our fetchData method to take in the value from our entry box and search for associated weather.
        self.Data = self.weather.fetchData(self.CityEntry.get())

        #Clear frame of mainscreen elements.
        for child in self.MainFrame.winfo_children():
            child.destroy()

        #If the returned value is true, then obviously something is wrong, so send an error message, and redraw r
        if self.Data == False:
            errorMessage = Label(self.MainFrame, text="I'm sorry, I can't find that city, please try again.", fg='Red', bg='#181818')
            errorMessage.pack(pady=(15, 0))

            self.CityLabel = Label(self.MainFrame, text='Please enter the name of the city you want weather for.', bg='#181818', fg='White')
            self.CityLabel.pack(pady=(15, 10))

            self.CityEntry = Entry(self.MainFrame, font=('Calibri', 14, 'bold'), bd=3)
            self.CityEntry.pack(pady=(0, 115))

            self.SubmitButton = Button(self.MainFrame, text='Submit', command=self.postData, width=20, height=3)
            self.SubmitButton.pack(pady=(0, 15))

            self.backHome = Button(self.MainFrame, text='Back to home page', command=self.mainScreen, width=20, height=3)
            self.backHome.pack()

        #Else, show the data to the user. This includes icons.
        else:
            path = f"./Icons/{self.weather.icon}.png"
            image = ImageTk.PhotoImage(Image.open(path))

            imageDisplay = Label(self.MainFrame, image=image, bg='#181818')
            imageDisplay.photo = image
            imageDisplay.pack(pady=(10, 5))

            Label(self.MainFrame, text=f"Country:  {self.Data[0]}", bg="#181818", fg="White", font=('Calibri', 16, 'bold')).pack(anchor=W)
            Label(self.MainFrame, text=f"City:  {self.Data[1]}", bg="#181818", fg="White", font=('Calibri', 16, 'bold')).pack(anchor=W)
            Label(self.MainFrame, text=f"Latitude:  {self.Data[2]}", bg="#181818", fg="White", font=('Calibri', 16, 'bold')).pack(anchor=W)
            Label(self.MainFrame, text=f"Longitude:  {self.Data[3]}", bg="#181818", fg="White", font=('Calibri', 16, 'bold')).pack(anchor=W)
            Label(self.MainFrame, text=f"Temp (°C):  {self.Data[4]}", bg="#181818", fg="White", font=('Calibri', 16, 'bold')).pack(anchor=W)
            Label(self.MainFrame, text=f"Wind Speed (m/s):  {self.Data[5]}", bg="#181818", fg="White", font=('Calibri', 16, 'bold')).pack(anchor=W)
            Label(self.MainFrame, text=f"Description:  {self.Data[6]}", bg="#181818", fg="White", font=('Calibri', 16, 'bold')).pack(anchor=W)

            #After 3 seconds, call the fileWrite function
            self.master.after(3000, self.fileWrite)


    #Will get information for the writeData() method from the user, like if they want to write their data and if so, a file path to write.
    def fileWrite(self):
        #Message box to ask user if they want to write the data to an external .txt file
        AskWrite = messagebox.askyesno('Write to file', 'Do you want to write this data to a .txt file?', icon='question')

        if AskWrite == True:
            #Get filepath to save to through file dialog box
            self.SaveLocation = filedialog.asksaveasfilename(defaultextension='.txt', initialdir='/', title='Save File', filetypes=(('Text Files', '*.txt'), ('All Files', '*.*')))
            if self.SaveLocation:
                #Invoke the writeData() method
                self.weather.writeData(self.SaveLocation)
            else:
                #If the user clicks cancel in the file dialog window, they will be shown a warning that their data won't get written.
                AskCancel = messagebox.showwarning('Write to file', "The data won't be written to a .txt file.")
        else:
            pass

        self.backHome = Button(self.MainFrame, text='Back to home page', command=self.mainScreen, height=3, width=20)
        self.backHome.pack(pady=(20, 0))


    #Methods the database integration relies on before we try connecting to the database.
    def Setup(self):

        for child in self.MainFrame.winfo_children():
            child.destroy()

        #Timing how long the methods are taking to prove they're actually running
        startTime = time.time()
        
        #Call the methods that don't require any user input.
        self.weather.readFile()
        self.weather.sortCities()
        self.weather.populateRecords()

        endTime = time.time()
        print(f"The 3 methods have executed successfully, taking: {endTime - startTime} seconds")

        #Button that will execute the database connection code when clicked.
        self.ConnectButton = Button(self.MainFrame, text='Connect to Database', command=self.ConnectDatabase, width=20, height=3)
        self.ConnectButton.pack(pady=(110, 15))

        self.backHome = Button(self.MainFrame, text='Back to home page', command=self.mainScreen, width=20, height=3)
        self.backHome.pack()

    
    #Runs the database connection code to insert the 1000 cities data into the table.
    def ConnectDatabase(self):

        for child in self.MainFrame.winfo_children():
            child.destroy()
            
        self.Connection = self.weather.databaseConnection()

        if self.Connection == False:
            Label(self.MainFrame, text='Error connecting to database.', bg='#181818', fg='Red').pack(pady=(15, 0))
            Label(self.MainFrame, text='Please ensure the server is active and try again.', bg='#181818', fg='Red').pack()

            #Recreate our connect button if things go wrong.
            self.ConnectButton = Button(self.MainFrame, text='Connect to Database', command=self.ConnectDatabase, width=20, height=3)
            self.ConnectButton.pack(pady=(110, 15))

            self.backHome = Button(self.MainFrame, text='Back to home page', command=self.mainScreen, width=20, height=3)
            self.backHome.pack()
        else:
            Label(self.MainFrame, text=f'Successfully connected to database. Connection ID: {self.Connection}', fg='White', bg='#181818').pack(pady=(10, 0))

            self.backHome = Button(self.MainFrame, text='Back to home page', command=self.mainScreen, width=20, height=3)
            self.backHome.pack(pady=(25, 0))


#If this is the main file, which it is, run the following code.
if __name__ == "__main__":
    #Creating window instance
    master = Tk()
    app = Application(master)
    app.mainScreen()

    #Tells Tkinter that we're done using or referencing the GUI window.
    master.mainloop()