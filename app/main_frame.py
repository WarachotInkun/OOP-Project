import tkinter as tk
from tkinter import PhotoImage     
from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap import font
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.dialogs import Messagebox
import requests
import json
from PIL import Image, ImageTk
from functools import partial
import re
import uvicorn
from fastapi import FastAPI

class KFCApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("KFC Huh")
        self.geometry("1000x600")
        self.g_id= NONE
        self.member_id = NONE
        self.member_name = NONE
        self.set_new_guest_id()
        print(self.g_id)


        self.login_ui = KFCLoginUI(self)
        self.signup_ui = KFCSignupUI(self)    
        self.menu_ui = KFCMenuUI(self)  
        self.mod_ui = KFCModUI(self)
        # self.cart_ui = KFCcart(self)
        # self.reviwe_ui = KFCreview(self)
        self.transaction_ui = None
        self.current_frame = self.signup_ui
        self.show_frame(self.menu_ui)
        


    def show_frame(self, frame):
        if self.current_frame:
            self.current_frame.main_frame.pack_forget()  # Hide the old frame
        self.current_frame = frame
        frame.main_frame.pack(side=tk.TOP, fill=tk.BOTH, anchor=tk.S)
    def set_member_details(self, member_id, member_name):
        self.member_id = member_id
        self.member_name = member_name
    def set_new_guest_id(self):
        self.API_root = "http://127.0.0.1:8000/root"
        self.respond = requests.get(self.API_root).json()       
        self.g_id = self.respond["Current"]
        print(self.g_id)

class KFCLoginUI(ttk.Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.app = root
        self.login_img= ImageTk.PhotoImage(file='img/login.png')
        self.login_img_focus= ImageTk.PhotoImage(file='img/login_focus.png')
        self.signup_img= ImageTk.PhotoImage(file='img/signup.png')
        self.menu_img= ImageTk.PhotoImage(file='img/menu.png')
         
        self.init_ui()

    def init_ui(self):
        self.main_frame = ttk.Frame(self.app)
        # self.main_frame.pack(side=tk.TOP, fill=tk.BOTH, anchor=tk.S)

        sign_in_text = ttk.Label(self.main_frame, text="Sign In", font=('', 25, "bold"), foreground='#cc0011',background='#ffffff')
        sign_in_text.pack(side=TOP, anchor=S, padx=1, pady=10)


        self.sub_text = ttk.Label(self.main_frame, text="Protecting the security of your \n  personal data is our priority", font=('', 15), foreground='#000000',background='#ffffff')
        self.sub_text.pack(side=TOP, anchor=S, padx=1, pady=10)
        self.sub2_text = ttk.Label(self.main_frame, text="Please sign in to your account with your username and password", font=('', 10), foreground='#000000',background='#ffffff')
        self.sub2_text.pack(side=TOP, anchor=S, padx=1, pady=10)


        self.entry_username = ttk.Entry(self.main_frame, width=40,font=('', 15), foreground='#a3a3a3',background='#ffffff',bootstyle="danger")
        self.entry_username.pack(side=TOP, padx=1, pady=10)
        self.entry_username.insert(0,"Username")  
        self.entry_username.bind("<FocusIn>", lambda event :self.handle_entry_click(event,"Username"))  
        self.entry_username.bind("<FocusOut>", lambda event :self.handle_out_focus(event,"Username"))  


        self.password_username = ttk.Entry(self.main_frame, width=40,font=('', 15), foreground='#a3a3a3',background='#ffffff',bootstyle="danger")
        self.password_username.pack(side=TOP, padx=1, pady=10)
        self.password_username.insert(0,"Password")  
        self.password_username.bind("<FocusIn>", lambda event :self.handle_entry_click(event,"Password"))  
        self.password_username.bind("<FocusOut>", lambda event :self.handle_out_focus(event,"Password"))  



        self.login_button = Label(self.main_frame, image=self.login_img,compound=CENTER)
        self.login_button.pack(side=TOP, padx=1, pady=10)
        self.login_button.bind("<Enter>", lambda event: self.on_enter(event))
        self.login_button.bind("<Leave>", self.on_leave)
        self.login_button.bind("<Button-1>",  lambda event:self.click_login(event))

        self.signup_button = Label(self.main_frame, image=self.signup_img,compound=CENTER)
        self.signup_button.pack(side=TOP, padx=1, pady=10)
        self.signup_button.bind("<Button-1>",  lambda event:self.click_signup(event))

        self.menu_button = Label(self.main_frame, image=self.menu_img,compound=CENTER)
        self.menu_button.pack(side=TOP, padx=1, pady=5)
        self.menu_button.bind("<Button-1>",  lambda event:self.app.show_frame(self.app.menu_ui))
        
    def handle_entry_click(self, event, text):
        content = event.widget.get()
        if content == text:
            event.widget.delete(0, tk.END)
        if text == "Password":
            event.widget.config(show='•')

    
    def handle_out_focus(self, event, text):
        content = event.widget.get()
        if content == '': 
            event.widget.insert(0, text)
        content = event.widget.get()
        if content == "Password":
            event.widget.config(show="")

    
    def on_enter(self,event ):
        event.widget.config( image = self.login_img_focus)

    def on_leave(self,event):
        event.widget.config( image = self.login_img)

    def click_login(self,event):
        print(self.entry_username.get())
        print(self.password_username.get())
        self.API_login = "http://127.0.0.1:8000/login"
        self.input_json = {
            "username": f"{self.entry_username.get()}",
            "password": f"{self.password_username.get()}",
            "guest_id": f"{app.g_id}"
            }
        self.response_login = requests.post(self.API_login, json=self.input_json)
        print(self.response_login.json())
        if self.response_login.json():
            self.app.set_member_details(self.response_login.json()["id"], self.response_login.json()["name"])
            self.app.transaction_ui = KFCtransaction(self.app) 
            self.app.show_frame(self.app.menu_ui)
            self.app.set_new_guest_id()
            self.app.menu_ui.login_text.pack_forget()
            
        else:
            mb = Messagebox.ok( "Username or Password is incorrect","Error",bootstyle="danger")
            self.entry_username.delete(0, tk.END)  
            self.password_username.delete(0, tk.END)  
            self.entry_username.insert(0,"Username")  
            self.password_username.insert(0,"Password")
            app.set_new_guest_id()






    def click_signup(self,event):
        self.app.show_frame(self.app.signup_ui)

    





class KFCSignupUI(ttk.Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.app = root
        self.init_ui()

    def init_ui(self):
        self.main_frame = ttk.Frame(self.app )
        # main_frame.pack(side=tk.TOP, fill=tk.BOTH, anchor=tk.S)

        # Create UI elements here
        sign_in_text = ttk.Label(self.main_frame, text="Create your account", font=('', 25, "bold"), foreground='#cc0011', background='#ffffff')
        sign_in_text.pack(side=tk.TOP, anchor=tk.S, padx=1, pady=10)

        sub2_text = ttk.Label(self.main_frame, text="Easier to order. Enable your point redemption. More privilege for online member", font=('', 10), foreground='#000000', background='#ffffff')
        sub2_text.pack(side=tk.TOP, anchor=tk.N, padx=1, pady=10)

        # Name entry
        self.entry_name = ttk.Entry(self.main_frame, width=40, font=('', 15), foreground='#a3a3a3', background='#ffffff', bootstyle="danger")
        self.entry_name.pack(side=tk.TOP, padx=1, pady=10)
        self.entry_name.insert(0, "Full name")
        self.entry_name.bind("<FocusIn>", lambda event :self.handle_entry_click(event,"Full name"))  
        self.entry_name.bind("<FocusOut>", lambda event :self.handle_out_focus(event,"Full name")) 
        # Username entry
        self.entry_username = ttk.Entry(self.main_frame, width=40, font=('', 15), foreground='#a3a3a3', background='#ffffff', bootstyle="danger")
        self.entry_username.pack(side=tk.TOP, padx=1, pady=10)
        self.entry_username.insert(0, "Username")
        self.entry_username.bind("<FocusIn>", lambda event :self.handle_entry_click(event,"Username"))  # Use class method
        self.entry_username.bind("<FocusOut>",lambda event :self.handle_out_focus(event,"Username"))  # Use class method

        # Password entry
        self.password_username = ttk.Entry(self.main_frame, width=40, font=('', 15), foreground='#a3a3a3', background='#ffffff', bootstyle="danger")
        self.password_username.pack(side=tk.TOP, padx=1, pady=10)
        
         
        self.password_username.bind("<FocusIn>", lambda event :self.handle_entry_click(event,"Password"))  
        self.password_username.bind("<FocusOut>", lambda event :self.handle_out_focus(event,"Password")) 
        

        # Confirm password entry
        self.confirm_password_username = ttk.Entry(self.main_frame, width=40, font=('', 15), foreground='#a3a3a3', background='#ffffff', bootstyle="danger")
        self.confirm_password_username.pack(side=tk.TOP, padx=1, pady=10)
        
        
        self.confirm_password_username.bind("<FocusIn>", lambda event :self.handle_entry_click(event,"Confirm password"))  # Use class method
        self.confirm_password_username.bind("<FocusOut>", lambda event :self.handle_out_focus(event,"Confirm password"))  # Use class method
        self.password_username.insert(0, "Password")
        self.confirm_password_username.insert(0, "Confirm password")
        # Load images (assuming they're in a subfolder named 'img')
        self.signup_img = PhotoImage(file='img/create.png')
        self.back_img = PhotoImage(file='img/back.png')

        
        self.signup_button = Label(self.main_frame, image=self.signup_img, compound=CENTER)
        self.signup_button.pack(side=tk.TOP, padx=1, pady=10)
        self.signup_button.bind("<Button-1>",  lambda event:self.click_signup(event))

        self.back_button = Label(self.main_frame, image=self.back_img, compound=CENTER,)
        self.back_button.pack(side=tk.TOP, padx=1, pady=10)
        self.back_button.bind("<Button-1>",  lambda event:self.go_to_login(event))

    def click_signup(self,event):
        print(self.entry_username.get())
        print(self.password_username.get())
        if self.password_username.get() == self.confirm_password_username.get():
            app.set_new_guest_id()
            self.API_register = "http://127.0.0.1:8000/register"
            self.input_json = {
                        "name": f"{self.entry_name.get()}",
                        "username": f"{self.entry_username.get()}",
                        "password": f"{self.password_username.get()}",
                        "guest_id": f"{app.g_id}"
                            }
            self.response_register = requests.post(self.API_register, json=self.input_json)
            print(self.response_register.json())
            app.set_new_guest_id()
            app.show_frame(app.login_ui)
        else:
            mb = Messagebox.ok( "Password is incorrect","Error",bootstyle="danger")
            self.entry_name.delete(0, tk.END)  
            self.entry_name.insert(0,"Full name")
            self.entry_username.delete(0, tk.END)  
            self.entry_username.insert(0,"Username")  
            self.password_username.delete(0, tk.END)  
            self.password_username.insert(0, "Password")
            self.confirm_password_username.delete(0, tk.END)  
            self.confirm_password_username.insert(0,"Confirm password")
            app.set_new_guest_id()


    def go_to_login(self, event): 
        self.app.show_frame(self.app.login_ui)

    def handle_entry_click(self, event, text):
        content = event.widget.get()
        if content in [text]:  # Exact match check
            event.widget.delete(0, tk.END)
        if text in ["Password", "Confirm password"]:  # Check if it's a password field
            event.widget.config(show='•')

    def handle_out_focus(self, event, text):
        content = event.widget.get()
        if  content == "":  # Only restore if completely empty
            event.widget.insert(0, text)
        content = event.widget.get()
        if content  in ["Password", "Confirm password"]: 
            event.widget.config(show="")
    


class KFCMenuUI(ttk.Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.app = root   
        self.init_ui()

    def init_ui(self):
        self.main_frame= ttk.Frame(self.app)
        

        self.nav = ttk.Frame(self.main_frame, height=80)
        self.nav.pack(side=TOP, fill=ttk.X)
        self.nav.pack_propagate(0)

        self.menu_frame = ScrolledFrame(self.main_frame,height=3000)
        self.menu_frame.pack(side=TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        

        
        
        self.promotion_text = ttk.Label(self.nav, text="Reviwe", font=('', 16, "bold"), foreground='#000000',background='#ffffff')
        self.promotion_text.pack(side=LEFT, padx=1, pady=1)
        self.promotion_text.bind("<Enter>", lambda event: self.on_enter(event, '#ad8003'))
        self.promotion_text.bind("<Leave>", self.on_leave)
        self.promotion_text.bind('<Button-1>', lambda event: self.app.show_frame(KFCreview(self.app)))
        ttk.Separator(self.nav, orient=VERTICAL).pack(side=LEFT)
        self.adress = ttk.Label(self.nav, text="Adresss", font=('', 16, "bold"), foreground='#000000',background='#ffffff')
        self.adress.pack(side=LEFT, padx=1, pady=1)
        self.adress.bind("<Enter>", lambda event: self.on_enter(event, '#ad8003'))
        self.adress.bind("<Leave>",self.on_leave)
        self.adress.bind('<Button-1>', lambda event: self.open_adress())
        # ttk.Separator(self.nav, orient=VERTICAL).pack(side=LEFT)KFCtransaction(ttk.Frame)
        # self.Acarte_text = ttk.Label(self.nav, text="A la carte", font=('', 16, "bold"), foreground='#000000',background='#ffffff')
        # self.Acarte_text.pack(side=LEFT, padx=1, pady=1)
        # self.Acarte_text.bind("<Enter>", lambda event: self.on_enter(event, '#ad8003'))
        # self.Acarte_text.bind("<Leave>", self.on_leave)
        ttk.Separator(self.nav, orient=VERTICAL).pack(side=LEFT)
        self.adress = ttk.Label(self.nav, text="transaction", font=('', 16, "bold"), foreground='#000000',background='#ffffff')
        self.adress.pack(side=LEFT, padx=1, pady=1)
        self.adress.bind("<Enter>", lambda event: self.on_enter(event, '#ad8003'))
        self.adress.bind("<Leave>",self.on_leave)
        self.adress.bind('<Button-1>', lambda event: self.open_success())

        price  = "Cart"
        self.cart_price_text = ttk.Label(self.nav, text=price, font=('', 16, "bold"), foreground='#000000',background='#ffffff')
        self.cart_price_text.pack(side=RIGHT, padx=1, pady=1)
        self.cart_price_text.bind("<Enter>", lambda event: self.on_enter(event, '#cc0011'))
        self.cart_price_text.bind("<Leave>", self.on_leave)
        self.cart_price_text.bind('<Button-1>', lambda event: self.open_cart())
        ttk.Separator(self.nav, orient=VERTICAL).pack(side=RIGHT)


        
        self.login_text = ttk.Label(self.nav, text="Login", font=('', 16, "bold"), foreground='#000000',background='#ffffff')
        self.login_text.pack(side=RIGHT, padx=1, pady=1)
        self.login_text.bind("<Enter>", lambda event: self.on_enter(event, '#cc0011'))
        self.login_text.bind("<Leave>", self.on_leave)
        self.login_text.bind('<Button-1>', lambda event: self.click_login())
        # temp_cart=""
        # self.cart_image = PhotoImage(file='img/cart_count.png')
        # self.cart_label = ttk.Label(self.nav, image=self.cart_image,text= temp_cart, compound=CENTER,foreground='#ffffff',font=('', 16, "bold"))
        # self.cart_label.pack(side=tk.RIGHT, padx=1, pady=1)


        self.inner_frame = ttk.Frame(self.menu_frame)
        self.inner_frame.pack()
        self.API_1 = "http://127.0.0.1:8000/menu"
        self.respond = requests.get(self.API_1).json()
        # print(self.respond["a la carte"])




        self.item_images = []
        self.promotion_button_list = []
        self.boxset_button_list = []
        self.Alacarte_button_list = []
        self.item_button_img = PhotoImage(file='img/price_button.png')
        self.item_button_img_focus= PhotoImage(file='img/price_button_focus.png')

        self.inframe_text_promotion = ttk.Label(self.inner_frame, text="PROMOTION", font=('', 20, "bold"), foreground='#000000',background='#ffffff')
        self.inframe_text_promotion.pack(side=TOP, anchor=NW, padx=1, pady=1)
        self.inner_grid_promotion = ttk.Frame(self.inner_frame)
        self.inner_grid_promotion.pack(side=TOP, padx=1, pady=1)
        for i in enumerate(self.respond["promotion"]):
            self.row_num = i[0] // 2
            self.col_num = i[0] % 2
            self.frame = ttk.Frame(self.inner_grid_promotion, width=400, height=300,relief=RAISED )
            self.frame.grid_propagate(False)
            self.frame.grid(padx=10, pady=10,row = self.row_num,column = self.col_num)
            self.frame.columnconfigure(0, weight=3)
            self.frame.columnconfigure(1, weight=1)
            self.item_label = ttk.Label(self.frame, text=i[1], font=('', 16, "bold"), foreground="#cc0011", background="#ffffff")
            self.item_label.grid(row = 0,column = 1,padx=10, pady=10,sticky=NW) 
            img = Image.open(f'menu_img/{i[1]}.png')
            img = img.resize((192, 155), Image.LANCZOS)  
            self.item_img = ImageTk.PhotoImage(img)
            self.item_images.append(self.item_img)
            self.item_label_img = ttk.Label(self.frame, image=self.item_img)
            self.item_label_img.grid(row = 0,column = 0,padx=10, pady=10,sticky=N)
            price = self.respond["promotion"][i[1]]["price"] 
            self.item_button = ttk.Label(self.frame, image=self.item_button_img, text=f"{price} บาท", compound=CENTER, foreground='#ffffff', font=('', 16, "bold"))  # Pass 'self.frame' as parent
            self.item_button.bind('<Enter>',lambda event : self.item_on_enter(event,self.item_button_img_focus))
            self.item_button.bind('<Leave>',lambda event : self.item_on_leave(event,self.item_button_img))
            self.item_button.bind('<Button-1>', partial(self.on_click, name=i[1]))
            self.promotion_button_list.append(self.item_button)
            self.promotion_button_list[i[0]].grid(row=1, column=0, padx=10, pady=10, sticky=N) 

        inframe_text_Boxset = ttk.Label(self.inner_frame, text="Boxset", font=('', 20, "bold"), foreground='#000000',background='#ffffff')
        inframe_text_Boxset.pack(side=TOP, anchor=NW, padx=1, pady=1)
        inner_grid_Boxset = ttk.Frame(self.inner_frame)
        inner_grid_Boxset.pack(side=TOP, padx=1, pady=1)

        for i in enumerate(self.respond["box set"]):
            self.row_num = i[0] // 2
            self.col_num = i[0] % 2
            self.frame = ttk.Frame(inner_grid_Boxset, width=400, height=300,relief=RAISED )
            self.frame.grid_propagate(False)
            self.frame.grid(padx=10, pady=10,row = self.row_num,column = self.col_num)
            self.frame.columnconfigure(0, weight=3)
            self.frame.columnconfigure(1, weight=1)
            self.item_label = ttk.Label(self.frame, text=i[1], font=('', 16, "bold"), foreground="#cc0011", background="#ffffff")
            self.item_label.grid(row = 0,column = 1,padx=10, pady=10,sticky=NW) 
            img = Image.open(f'menu_img/{i[1]}.png')
            img = img.resize((192, 155), Image.LANCZOS)  
            self.item_img = ImageTk.PhotoImage(img)
            self.item_images.append(self.item_img)
            self.item_label_img = ttk.Label(self.frame, image=self.item_img)
            self.item_label_img.grid(row = 0,column = 0,padx=10, pady=10,sticky=N)
            price = self.respond["box set"][i[1]]["price"] 
            self.item_button = ttk.Label(self.frame, image=self.item_button_img, text=f"{price} บาท", compound=CENTER, foreground='#ffffff', font=('', 16, "bold"))  # Pass 'self.frame' as parent
            self.item_button.bind('<Enter>',lambda event : self.item_on_enter(event,self.item_button_img_focus))
            self.item_button.bind('<Leave>',lambda event : self.item_on_leave(event,self.item_button_img))
            self.item_button.bind('<Button-1>', partial(self.on_click, name=i[1]))
            self.boxset_button_list.append(self.item_button)
            self.boxset_button_list[i[0]].grid(row=1, column=0, padx=10, pady=10, sticky=N)


        inframe_text_Acarte = ttk.Label(self.inner_frame, text="A la Carte", font=('', 20, "bold"), foreground='#000000',background='#ffffff')
        inframe_text_Acarte.pack(side=TOP, anchor=NW, padx=1, pady=1)
        inner_grid_Acarte = ttk.Frame(self.inner_frame)
        inner_grid_Acarte.pack(side=TOP, padx=1, pady=1)

        for i in enumerate(self.respond["a la carte"]):
            self.row_num = i[0] // 2
            self.col_num = i[0] % 2
            self.frame = ttk.Frame(inner_grid_Acarte, width=400, height=330,relief=RAISED )
            self.frame.grid_propagate(False)
            self.frame.grid(padx=10, pady=10,row = self.row_num,column = self.col_num)
            self.frame.columnconfigure(0, weight=3)
            self.frame.columnconfigure(1, weight=1)
            self.item_label = ttk.Label(self.frame, text=i[1], font=('', 16, "bold"), foreground="#cc0011", background="#ffffff")
            self.item_label.grid(row = 0,column = 1,padx=10, pady=10,sticky=N) 
            img = Image.open(f'menu_img/{i[1]}.png')
            img = img.resize((216, 175), Image.LANCZOS)  
            self.item_img = ImageTk.PhotoImage(img)
            self.item_images.append(self.item_img)
            self.item_label_img = ttk.Label(self.frame, image=self.item_img)
            self.item_label_img.grid(row = 0,column = 0,padx=10, pady=10,sticky=N)

            price = self.respond["a la carte"][i[1]]["price"]
    
            self.item_button = ttk.Label(self.frame, image=self.item_button_img, text=f"{price} บาท", compound=CENTER, foreground='#ffffff', font=('', 16, "bold"))  # Pass 'self.frame' as parent
            self.item_button.bind('<Enter>',lambda event : self.item_on_enter(event,self.item_button_img_focus))
            self.item_button.bind('<Leave>',lambda event : self.item_on_leave(event,self.item_button_img))
            self.item_button.bind('<Button-1>', partial(self.on_click, name=i[1]))
            self.Alacarte_button_list.append(self.item_button)
            self.Alacarte_button_list[i[0]].grid(row=1, column=0, padx=10, pady=10, sticky=N)

    def item_on_leave(self,event,img ):
        event.widget.config(image=img)
    def item_on_enter(self,event,img):
        event.widget.config(image=img)


    def on_enter(self,event ,color  ):
        event.widget.config(foreground=color, font=('', 16, "bold"))

    def on_leave(self,event):
        event.widget.config(foreground='#000000', font=('', 16, "bold"))
    def on_click(self,event,name):
        if self.app.member_id != "none":
            app.mod_ui.set_meal_name(name)
            app.mod_ui.set_member_id(self.app.member_id)
            app.mod_ui.init_ui()
            app.show_frame(app.mod_ui)
            print(name)
        else:
            self.app.show_frame(self.app.login_ui)       
    def open_cart(self):
        if self.app.member_id == "none":
            self.app.show_frame(self.app.login_ui)
        else:
            temp_address = KFCaddress(self.app).response_show_address.json()
            print(temp_address)
            if temp_address == {}:
                self.app.show_frame(KFCaddress(self.app))
            else:
                self.app.show_frame(KFCcart(self.app))
    def open_adress(self):
        if self.app.member_id == "none":
            self.app.show_frame(self.app.login_ui)
        else:
            self.app.show_frame(KFCaddress(self.app))
    def open_success(self):
        if self.app.member_id == "none":
            self.app.show_frame(self.app.login_ui)
        else:
            self.app.transaction_ui.init_ui()
            self.app.show_frame(self.app.transaction_ui)
    def click_login(self):
        self.app.show_frame(self.app.login_ui)

class KFCcart(ttk.Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.app = root
        self.API_show_cart = "http://127.0.0.1:8000/show_cart"
        self.API_remove_item = "http://127.0.0.1:8000/remove_item"
        self.member_id = self.app.member_id
        self.input_json = {
            "member_id": self.member_id  
            }
        self.response_show_cart = requests.post(self.API_show_cart, json=self.input_json)
        
        self.init_ui()

    def init_ui(self,):
        self.main_frame = ttk.Frame(self.app)


        self.cart_title = ttk.Label(self.main_frame, text="Cart", font=('', 20, "bold"), foreground='#000000',background='#ffffff',relief=RIDGE)
        self.cart_title.pack(side = TOP, padx=10, pady=10)
        self.main_frame2 = ttk.Frame(self.main_frame, height=1000, width=600, bootstyle = "danger") 
        self.main_frame2.pack(side = TOP, padx=10, pady=10)
        self.cart_frame = ScrolledFrame(self.main_frame2,height=1000,width=650)
        self.cart_frame.pack(side = LEFT, padx=10, pady=10)
        self.button_box = ttk.Frame(self.main_frame2, height=200, width=200,bootstyle="info")
        self.button_box.pack(side = TOP, padx=10, pady=10,)
        self.add_more_food_button = ttk.Button(self.button_box, text="Add More Food", bootstyle = 'danger',command=lambda: self.add_more_food_button_click())
        self.add_more_food_button.grid(column=0, row= 0, pady=35, padx=5, sticky=W)
        self.checkout_button = ttk.Button(self.button_box, text="Checkout", bootstyle = 'danger',command=lambda: self.checkout_button_click())
        self.checkout_button.grid(column=0, row= 2, pady=35, padx=5, sticky=W) 
        self.display_item(self.response_show_cart)
    
    def display_item(self,response_cart):
        self.index = 0
        self.total_price = 0
        self.list_item_id = []
        for name, all_items in response_cart.json().items():
            self.name_label = ttk.Label(self.cart_frame, text=name, font=('', 16, "bold"),bootstyle = "default")
            self.name_label.grid(padx=20, pady=5,row = 0,column = 0)
            for each_item,price in all_items.items():
                self.list_item_id.append(price['item_id'])
                self.each_item_frame = ttk.Frame(self.cart_frame, width=500, height=100,bootstyle="danger",relief=RIDGE,borderwidth=1)
                self.each_item_frame.grid(padx =50, pady=25,row = self.index+1,column = 0,sticky=W)
                self.item_name_label = ttk.Label(self.each_item_frame, text=each_item, font=('', 10, "bold"),bootstyle = "danger")
                self.item_name_label.grid(padx=20, pady=5,row = 1,column = 1)
                self.item_price_label = ttk.Label(self.each_item_frame, text= 'price : ' + str(price['price']), font=('', 10, "bold"),bootstyle = "danger")
                self.item_price_label.grid(padx=200, pady=5,row = 2,column = 1)
                self.total_price = self.total_price + price['price']
                self.index = self.index + 1
        self.index = 0
        for item_id in self.list_item_id:
            self.delete_button = ttk.Button(self.cart_frame, text="X", bootstyle = 'danger',command=lambda item_id=item_id: self.delete_button_click(item_id))
            self.delete_button.grid(padx=0, pady=5,row = self.index+1,column = 1)
            self.index = self.index + 1
        self.total_price_label = ttk.Label(self.button_box, text="Total Price :" + str(self.total_price), font=('', 16, "bold"),bootstyle = "danger")
        self.total_price_label.grid(column=0, row= 3, pady=35, padx=5, sticky=W)
        
    def delete_button_click(self,item_id):
        input_json = {
            "member_id": self.member_id,
            "meal_id": item_id
            }
        print(input_json)
        response_remove_item = requests.post(self.API_remove_item, json=input_json)
        self.response_show_cart = response_remove_item
        for child in self.cart_frame.winfo_children():
            child.destroy()
        self.total_price_label.destroy()
        self.display_item(self.response_show_cart)


    def add_more_food_button_click(self):
        self.app.show_frame(self.app.menu_ui)
        
    def checkout_button_click(self):
        self.app.show_frame(KFCpayment(self.app))




class KFCreview(ttk.Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.app = root
        self.memebr_id = self.app.member_id
        self.API_review = "http://127.0.0.1:8000/show_all_review"
        self.response_show_review = requests.get(self.API_review)
        self.API_write_review = "http://127.0.0.1:8000/write_review"
        self.init_ui()
        
    
    def init_ui(self):
        print(self.app.member_id)
        self.all_review = []
        for i in self.response_show_review.json().values():
            this_review = []
            this_review.append(i["score"])
            this_review.append(i["comment"])
            self.all_review.append(this_review)

        self.main_frame= ttk.Frame(self.app)
        

        self.Review_label = ttk.Label(self.main_frame, text="Review", font=('', 20, "bold"), foreground='#000000',background='#ffffff',relief=RIDGE,borderwidth=20)
        self.Review_label.pack(side=TOP, anchor=N, padx=1, pady=1)

        self.back_button = ttk.Button(self.main_frame, text="Back", bootstyle = 'danger',command= lambda : self.back_button_click())        
        self.back_button.pack(side=TOP, anchor=W, padx=1, pady=1)

        self.write_review_button = ttk.Button(self.main_frame, text="Write Review", bootstyle = 'danger',command = self.write_review_button_click)
        self.write_review_button.pack(side=TOP, anchor=E, padx=1, pady=1)

        self.main_review_frame = ScrolledFrame(self.main_frame,height=3000)
        self.main_review_frame.pack(side=TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.display_item()

    def display_item(self):
        for i in range(len(self.response_show_review.json())):
            self.row_num = i
            self.col_num = 1
            self.review_frame = ttk.Frame(self.main_review_frame, width=750, height=75,bootstyle="danger",relief=RIDGE,borderwidth=1)
            self.review_frame.grid(padx=125, pady=25,row = self.row_num,column = self.col_num,sticky=W)
            self.score_label = tk.Label(self.review_frame, text="score : " + str(self.all_review[i][0]), font=('', 16, "bold"))
            self.score_label.grid(padx=20, pady=5,row = 1,column = 1,sticky=W)
            self.comment_label = tk.Label(self.review_frame, text="comment : " + str(self.all_review[i][1]), font=('', 16, "bold"))
            self.comment_label.grid(padx=20, pady=5,row = 2,column = 1,sticky=W)

    def back_button_click(self):
        self.app.show_frame(self.app.menu_ui)

    def write_review_button_click(self):
        
        if self.app.member_id != "none":
            self.write_review_window = tk.Tk()
            self.write_review_window.title("Write Review")
            self.score_label = ttk.Label(self.write_review_window, text = 'score', font=('',14, "bold"))
            self.score_label.grid(row = 0, column = 0, padx=10, pady=0)
            self.choses_scores = tk.IntVar()
            self.choses_scores = ttk.Combobox(self.write_review_window, textvariable=self.choses_scores)
            self.choses_scores['values'] = (1,2,3,4,5)
            self.choses_scores.grid(row = 0, column = 1,padx=10,pady = 0)
            
            self.comment_label = ttk.Label(self.write_review_window, text = 'comment', font=('',14, "bold"))
            self.comment_label.grid(row = 1, column = 0, padx=10, pady=0)
            self.comment = tk.StringVar()
            self.comment = tk.Entry(self.write_review_window,textvariable=self.comment)
            self.comment.grid(row = 1, column = 1, padx=10, pady=10)
            
            self.confirm_method_button = ttk.Button(self.write_review_window, text="Confirm", bootstyle = 'info',command=self.confirm_button_click)
            self.confirm_method_button.grid(row = 2, column = 1, columnspan=2, padx=10, pady=10)
            
        else:
            self.app.show_frame(self.app.login_ui)

    
    def confirm_button_click(self):
        self.input_json= {
                        "member_id": self.memebr_id,
                        "score": self.choses_scores.get(),
                        "comment": self.comment.get()
                        }
        print(self.input_json)
        self.write_review_response = requests.post(self.API_write_review, json=self.input_json)
        self.response_show_review = self.write_review_response
        this_review = []
        this_review.append(self.choses_scores.get())
        this_review.append(self.comment.get())
        self.all_review.append(this_review)
        for child in self.main_review_frame.winfo_children():
            child.destroy()
        self.display_item()
        self.write_review_window.destroy()
        print("success")





class KFCModUI(ttk.Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.app = root
        self.member_id = self.app.member_id
        self.meal_name = None  
        if self.meal_name != None:
            self.init_ui()

    def init_ui(self):
        self.main_frame= Frame(self.app)
        self.scoll_frame= ScrolledFrame(self.main_frame , height=1050)
        self.scoll_frame.pack(side=TOP, fill =ttk.BOTH)
        self.scoll_frame.pack_propagate(0)
        self.select_frame  = ttk.Frame(self.scoll_frame, height=250)
        self.select_frame.pack(side=TOP, fill =ttk.X)

        self.API_select_food = "http://127.0.0.1:8000/select_food"

        self.input_json = {
            "member_id": self.member_id  ,
            "meal_name": f"{self.meal_name}"
            }
        self.response_select_food = requests.post(self.API_select_food, json=self.input_json)
        print(self.response_select_food.json())
        self.item_name =list(self.response_select_food.json().keys())[0]
        print(self.item_name)
        self.item_img = Image.open(f'menu_img/{self.item_name}.png')
        self.item_img = ImageTk.PhotoImage(self.item_img)
        self.item_label_img = ttk.Label(self.select_frame, image=self.item_img)
        self.item_label_img.grid(row = 0,column = 0,padx=10, pady=10,sticky=N,rowspan=2)
        

        self.food_item_names_key = list(self.response_select_food.json().keys())[0]
        self.food_item_names = list(self.response_select_food.json()[self.food_item_names_key].keys())
        self.item_detel = ""

        ttk.Separator(self.scoll_frame, orient=HORIZONTAL).pack( fill=ttk.X)

        if "id" not in self.food_item_names:
            for name in self.food_item_names:
                self.item_detel += name + "\n"

        self.item_label = ttk.Label(self.select_frame, text=self.item_name, font=('', 20, "bold"), foreground="#cc0011", background="#ffffff")
        self.item_label.grid(row = 0,column = 1,padx=0, pady=10,sticky=SW)
        self.item_detel_label = ttk.Label(self.select_frame, text=self.item_detel, font=('', 10), foreground="#000000", background="#ffffff")
        self.item_detel_label.grid(row = 1,column = 1,padx=0, pady=10,sticky=NW)



        self.item_list = self.extract_last_layer_and_ids(self.response_select_food.json())
        print(self.item_list)
        # for key, value in self.temp.items():
        #     print(key[2:],value)

        self.back_button = ttk.Button(self.select_frame, text="Back", bootstyle = 'danger',command=lambda:self.app.show_frame(self.app.menu_ui))
        self.back_button.place(x=10,y=10)


        chicken_part = ["อก" ,"น่อง" ,"สะโพก" ,"ปีก"]
        chichen_recipe =["ออริจินอล","สไปซี่","ไม่กรอบ"]  
        drink_type = ["น้ำเปล่า" ,"น้ำอัดลม"]
        drink_size  = ["S","M","L","XL"]
        bowl_type = ["ข้าวเปล่า" ,"ข้าวไก่ทอด"]
        bolw_topping = ["ไก่เผ็ด","แกงเขียวหวาน"]





        self.menubuttons = []
        value_list = []
        for key, value in self.item_list.items():
            self.inner_frame = ttk.Frame(self.scoll_frame)
            self.inner_frame.pack(side=TOP, padx=1, pady=1, anchor=NW)
            key = re.sub(r'\d+', '', key)
            if "ไก่ทอด" in key  and "ข้าว" not in key:
                self.item_name = ttk.Label(self.inner_frame, text=key, font=('', 16, "bold"), foreground="#cc0011", background="#ffffff")
                self.item_name.pack(side=LEFT, padx=10, pady=10)

                # Part Menu
                part_menu = ttk.Menubutton(self.inner_frame, text="Part", width=30, bootstyle="dark-outline")
                part_menu.pack(side=LEFT, padx=10, pady=10)
                self.menubuttons.append(part_menu)

                # Create a unique variable for each item
                part_variable = StringVar()

                inside_part_menu = ttk.Menu(part_menu)
                for attribute in chicken_part:
                    inside_part_menu.add_radiobutton(label=attribute, variable=part_variable,
                                                    command=lambda text=attribute, mod_menu=part_menu:
                                                    self.change_text_menu(mod_menu, text))
                part_menu["menu"] = inside_part_menu

                # Recipe Menu
                recipe_menu = ttk.Menubutton(self.inner_frame, text="Recipe", width=30, bootstyle="dark-outline")
                recipe_menu.pack(side=LEFT, padx=10, pady=10)
                self.menubuttons.append(recipe_menu)

                # Create a unique variable for each item
                recipe_variable = StringVar()

                inside_recipe_menu = ttk.Menu(recipe_menu)
                for attribute in chichen_recipe:
                    inside_recipe_menu.add_radiobutton(label=attribute, variable=recipe_variable,
                                                    command=lambda text=attribute, mod_menu=recipe_menu:
                                                    self.change_text_menu(mod_menu, text))
                recipe_menu["menu"] = inside_recipe_menu

                self.button = ttk.Button(self.inner_frame, text="OK", command=lambda: self.click_mod_button(value, part_variable.get(), recipe_variable.get()), bootstyle="dark-outline")
                self.button.pack(side=LEFT, padx=10, pady=10)
                self.menubuttons.append(self.button)

            elif "น้ำ" in key:
                self.item_name = ttk.Label(self.inner_frame, text=key, font=('', 16, "bold"), foreground="#0000cc", background="#ffffff")
                self.item_name.pack(side=LEFT, padx=10, pady=10)

                # Drink Type Menu
                drink_type_menu = ttk.Menubutton(self.inner_frame, text="Type", width=30, bootstyle="dark-outline")
                drink_type_menu.pack(side=LEFT, padx=10, pady=10)
                self.menubuttons.append(drink_type_menu)

                inside_drink_type_menu = ttk.Menu(drink_type_menu)
                drink_type_variable = StringVar()
                for attribute in drink_type:
                    inside_drink_type_menu.add_radiobutton(label=attribute, variable=drink_type_variable,
                                                        command=lambda text=attribute, mod_menu=drink_type_menu:
                                                                self.change_text_menu(mod_menu, text))
                drink_type_menu["menu"] = inside_drink_type_menu

                # Drink Size Menu
                drink_size_menu = ttk.Menubutton(self.inner_frame, text="Size", width=30, bootstyle="dark-outline")
                drink_size_menu.pack(side=LEFT, padx=10, pady=10)
                self.menubuttons.append(drink_size_menu)

                inside_drink_size_menu = ttk.Menu(drink_size_menu)
                drink_size_variable = StringVar()
                for attribute in drink_size:
                    inside_drink_size_menu.add_radiobutton(label=attribute, variable=drink_size_variable,
                                                        command=lambda text=attribute, mod_menu=drink_size_menu:
                                                                self.change_text_menu(mod_menu, text))
                drink_size_menu["menu"] = inside_drink_size_menu

                self.button = ttk.Button(self.inner_frame, text="OK", command=lambda :self.click_mod_button(value,drink_type_variable.get(),drink_size_variable.get()), bootstyle="dark-outline")
                self.button.pack(side=LEFT, padx=10, pady=10)

            elif "ข้าวไก่ทอด" in key:     
                self.item_name = ttk.Label(self.inner_frame, text=key, font=('', 16, "bold"), foreground="#643200", background="#ffffff")  # Brown color for bowls
                self.item_name.pack(side=LEFT, padx=10, pady=10)

                # Bowl Topping Menu
                bowl_type_menu = ttk.Menubutton(self.inner_frame, text="ข้าวไก่ทอด", width=30, bootstyle="dark-outline")
                bowl_type_menu.pack(side=LEFT, padx=10, pady=10)
                self.menubuttons.append(bowl_type_menu)

                inside_bowl_type_menu = ttk.Menu(bowl_type_menu)
                bowl_type_variable = StringVar()
                for attribute in ["ข้าวไก่ทอด"]:
                    inside_bowl_type_menu.add_radiobutton(label=attribute, variable=bowl_type_variable,
                                                            command=lambda text=attribute, mod_menu=bowl_type_menu:
                                                                    self.change_text_menu(mod_menu, text))
                bowl_type_menu["menu"] = inside_bowl_type_menu

                bowl_topping_menu = ttk.Menubutton(self.inner_frame, text="Topping", width=30, bootstyle="dark-outline")
                bowl_topping_menu.pack(side=LEFT, padx=10, pady=10)
                self.menubuttons.append(bowl_topping_menu)

                inside_bowl_topping_menu = ttk.Menu(bowl_topping_menu)
                bowl_topping_variable = StringVar()
                for attribute in bolw_topping:
                    inside_bowl_topping_menu.add_radiobutton(label=attribute, variable=bowl_topping_variable,
                                                            command=lambda text=attribute, mod_menu=bowl_topping_menu:
                                                                    self.change_text_menu(mod_menu, text))
                bowl_topping_menu["menu"] = inside_bowl_topping_menu
                self.button = ttk.Button(self.inner_frame, text="OK", command=lambda :self.click_mod_button(value,key,bowl_topping_variable.get()), bootstyle="dark-outline")
                
                self.button.pack(side=LEFT, padx=10, pady=10)
        self.add_to_card = ttk.Button(self.inner_frame, text="Add to card", command=lambda: self.add_to_cart())
        self.add_to_card.pack(side=LEFT, padx=10, pady=10)

    def add_to_cart(self):
        print("Add to cart")
        
        self.API_show_summary = "http://127.0.0.1:8000/show_summary"
        self.API_add_to_cart = "http://127.0.0.1:8000/add_to_cart"
        self.input_json = {
            "member_id": self.app.member_id 
            }
        print(self.input_json)
        self.response_show_summary = requests.post(self.API_show_summary, json=self.input_json)
        self.response_add_to_cart = requests.post(self.API_add_to_cart, json=self.input_json)
        print(self.response_show_summary.json())
        self.app.show_frame(self.app.menu_ui)

    def click_mod_button(self,meal_id,attribute_1,attribute_2):
        print(meal_id,attribute_1,attribute_2)
    def change_text_menu(self, menubutton, text):
        menubutton.config(text=text) 

    def extract_last_layer_and_ids(self,json_data):
        last_layer_elements = {}
        for key, value in json_data.items():
            if isinstance(value, dict):
                if "id" in value:
                    last_layer_elements[key] = value["id"]
                else:
                    last_layer_elements.update(self.extract_last_layer_and_ids(value))
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict) and "id" in item:
                        last_layer_elements[key] = item["id"]
            else:
                pass

        return last_layer_elements
    
    def set_meal_name(self, meal_name):
        self.meal_name = meal_name

    def set_member_id(self, id):
        self.member_id = id




class KFCaddress(ttk.Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root)
        self.API_show_address = "http://127.0.0.1:8000/show_address"
        self.API_remove_item = "http://127.0.0.1:8000/remove_address"
        self.API_add_address = "http://127.0.0.1:8000/add_address"
        self.app = root
        self.member_id = self.app.member_id
        self.input_json = {
            "id": self.member_id  
            }
        print(self.input_json)
        self.response_show_address = requests.post(self.API_show_address, json=self.input_json)
        
        
        self.init_ui()

    def init_ui(self):

        self.main_frame = ttk.Frame(self.app)

        self.address_title = ttk.Label(self.main_frame, text="Address", font=('', 20, "bold"), foreground='#000000',background='#ffffff',relief=RIDGE)
        self.address_title.grid(padx= 450 ,sticky=N,row = 0, column = 0)
        self.main_frame2 = ttk.Frame(self.main_frame, height=600, width=750, bootstyle = "danger")
        self.main_frame2.grid(column = 0, row = 1,pady = 35,padx = 125,  sticky=W)
        self.address_frame = ScrolledFrame(self.main_frame2,height=600,width=800)
        self.address_frame.pack(side = LEFT, padx=10, pady=10)
        self.add_address_button = ttk.Button(self.address_frame, text="Add Address", bootstyle = 'danger',command=lambda: self.add_address_button_click())
        self.add_address_button.grid(pady= 20 ,sticky=N,row = 1, column = 0)
        self.back_button = ttk.Button(self.main_frame, text="Back", bootstyle = 'danger',command=lambda:self.app.show_frame(self.app.menu_ui))
        self.back_button.place(x=10,y=10)
        self.display_item(self.response_show_address)

    def display_item(self,response_show_address):
        self.index = 1
        print(response_show_address.json())
        self.item_name_list = []
        for address in response_show_address.json().items():
            self.item_name_list.append(address[0])
            self.each_item_frame = ttk.Frame(self.address_frame, width=500, height=300, bootstyle="danger",relief=RIDGE,borderwidth=1)
            self.each_item_frame.grid(padx =20, pady=25,row = self.index+1,column = 0,sticky=W)
            self.address_name_label = ttk.Label(self.each_item_frame, text=address[0], font=('', 15, "bold"), foreground='#000000',background='#ffffff',relief=RIDGE)
            self.address_name_label.grid(padx=20, pady=5,row = 0,column = 0)
            self.addrss_country_label = ttk.Label(self.each_item_frame, text='Country : ' + str(address[1]["Country"]), font=('', 10, "bold"), foreground='#000000',background='#ffffff',relief=RIDGE)
            self.addrss_country_label.grid(padx=20, pady=5,row = 1,column = 1)
            self.address_city_label = ttk.Label(self.each_item_frame, text='City :'+ str(address[1]["City"]), font=('', 10, "bold"), foreground='#000000',background='#ffffff',relief=RIDGE)
            self.address_city_label.grid(padx=20, pady=5,row = 1,column = 2)
            self.address_district_label = ttk.Label(self.each_item_frame, text='District :'+ str(address[1]["District"]), font=('', 10, "bold"), foreground='#000000',background='#ffffff',relief=RIDGE)
            self.address_district_label.grid(padx=20, pady=5,row = 1,column = 3)
            self.address_subdistrict_label = ttk.Label(self.each_item_frame, text='Subdistrict :'+ str(address[1]["Subdistrict"]), font=('', 10, "bold"), foreground='#000000',background='#ffffff',relief=RIDGE)
            self.address_subdistrict_label.grid(padx=20, pady=5,row = 2,column = 1)
            self.address_road_label = ttk.Label(self.each_item_frame, text='Road : ' + str(address[1]['Road']), font=('', 10, "bold"), foreground='#000000',background='#ffffff',relief=RIDGE)
            self.address_road_label.grid(padx=20, pady=5,row = 2,column = 2)
            self.address_house_number_label = ttk.Label(self.each_item_frame, text='House Number :'+ str(address[1]['House Number']), font=('', 10, "bold"), foreground='#000000',background='#ffffff',relief=RIDGE)
            self.address_house_number_label.grid(padx=20, pady=5,row = 2,column = 3)
            self.address_zipcode_label = ttk.Label(self.each_item_frame, text='Zipcode :'+ str(address[1]['Zip Code']), font=('', 10, "bold"), foreground='#000000',background='#ffffff',relief=RIDGE)
            self.address_zipcode_label.grid(padx=20, pady=5,row = 3,column = 1)
            self.address_type_label = ttk.Label(self.each_item_frame, text='Type :'+ str(address[1]['Type']), font=('', 10, "bold"), foreground='#000000',background='#ffffff',relief=RIDGE)
            self.address_type_label.grid(padx=20, pady=5,row = 3,column = 2)
            self.address_landmark_label = ttk.Label(self.each_item_frame, text='Landmark :'+ str(address[1]['Landmark']), font=('', 10, "bold"), foreground='#000000',background='#ffffff',relief=RIDGE)
            self.address_landmark_label.grid(padx=20, pady=5,row = 3,column = 3)
            self.address_note_label = ttk.Label(self.each_item_frame, text='Note :'+ str(address[1]['Note']), font=('', 10, "bold"), foreground='#000000',background='#ffffff',relief=RIDGE)
            self.address_note_label.grid(padx=20, pady=5,row = 4,column = 1)
            self.index = self.index + 1
        self.index = 0
        for item_name in self.item_name_list:
            self.delete_button = ttk.Button(self.address_frame, text="X", bootstyle = 'danger',command=lambda item_name=item_name: self.delete_button_click(item_name))
            self.delete_button.grid(padx=0, pady=5,row = self.index+2,column = 1)
            self.index = self.index + 1

    def delete_button_click(self,item_name):
        self.input_json = {
                    "member_id":self.member_id,
                    "address_name":item_name
                    }
        print(self.input_json)
        response_remove_item = requests.post(self.API_remove_item, json=self.input_json)
        self.response_show_address = response_remove_item
        self.app.show_frame(KFCaddress(self.app))
        # self.init_ui()


    def add_address_button_click(self):
        self.new_address_window = tk.Toplevel(self.main_frame)
        self.new_address_window.title("KFC Huh")
        self.new_address_window.geometry("500x500")

        self.new_address_name = tk.StringVar()
        self.new_address_name_label = ttk.Label(self.new_address_window, text="Address Name", font=('', 10, "bold"), foreground='#000000',background='#ffffff',relief=RIDGE)
        self.new_address_name_label.grid(padx=0, pady=0,row = 1,column = 0)
        self.entry = ttk.Entry(self.new_address_window,textvariable=self.new_address_name, width=20,font=('', 10), foreground='#a3a3a3',background='#ffffff',bootstyle="danger")
        self.entry.grid(row=1, column=1)

        self.new_country = tk.StringVar()
        self.new_country_label = ttk.Label(self.new_address_window, text="Country", font=('', 10, "bold"), foreground='#000000',background='#ffffff',relief=RIDGE)
        self.new_country_label.grid(padx=0, pady=0,row = 2,column = 0)
        self.entry = ttk.Entry(self.new_address_window,textvariable=self.new_country, width=20,font=('', 10), foreground='#a3a3a3',background='#ffffff',bootstyle="danger")
        self.entry.grid(row=2, column=1)

        self.new_city = tk.StringVar()
        self.new_city_label = ttk.Label(self.new_address_window, text="City", font=('', 10, "bold"), foreground='#000000',background='#ffffff',relief=RIDGE)
        self.new_city_label.grid(padx=0, pady=0,row = 3,column = 0)
        self.entry = ttk.Entry(self.new_address_window,textvariable=self.new_city, width=20,font=('', 10), foreground='#a3a3a3',background='#ffffff',bootstyle="danger")
        self.entry.grid(row=3, column=1)

        self.new_district = tk.StringVar()
        self.new_district_label = ttk.Label(self.new_address_window, text="District", font=('', 10, "bold"), foreground='#000000',background='#ffffff',relief=RIDGE)
        self.new_district_label.grid(padx=0, pady=0,row = 4,column = 0)
        self.entry = ttk.Entry(self.new_address_window,textvariable=self.new_district, width=20,font=('', 10), foreground='#a3a3a3',background='#ffffff',bootstyle="danger")
        self.entry.grid(row=4, column=1)

        self.new_subdistrict = tk.StringVar()
        self.new_subdistrict_label = ttk.Label(self.new_address_window, text="SubDistrict", font=('', 10, "bold"), foreground='#000000',background='#ffffff',relief=RIDGE)
        self.new_subdistrict_label.grid(padx=0, pady=0,row = 5,column = 0)
        self.entry = ttk.Entry(self.new_address_window,textvariable=self.new_subdistrict, width=20,font=('', 10), foreground='#a3a3a3',background='#ffffff',bootstyle="danger")
        self.entry.grid(row=5, column=1)

        self.new_road = tk.StringVar()
        self.new_road_label = ttk.Label(self.new_address_window, text="Road", font=('', 10, "bold"), foreground='#000000',background='#ffffff',relief=RIDGE)
        self.new_road_label.grid(padx=0, pady=0,row = 6,column = 0)
        self.entry = ttk.Entry(self.new_address_window,textvariable=self.new_road, width=20,font=('', 10), foreground='#a3a3a3',background='#ffffff',bootstyle="danger")
        self.entry.grid(row=6, column=1)

        self.new_house_number = tk.StringVar()
        self.new_house_number_label = ttk.Label(self.new_address_window, text="House number", font=('', 10, "bold"), foreground='#000000',background='#ffffff',relief=RIDGE)
        self.new_house_number_label.grid(padx=0, pady=0,row = 7,column = 0)
        self.entry = ttk.Entry(self.new_address_window,textvariable=self.new_house_number, width=20,font=('', 10), foreground='#a3a3a3',background='#ffffff',bootstyle="danger")
        self.entry.grid(row=7, column=1)

        self.new_zip = tk.StringVar()
        self.new_zip_label = ttk.Label(self.new_address_window, text="Zip code", font=('', 10, "bold"), foreground='#000000',background='#ffffff',relief=RIDGE)
        self.new_zip_label.grid(padx=0, pady=0,row = 8,column = 0)
        self.entry = ttk.Entry(self.new_address_window,textvariable=self.new_zip, width=20,font=('', 10), foreground='#a3a3a3',background='#ffffff',bootstyle="danger")
        self.entry.grid(row=8, column=1)

        self.new_type = tk.StringVar()
        self.new_type_label = ttk.Label(self.new_address_window, text="Type", font=('', 10, "bold"), foreground='#000000',background='#ffffff',relief=RIDGE)
        self.new_type_label.grid(padx=0, pady=0,row = 9,column = 0)
        self.entry = ttk.Entry(self.new_address_window,textvariable=self.new_type, width=20,font=('', 10), foreground='#a3a3a3',background='#ffffff',bootstyle="danger")
        self.entry.grid(row=9, column=1)

        self.new_type = tk.StringVar()
        self.new_type_label = ttk.Label(self.new_address_window, text="Type", font=('', 10, "bold"), foreground='#000000',background='#ffffff',relief=RIDGE)
        self.new_type_label.grid(padx=0, pady=0,row = 9,column = 0)
        self.entry = ttk.Entry(self.new_address_window,textvariable=self.new_type, width=20,font=('', 10), foreground='#a3a3a3',background='#ffffff',bootstyle="danger")
        self.entry.grid(row=9, column=1)       

        self.new_landmark = tk.StringVar()
        self.new_landmark_label = ttk.Label(self.new_address_window, text="Landmark", font=('', 10, "bold"), foreground='#000000',background='#ffffff',relief=RIDGE)
        self.new_landmark_label.grid(padx=0, pady=0,row = 10,column = 0)
        self.entry = ttk.Entry(self.new_address_window,textvariable=self.new_landmark, width=20,font=('', 10), foreground='#a3a3a3',background='#ffffff',bootstyle="danger")
        self.entry.grid(row=10, column=1)   

        self.new_note = tk.StringVar()
        self.new_note_label = ttk.Label(self.new_address_window, text="Note", font=('', 10, "bold"), foreground='#000000',background='#ffffff',relief=RIDGE)
        self.new_note_label.grid(padx=0, pady=0,row = 11,column = 0)
        self.entry = ttk.Entry(self.new_address_window,textvariable=self.new_note, width=20,font=('', 10), foreground='#a3a3a3',background='#ffffff',bootstyle="danger")
        self.entry.grid(row=11, column=1)                   

        self.button = ttk.Button(self.new_address_window, text="Confirm", bootstyle = 'danger',command=self.confirm_button_click)
        self.button.grid(row=12, column=1)
        
        
    def confirm_button_click(self):
        self.new_address = {
                        "member_id" : self.member_id,
                        "address_name" : self.new_address_name.get(),
                        "country" : self.new_country.get(),
                        "city" : self.new_city.get(),
                        "district" : self.new_district.get(),
                        "subdistrict" : self.new_subdistrict.get(),
                        "road" : self.new_road.get(),
                        "house_number" : self.new_house_number.get(),
                        "zip_code" : self.new_zip.get(),
                        "type" : self.new_type.get(),
                        "landmark" : self.new_landmark.get(),
                        "note" : self.new_note.get()
                        }
        self.response_add_address = requests.post(self.API_add_address, json=self.new_address)
        self.response_show_address = self.response_add_address
        self.app.show_frame(KFCaddress(self.app))
        self.new_address_window.destroy()


class KFCpayment(ttk.Frame):
    def __init__(self,root,*args, **kwargs):
        super().__init__(root,*args, **kwargs)
        print("asfldhjaswdehfgjklweadsfg")
        self.app = root
        self.member_id = self.app.member_id
        print(self.member_id)

        self.init_ui()

    def init_ui(self):
        self.confirm_dicr ={'payment_method':False,'address':False}
        self.main_frame = Frame(self.app)
        
        self.input_json = {
                            'member_id' : self.member_id
                            }
        self.API_order= "http://127.0.0.1:8000/check_out"       
        self.API_show_payment = "http://127.0.0.1:8000/payment"
        self.API_select_payment_method = "http://127.0.0.1:8000/select_payment_method"
        self.API_select_address = "http://127.0.0.1:8000/select_address"

        self.response_show_order = requests.post(self.API_order, json=self.input_json)
        self.response_show_payment = requests.post(self.API_show_payment, json=self.input_json)
        print(self.response_show_payment.json())



        self.back_button = ttk.Button(self.main_frame, text="Back", bootstyle = 'danger',command= lambda : self.app.show_frame(self.app.menu_ui))        
        self.back_button.place(relx=0.01,rely=0.01)


        self.payment_title = ttk.Label(self.main_frame, text = 'Payment', font=('', 20, "bold"))
        self.payment_title.pack(side=TOP, anchor=S)
        self.main_frame2 = ttk.Frame(self.main_frame, height=1000, width=600, bootstyle = "danger")
        self.main_frame2.pack(side=TOP, anchor=S)
        self.member_id_label = ttk.Label(self.main_frame2, text = 'member id : ' + self.response_show_payment.json()['member_id'], font=('', 14, "bold"))
        self.member_id_label.grid(row = 0, column = 0,padx = 10,pady = 10)
        self.order_id_label = ttk.Label(self.main_frame2, text = 'order id : ' + self.response_show_payment.json()['order_id'], font=('', 14, "bold"))
        self.order_id_label.grid(row = 0, column = 1,padx = 10,pady = 10)
        self.order_item_frame = ScrolledFrame(self.main_frame2, width= 300, height=300)
        self.order_item_frame.grid(row = 1, column = 0, rowspan=4, padx = 10, pady = 10)
        self.display_item(self.response_show_payment.json()['order_item'])
        self.payment_method_label = ttk.Label(self.main_frame2, text = 'payment method', font=('', 14, "bold"))
        self.payment_method_label.grid(row = 1, column = 1, padx=10, pady=10)
        self.choses_payment_method = tk.StringVar()
        self.payment_method_combobox = ttk.Combobox(self.main_frame2, textvariable=self.choses_payment_method)
        self.payment_method_combobox['values'] = ('qr_code', 'pay_on_delivery')
        self.payment_method_combobox.grid(row = 1, column = 2,padx=10,pady = 0)
        self.payment_address_label = ttk.Label(self.main_frame2, text = 'Address', font=('',14, "bold"))
        self.payment_address_label.grid(row = 3, column = 1, padx=10, pady=0)
        self.choses_address = tk.StringVar()
        self.payment_address_entry = tk.Entry(self.main_frame2,textvariable=self.choses_address)
        self.payment_address_entry.grid(row = 3, column = 2, padx=10, pady=10)
        self.confirm_method_button = ttk.Button(self.main_frame2, text="Confirm method", bootstyle = 'info',command=self.confirm_method_button_click)
        self.confirm_method_button.grid(row = 2, column = 1, columnspan=2, padx=10, pady=10)
        self.confirm_address_button = ttk.Button(self.main_frame2, text="Confirm address", bootstyle = 'info',command=self.confirm_address_button_click)
        self.confirm_address_button.grid(row = 4, column = 1, columnspan=2, padx=10, pady=10)

        self.out_button = ttk.Button(self.main_frame, text="Confirm payment", bootstyle = 'info',command= self.out_button_click)
        self.out_button.pack(side=TOP,padx=10,pady=10)
        self.out_button.config(state=DISABLED,text="You need to confirm address and payment method")
    def out_button_click(self):
        self.input_json = {
                            'member_id' : self.app.member_id
                            }
        self.API_success= "http://127.0.0.1:8000/payment_succsess"       

        self.response_success = requests.post(self.API_success, json=self.input_json)
        self.app.show_frame(self.app.menu_ui)
    def display_item(self,item_order):
        self.index = 0
        for item_name, price in item_order.items():
            self.each_item_label = ttk.Label(self.order_item_frame,text = 'item_name : ' + item_name + '     price : ' + str(price))
            self.each_item_label.grid(row = self.index, column = 1)
            self.index = self.index + 1
            

    def confirm_method_button_click(self):
        self.input_json= {
                        "member_id": self.member_id,
                        "payment_method": self.choses_payment_method.get()
                        }
        print(self.input_json)
        self.response_show_payment_new = requests.post(self.API_select_payment_method, json=self.input_json)
        print(self.response_show_payment_new.json())
        self.confirm_dicr['payment_method'] = True
        self.is_ready()
    
    def confirm_address_button_click(self):
        address_name = KFCaddress(self.app).response_show_address
        adddress_name_list = []
        for address in address_name.json().items():
            adddress_name_list.append(address[0])
        if self.choses_address.get() in adddress_name_list:
            print(adddress_name_list)
            
            self.input_json= {
                            "member_id": self.member_id,
                            "address_name": self.choses_address.get()
                            }
            print(self.input_json)
            self.response_show_payment_new = requests.post(self.API_select_address, json=self.input_json)
            print(self.response_show_payment_new.json())
            self.confirm_dicr['address'] = True
            self.is_ready()
        else:
            Messagebox.ok("Incorrect address","Error",bootstyle="danger")

    def is_ready(self):
        if self.confirm_dicr['payment_method'] == True and self.confirm_dicr['address'] == True:
            self.out_button.config(state=NORMAL,text="Confirm payment")
        else:
            self.out_button.config(state=DISABLED,text="You need to confirm address and payment method")
        
        
    







class KFCtransaction(ttk.Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root)
        self.app = root
        self.member_id = self.app.member_id

        
        self.init_ui()

    def init_ui(self):
        self.API_transaction = "http://127.0.0.1:8000/show_transaction"
        self.payload = {"id": self.member_id}
        self.response_transaction = requests.post(self.API_transaction,json=self.payload)

        self.main_frame = Frame(self.app)
        self.transaction_title = ttk.Label(self.main_frame, text="Transaction", font=('', 20, "bold"), foreground='#000000',background='#ffffff',relief=RIDGE)
        self.transaction_title.grid(padx= 350 ,row = 0,column = 0,sticky=N)
        self.back_button = ttk.Button(self.main_frame, text="Back", bootstyle = 'danger', command=lambda: self.back_button_click())
        self.back_button.grid(row = 0,column = 0,sticky=W)
        self.main_frame2 = ttk.Frame(self.main_frame, height=1000, width=1000, bootstyle = "danger") 
        self.main_frame2.grid(column = 0, row = 1,pady = 35,padx = 125,  sticky=W)

        self.transaction_frame = ScrolledFrame(self.main_frame2,height=3000,width=750)
        self.transaction_frame.pack(side=TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.index = 0
        for transaction in self.response_transaction.json().values():
            print(transaction)
            self.each_transaction_frame = ttk.Frame(self.transaction_frame, width=600, height=150,bootstyle="danger",relief=RIDGE,borderwidth=1)
            self.each_transaction_frame.grid(padx =75, pady=25,row = self.index+1,column = 0,sticky=W)
            self.member_id_label = ttk.Label(self.each_transaction_frame, text='member_id :' + transaction['member id'], font=('', 10, "bold"),bootstyle = "danger")
            self.member_id_label.grid(padx=20, pady=5,row = 1,column = 1)
            self.transaction_id_label = ttk.Label(self.each_transaction_frame, text='Transaction_id :' + transaction['Transaction id'], font=('', 10, "bold"),bootstyle = "danger")
            self.transaction_id_label.grid(padx=20, pady=5,row = 1,column = 2)
            self.cost_label = ttk.Label(self.each_transaction_frame, text='cost :' + str(transaction['cost']), font=('', 10, "bold"),bootstyle = "danger")
            self.cost_label.grid(padx=20, pady=5,row = 1,column = 3)
            self.payment_method_label = ttk.Label(self.each_transaction_frame, text='Payment method : '+ transaction['payment method']['_PaymentMethod__method_name'], font=('', 10, "bold"),bootstyle = "danger")
            self.payment_method_label.grid(padx=20, pady=5,row = 2,column = 1)
            self.delivery_address_label = ttk.Label(self.each_transaction_frame, text='Delivery address : '+ transaction['delivery address'], font=('', 10, "bold"),bootstyle = "danger")
            self.delivery_address_label.grid(padx=20, pady=5,row = 2,column = 2)
            self.date_label = ttk.Label(self.each_transaction_frame, text='Date : '+ transaction['Date'], font=('', 10, "bold"),bootstyle = "danger")
            self.date_label.grid(padx=20, pady=5,row = 3,column = 1)
            self.index = self.index+1
    
    def back_button_click(self):
        self.app.show_frame(self.app.menu_ui)







if __name__ == '__main__':
    app = KFCApp()
    app.mainloop()
