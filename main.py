# Made By CSDC-K Kuzey
# V1.2
import customtkinter
import CTkMenuBar
import json
import sys
import os
import time
from threading import Thread
from random import choice
import tkinter as tk

from customtkinter import filedialog

import google.genai as _CallGemini

with open("ThemeConfig.json", "r") as configFile:
    configs = json.load(configFile)

if configs["ActiveTheme"] == "DARK":
    ActiveTheme = "DARK"
elif configs["ActiveTheme"] == "LIGHT":
    ActiveTheme = "LIGHT"

with open("UserConfig.json", "r") as userconfigFile:
    user_configs = json.load(userconfigFile)

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
        

        self.AiFrame = customtkinter.CTkFrame(self.NPad, width=300, height=570, fg_color=self.config["FrameColor"])
        self.AiFrame.place(x=1200, y=40)
        self.aiTitleLabel = customtkinter.CTkLabel(self.AiFrame, text="Ai Chat", font=("Helvetica", 18, "bold"), text_color=self.config["TextColor"])
        self.aiTitleLabel.pack(pady=(10, 5))


        self.chatArea = customtkinter.CTkScrollableFrame(self.AiFrame, width=280, height=455, fg_color="transparent")
        self.chatArea.pack(pady=(5, 5))
        def _on_mouse_wheel(event):
            if event.delta:  # Windows / Mac
                self.chatArea._parent_canvas.yview_scroll(-1*(event.delta//120), "units")
            else:  # Linux (event.num = 4,5 up,down)
                if event.num == 4:
                    self.chatArea._parent_canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    self.chatArea._parent_canvas.yview_scroll(1, "units")

        self.chatArea._parent_canvas.bind_all("<MouseWheel>", _on_mouse_wheel)  # Windows/Mac
        self.chatArea._parent_canvas.bind_all("<Button-4>", _on_mouse_wheel)    # Linux up
        self.chatArea._parent_canvas.bind_all("<Button-5>", _on_mouse_wheel)    # Linux down

        self.input_frame = customtkinter.CTkFrame(self.AiFrame, fg_color="transparent")
        self.input_frame.pack(side="bottom", fill="x", padx=10, pady=(0, 10))
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.msgEntry = customtkinter.CTkEntry(self.input_frame, width=230, height=40, placeholder_text="Bir mesaj yazın...", text_color=self.config["TextColor"], border_width=0)
        self.msgEntry.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        self.msgEntry.bind("<Return>", lambda event=None: self.send_message())

        self.msgButton = customtkinter.CTkButton(self.input_frame, text="Gönder", fg_color=self.config["AiButtonColor"], hover_color=self.config["AiButtonHoverColor"], width=40, height=40, text_color="#FFFFFF", command=self.send_message)
        self.msgButton.grid(row=0, column=1, padx=(5, 0))



        self.add_bubble("Hello! How can i help you?", "ai")

        NPadMenuBar = CTkMenuBar.CTkMenuBar(master=self.NPad,bg_color=self.config["MenuBarColor"])
        NPadMenuBar.grid(row=0, column=0, sticky="ew")

        info_label = customtkinter.CTkLabel(
            NPadMenuBar, 
            text="Cus-Pad v1.2", 
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
        aiMenu = NPadMenuBar.add_cascade(text="Plugins",text_color=self.config["MenuBarTextColor"],hover_color=self.config["MenuBarHoverColor"],font=("Default", 16,"bold"))

        fileDownCase = CTkMenuBar.CustomDropdownMenu(widget=fileMenu, fg_color=self.config["DropDownColor"],text_color=self.config["DropDownTextColor"],hover_color=self.config["DropDownHoverColor"],
                                                     bg_color=self.config["DropDownColor"],corner_radius=configs["DropDownBorderRadius"])
        editDownCase = CTkMenuBar.CustomDropdownMenu(widget=editMenu, fg_color=self.config["DropDownColor"],text_color=self.config["DropDownTextColor"],hover_color=self.config["DropDownHoverColor"],
                                                     bg_color=self.config["DropDownColor"],corner_radius=configs["DropDownBorderRadius"])    
        viewDownCase = CTkMenuBar.CustomDropdownMenu(widget=viewMenu, fg_color=self.config["DropDownColor"],text_color=self.config["DropDownTextColor"],hover_color=self.config["DropDownHoverColor"],
                                                     bg_color=self.config["DropDownColor"],corner_radius=configs["DropDownBorderRadius"])      
        aboutDownCase = CTkMenuBar.CustomDropdownMenu(widget=aboutMenu, fg_color=self.config["DropDownColor"],text_color=self.config["DropDownTextColor"],hover_color=self.config["DropDownHoverColor"],
                                                     bg_color=self.config["DropDownColor"],corner_radius=configs["DropDownBorderRadius"])      
        aiDownCase = CTkMenuBar.CustomDropdownMenu(widget=aiMenu, fg_color=self.config["DropDownColor"],text_color=self.config["DropDownTextColor"],hover_color=self.config["DropDownHoverColor"],
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
        aiDownCase.add_option(option="Gemini", command=self._Gemi)


        self.NPadTextBox = customtkinter.CTkTextbox(self.NPad,fg_color=self.config["FrameColor"],width=910,height=570,border_spacing=0,text_color=self.config["TextColor"],
                                               font=(configs["Font"], configs["FontSize"], configs["FontB"]),
                                               undo=True)
        self.NPadTextBox.place(x=25,y=40)

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

    # Animations
    def slide_widget_right_to_left(self,widget, start_x, end_x, y, step=5, delay=10):
        widget.place(x=start_x, y=y)
        def move():
            nonlocal start_x
            if start_x > end_x:
                start_x -= step
                widget.place(x=start_x, y=y)
                widget.after(delay, move)
        move()

    def slide_widget_left_to_right(self,widget, start_x, end_x, y, step=5, delay=10):
        widget.place(x=start_x, y=y)
        def move():
            nonlocal start_x
            if start_x < end_x:
                start_x += step
                widget.place(x=start_x, y=y)
                widget.after(delay, move)
        move()

    def animate_width(self,widget, target_width, step=8, delay=6):
        info = widget.place_info()
        current_width = info.get("width")
        if not current_width:
            current_width = widget.winfo_width()
        current_width = int(current_width)

        def animate():
            nonlocal current_width
            if current_width < target_width:
                current_width += step
                if current_width > target_width:
                    current_width = target_width
                widget.place_configure(width=current_width)
                widget.after(delay, animate)
            elif current_width > target_width:
                current_width -= step
                if current_width < target_width:
                    current_width = target_width
                widget.place_configure(width=current_width)
                widget.after(delay, animate)
        animate()

    def _Gemi(self):
        if configs["GeminiKey"] != "NONE":
            if self.NPadTextBox.winfo_width() < 601:
                self.NPadTextBox.configure(width=910)
                self.AiFrame.place(x=1500,y=40)
                self.slide_widget_left_to_right(self.AiFrame,start_x=635,end_x=1250,y=40,step=7,delay=3)
                self.animate_width(widget=self.NPadTextBox,target_width=910)
            else:
                self.animate_width(widget=self.NPadTextBox,target_width=600)
                self.slide_widget_right_to_left(self.AiFrame,start_x=1250,end_x=635,y=40,step=8,delay=3)


    def add_bubble(self, message, sender):
        """Sohbet balonu oluşturup arayüze ekler."""
        message_bubble = customtkinter.CTkFrame(self.chatArea, corner_radius=15)

        message_label = customtkinter.CTkLabel(
            master=message_bubble,
            text=message,
            font=(configs["Font"], configs["FontSize"]-3),
            text_color=self.config["TextColor"],
            wraplength=250,
            justify="left",
            anchor="w"
        )

        def copy_text(event):
            self.NPad.clipboard_clear()
            self.NPad.clipboard_append(message)

        message_label.bind("<Button-3>", copy_text)

        if sender == "user":
            message_bubble.pack(pady=(2, 2), padx=(50, 5), anchor="e")
            message_bubble.configure(fg_color=self.config["UserChatBubbleColor"])
            message_label.configure(fg_color=self.config["UserChatBubbleColor"])
            message_label.pack(side="right", padx=10, pady=5)

        elif sender == "ai":
            message_bubble.pack(pady=(2, 2), padx=(5, 50), anchor="w")
            message_bubble.configure(fg_color=self.config["AiChatBubbleColor"])
            message_label.configure(fg_color=self.config["AiChatBubbleColor"])
            message_label.pack(side="left", padx=10, pady=5)


        self.chatArea.update_idletasks()
        self.chatArea._parent_canvas.yview_moveto(1.0)

    
    def send_message(self):
        """Kullanıcının mesajını gönderir ve yapay zeka yanıtını tetikler."""
        self.user_message = self.msgEntry.get().strip()
        if self.user_message:
            self.add_bubble(self.user_message, "user")
            self.msgEntry.delete(0, "end")
            

            thread = Thread(target=self._ResponseForGemini)
            thread.start()

    def _ResponseForGemini(self):
        if user_configs["AI"]["GeminiKey"] == "NONE":
            self.NPad.after(0, self.add_bubble, "GeminiApi Key Not Founded.", "ai")
            return
        else:
            try:
                client = _CallGemini.Client(api_key=user_configs["AI"]["GeminiKey"])
                ai_response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=self.user_message
                    
                )
                print(self.user_message)
            except Exception as e:
                print(e)

            finally:
                self.NPad.after(0, self.add_bubble, ai_response.text, "ai")

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
        self.AboutPage.grab_set()

        title = customtkinter.CTkLabel(self.AboutPage,text="CUSPAD 1.2",font=("Helvetica",40,"bold"),text_color=configs[ActiveTheme]["TextColor"])
        title.place(x=85,y=75)

        label1 = customtkinter.CTkLabel(self.AboutPage,text="Made By CSDC-K Kuzey", font=("Default",18,"italic"),text_color=configs[ActiveTheme]["TextColor"])
        label1.place(x=105,y=150)  

if __name__ == "__main__":
    app = NotePad()
