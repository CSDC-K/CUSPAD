# Made By CSDC-K Kuzey

import customtkinter
import CTkMenuBar
import json
import sys
import os

from customtkinter import filedialog

with open("Config.json", "r") as configFile:
    configs = json.load(configFile)

if configs["ActiveTheme"] == "DARK":
    ActiveTheme = "DARK"
elif configs["ActiveTheme"] == "LIGHT":
    ActiveTheme = "LIGHT"



"#e0e0e0"


class NotePad:
    def __init__(self):
        self.config = configs[ActiveTheme]
        self.NPad = customtkinter.CTk(fg_color=self.config["PageColor"])
        self.NPad.title("NotePad")
        self.NPad.geometry("960x620")
        self.NPad.resizable(False, False)

        self.NPad.grid_rowconfigure(0, weight=0) 
        self.NPad.grid_rowconfigure(1, weight=1)
        self.NPad.grid_columnconfigure(0, weight=1)

        # auto binds:

        self.NPad.bind("<Control-plus>", lambda event: self.zoomin())
        self.NPad.bind("<Control-minus>", lambda event: self.zoomout())
        self.NPad.bind("<Control-q>", lambda event: self.quit())
        self.NPad.bind("<Control-t>", lambda event: ThemeEditor(self.NPad))
        self.NPad.bind("<Control-Shift-s>", lambda event: self.saveFileAs())
        self.NPad.bind("<Control-s>", lambda event: self.saveFile())
        self.NPad.bind("<Control-o>", lambda event: self.openFile())
        self.NPad.bind("<Control-n>", lambda event: self.newFile())


        

        NPadMenuBar = CTkMenuBar.CTkMenuBar(master=self.NPad,bg_color=self.config["MenuBarColor"])
        NPadMenuBar.grid(row=0, column=0, sticky="ew")

        info_label = customtkinter.CTkLabel(
            NPadMenuBar, 
            text="Cus-Pad v1.0", 
            text_color=self.config["TopBarTitleColor"],
            font=("Default", 16,"bold")
        )
        info_label.grid(row=0, column=99, sticky="e", padx=250,pady=(1,0))

        self.fileinfo_label = customtkinter.CTkLabel(
            NPadMenuBar, 
            text="", 
            text_color=self.config["TopBarTitleColor"],
            font=("Default", 16,"bold")
        )
        self.fileinfo_label.grid(row=0, column=100, sticky="e", padx=75,pady=(1,0))

        fileMenu = NPadMenuBar.add_cascade(text="File",text_color=self.config["MenuBarTextColor"],hover_color=self.config["MenuBarHoverColor"],font=("Default", 16,"bold"))
        editMenu = NPadMenuBar.add_cascade(text="Edit",text_color=self.config["MenuBarTextColor"],hover_color=self.config["MenuBarHoverColor"],font=("Default", 16,"bold"))
        viewMenu = NPadMenuBar.add_cascade(text="View",text_color=self.config["MenuBarTextColor"],hover_color=self.config["MenuBarHoverColor"],font=("Default", 16,"bold"))
        aboutMenu = NPadMenuBar.add_cascade(text="About",text_color=self.config["MenuBarTextColor"],hover_color=self.config["MenuBarHoverColor"],font=("Default", 16,"bold"))


        fileDownCase = CTkMenuBar.CustomDropdownMenu(widget=fileMenu, fg_color=self.config["DropDownColor"],text_color=self.config["DropDownTextColor"],hover_color=self.config["DropDownHoverColor"],
                                                     bg_color=self.config["DropDownColor"],corner_radius=configs["DropDownBorderRadius"])
        editDownCase = CTkMenuBar.CustomDropdownMenu(widget=editMenu, fg_color=self.config["DropDownColor"],text_color=self.config["DropDownTextColor"],hover_color=self.config["DropDownHoverColor"],
                                                     bg_color=self.config["DropDownColor"],corner_radius=configs["DropDownBorderRadius"])    
        viewDownCase = CTkMenuBar.CustomDropdownMenu(widget=viewMenu, fg_color=self.config["DropDownColor"],text_color=self.config["DropDownTextColor"],hover_color=self.config["DropDownHoverColor"],
                                                     bg_color=self.config["DropDownColor"],corner_radius=configs["DropDownBorderRadius"])      
        aboutDownCase = CTkMenuBar.CustomDropdownMenu(widget=aboutMenu, fg_color=self.config["DropDownColor"],text_color=self.config["DropDownTextColor"],hover_color=self.config["DropDownHoverColor"],
                                                     bg_color=self.config["DropDownColor"],corner_radius=configs["DropDownBorderRadius"])      


        fileDownCase.add_option(option="New File\t\t\tCTRL+N", command=self.newFile)
        fileDownCase.add_option(option="Open File\t\t\tCTRL+O", command=self.openFile)
        fileDownCase.add_option(option="Save File\t\t\tCTRL+S", command=self.saveFile)
        fileDownCase.add_option(option="Save File as\t\tCTRL+SHIFT+S", command=self.saveFileAs)
        fileDownCase.add_option(option="Quit File\t\t\tCTRL+Q", command=self.quit)


        editDownCase.add_option(option="Undo\t\tCTRL+Z", command=self.Undo)
        editDownCase.add_option(option="Redo\t\tCTRL+Y", command=self.Redo)
        editDownCase.add_option(option="Cut\t\tCTRL+X", command=self.cut)
        editDownCase.add_option(option="Copy\t\tCTRL+C", command=self.copy)
        editDownCase.add_option(option="Paste\t\tCTRL+V", command=self.paste)
        editDownCase.add_option(option="Select All\t\tCTRL+A", command=self.selectall)

        viewDownCase.add_option(option="Theme\t\t\tCTRL+T", command=lambda:ThemeEditor(self.NPad))
        viewDownCase.add_option(option="Zoom In\t\t\tCTRL +", command=self.zoomin)
        viewDownCase.add_option(option="Zoom Out\t\tCTRL -", command=self.zoomout)

        aboutDownCase.add_option(option="About", command=lambda:About(self.NPad))


        self.NPadTextBox = customtkinter.CTkTextbox(self.NPad,fg_color=self.config["FrameColor"],width=910,height=570,border_spacing=0,text_color=self.config["TextColor"],
                                               font=(configs["Font"], configs["FontSize"], configs["FontB"]),
                                               undo=True)
        self.NPadTextBox.grid(row=1, column=0, padx=25, pady=(20,10), sticky="nsew")

        self.NPad.mainloop()

    # FILES

    def openFile(self):
        file_path = filedialog.askopenfilename(
            title="Open File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.NPadTextBox.delete("1.0", "end")
            self.NPadTextBox.insert("1.0", content)
            file_name = os.path.basename(file_path)
            self.fileinfo_label.configure(text=file_name)

            self.openedFilePath = file_path

    def saveFile(self):
        if self.openedFilePath:
            try:
                with open(self.openedFilePath, "w", encoding="utf-8") as f:
                    f.write(self.NPadTextBox.get("1.0", "end-1c"))
            except Exception as e:
                print(e)

        elif self.openedFilePath is None:
            self.saveFileAs()

    def saveFileAs(self):
        file_path = filedialog.asksaveasfilename(
            title="Save As",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.NPadTextBox.get("1.0", "end-1c"))
            self.openedFilePath = file_path
            file_name = os.path.basename(file_path)
            self.fileinfo_label.configure(text=file_name)

    def newFile(self):
        self.NPadTextBox.delete("1.0", "end")
        self.openedFilePath = None
        self.fileinfo_label.configure(text="Not Named File")




    def quit(self):
        self.NPadTextBox.delete("1.0", "end")
        self.openedFilePath = None
        self.fileinfo_label.configure(text="")
        


    # EDITS
    def Undo(self):
        self.NPadTextBox.edit_undo()
    def Redo(self):
        self.NPadTextBox.edit_redo()
    def cut(self):
        selected = self.NPadTextBox.get("sel.first", "sel.last")
        self.NPad.clipboard_clear()
        self.NPad.clipboard_append(selected)
        self.NPadTextBox.delete("sel.first", "sel.last")
    def copy(self):
        selected = self.NPadTextBox.get("sel.first", "sel.last")
        self.NPad.clipboard_clear()
        self.NPad.clipboard_append(selected)
    def paste(self):
        clipboard_data = self.NPad.clipboard_get()
        self.NPadTextBox.insert("insert", clipboard_data)
    def selectall(self):
        self.NPadTextBox.tag_add("sel", "1.0", "end-1c")

    # VIEWS

    def zoomin(self):
        configs["FontSize"] = configs["FontSize"] + 1
        self.NPadTextBox.configure(font=(configs["Font"], configs["FontSize"], configs["FontB"]))

    def zoomout(self):
        configs["FontSize"] = configs["FontSize"] - 1
        self.NPadTextBox.configure(font=(configs["Font"], configs["FontSize"], configs["FontB"]))



class ThemeEditor:
    def __init__(self, parent):

        self.ThemePage = customtkinter.CTkToplevel(parent)
        self.ThemePage.geometry("400x300")
        self.ThemePage.resizable(False, False)
        self.ThemePage.title("Theme Editor")
        self.ThemePage.grab_set()

class About:
    def __init__(self, parent):

        self.AboutPage = customtkinter.CTkToplevel(parent)
        self.AboutPage.geometry("400x300")
        self.AboutPage.resizable(False, False)
        self.AboutPage.title("About")

        title = customtkinter.CTkLabel(self.AboutPage,text="CUSPAD 1.0",font=("Helvetica",40,"bold"),text_color=configs[ActiveTheme]["TextColor"])
        title.place(x=85,y=75)

        label1 = customtkinter.CTkLabel(self.AboutPage,text="Made By CSDC-K Kuzey", font=("Default",18,"italic"),text_color=configs[ActiveTheme]["TextColor"])
        label1.place(x=105,y=150)  


if __name__ == "__main__":
    app = NotePad()
