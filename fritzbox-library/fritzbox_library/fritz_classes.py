# -*- coding: utf-8 -*-
import datetime
import os
import requests
import hashlib
from xml.etree import ElementTree
from tkinter import messagebox
import tkinter as tk
import re
from tkinter import ttk

class Login_Error(Exception):
    def __init__(self):
        self.occurrence = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%M")

class Communication_Error(Exception):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code
        self.message = message
        self.occurrence = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class terminationmessage:
    def __init__(self, status, message):
        if status == 0:
            self.icon = 'warning'
        elif status == 1:
            self.icon = 'error'
        else:
            raise ValueError('Status must be either 0 (Warning) or 1 (Error)')

        self.message = message
        self.create_messagebox()

    def create_messagebox(self):
        messagebox.showwarning('Program Termination', self.message, icon=self.icon)

class trackingparameter:
    def __init__(self, list, devicename):
        self.toplevel = tk.Tk()
        self.toplevel.transient()
        self.toplevel.grab_set()
        self.toplevel.bind('<Escape>', lambda event: self.cancel())
        self.toplevel.bind('<Return>', lambda event: self.ok())
        self.toplevel.title(f"Parameter for {devicename}")
        self.list = sorted(list)

        treeview_frame = tk.Frame(self.toplevel)
        treeview_frame.pack(padx=10, pady=10, fill='both', expand=True)

        scrollbar = tk.Scrollbar(treeview_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.treeview = ttk.Treeview(treeview_frame, columns=('Element'), show='headings', yscrollcommand=scrollbar.set)
        self.treeview.heading('Element', text='Element')

        for l in list:
            self.treeview.insert('', 'end', values=(l,))
        self.treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.treeview.yview)
        
        button_frame = tk.Frame(self.toplevel)
        button_frame.pack(padx=10, pady=10, anchor='s')
        ok_button = tk.Button(button_frame, text="OK", command=self.ok)
        ok_button.grid(row=0, column=0, padx=10)
        cancel_button = tk.Button(button_frame, text="Cancel", command=self.cancel)
        cancel_button.grid(row=0, column=1, padx=10)
        
        self.toplevel.update_idletasks()
        window_width = self.toplevel.winfo_reqwidth()
        window_height = self.toplevel.winfo_reqheight()
        position_right = int(self.toplevel.winfo_screenwidth()/2 - window_width/2)
        position_down = int(self.toplevel.winfo_screenheight()/2 - window_height/2)
        self.toplevel.geometry("+{}+{}".format(position_right, position_down))

        self.toplevel.wait_window(self.toplevel)

    def ok(self):
        selected_items = self.treeview.selection()
        if not selected_items or len(selected_items) < 1:
            messagebox.showerror("Error", "Please select 1 element in the list.")
            return
        else:
            try: 
                selected_values = [self.treeview.item(item)['values'][0] for item in selected_items]
                self.result = {
                    'selected_values': selected_values,
                    'ax1label': selected_values[0],
                }
            except Exception as e:
                messagebox.showerror("Error", "Please make sure to use integer numbers." + str(e))
                return
 
        self.toplevel.destroy()

    def cancel(self):
        self.result = None
        self.toplevel.destroy()

class fritzdevice:
    def __init__(self, ain, devdetail):
        self.ain = ain
        self.devdetail = devdetail
        self.allparams = self.xml_to_dict(devdetail)
        
    def xml_to_dict(self, xmlelements, parenttag=""):
        if len(xmlelements) == 0:
            return xmlelements.text
        else:
            result = {}
            for child in xmlelements:
                if len(child) == 0:
                    newtag = str(parenttag) + " - " + str(child.tag) if parenttag else child.tag
                    result[newtag] = child.text
                else:
                    result.update(self.xml_to_dict(child, child.tag))
            return result
    
    def availabletags(self):
        return sorted(list(self.allparams.keys()))
    
    def setparam(self, queryurl):
        whatdo = 0
        try:
            try:
                xmlstring = requests.get(queryurl).content
            except requests.exceptions.RequestException as e:
                raise Communication_Error("Communication Error", -1)
        except Communication_Error as ce:
            print(f"{ce.occurrence}: {ce.message} - {ce.error_code}")
            whatdo = ce.error_code
        finally:
            if whatdo == -1:
                self.allparams = self.allparams
            else:
                if xmlstring is not None:
                    xml = ElementTree.fromstring(xmlstring)
                    self.allparams = self.xml_to_dict(xml)
                else:
                    whatdo == -1
            return whatdo

    def updatedevice(self, queryurl):
        fail = 0
        try:
            try:
                requests.get(queryurl).content
            except requests.exceptions.RequestException:
                self = -1
                raise Communication_Error("Error sending command!", -1)
        except Communication_Error as ce:
            jetzt = datetime.datetime.now()
            print(f"{ce.occurrence}: {ce.message} - {ce.error_code}")
            fail = -1
        finally:
            return fail
    
    def readparam(self, paramname):
        return self.allparams[paramname]

class fritzbox:
    def __init__(self) -> None:
        PWDialog = logindialog()
        self.username = PWDialog.username
        self.password = PWDialog.password
        self.address = PWDialog.address
        if self.username is None and self.password is None:
            terminationmessage(0, "Login cancelled!")
            raise Login_Error()
        self.loginurl = self.address + "//login_sid.lua"
        self.ahaurl = self.address + "//webservices/homeautoswitch.lua"
        
        self.sid = fritzbox.get_sid(self.loginurl, self.username, self.password)
        if not self.sid:
            terminationmessage(0, f'No connection to Fritzbox! SID = {self.sid}')
            raise Login_Error()
        self.query_url = self.ahaurl + '?sid=' + self.sid
        self.devicebyname = {}
        self.devices = {}
        self.getdevices()

    def getdevices(self):
        try:
            try:
                xmlstring = requests.get(self.query_url + "&switchcmd=getdevicelistinfos").content
            except requests.exceptions.RequestException:
                raise Communication_Error("Communication to Fritzbox failed!", 1)
        except Communication_Error as ce:
            terminationmessage(ce.error_code, ce.message)
            os._exit(1)

        xml = ElementTree.fromstring(xmlstring)
        
        if xml is None or (xml.find('device') is None or not len(xml.findall('group'))):
            terminationmessage(1, "Could not get devices from Fritzbox!")
            raise Communication_Error()
        else:
            for device in xml.findall('device'):
                attributes = device.attrib
                ain = attributes['identifier']
                name = device.find('name').text
                self.devicebyname[name] = ain
                self.devices[ain] = fritzdevice(ain, device)
            for device in xml.findall('group'):
                attributes = device.attrib
                ain = attributes['identifier']
                name = device.find('name').text
                self.devicebyname[name] = ain
                self.devices[ain] = fritzdevice(ain, device)

    def updatedevice(self, ain, switchcommand):
        fail = self.devices[ain].updatedevice(self.query_url + "&switchcmd=" + switchcommand + "&ain=" + ain)
        return fail
    
    def setparam(self, ain):
        fail = self.devices[ain].setparam(self.query_url + "&switchcmd=getdeviceinfos&ain=" + ain)
        return fail
    
    @classmethod
    def get_sid(cls, loginurl, username, password):
        try:
            try:
                response = requests.get(loginurl)
            except requests.exceptions.RequestException:
                raise Communication_Error("Communication to Fritzbox failed!", 1)
        except Communication_Error as ce:
            terminationmessage(ce.error_code, ce.message)
            os._exit(1)
            
        xml = ElementTree.fromstring(response.content)
        challenge = xml.find('Challenge').text
        sid = xml.find('SID').text
        if sid == '0000000000000000' and challenge:
            pass_str = (challenge + '-' + password).encode('utf-16le')
            md5 = hashlib.md5(pass_str).hexdigest()
            challenge_response = challenge + '-' + md5
            url = loginurl + "?username=" + username + "&response=" + challenge_response
            try:
                try:
                    response = requests.get(url)
                except requests.exceptions.RequestException:
                    raise Communication_Error("Login to Fritzbox failed!", 1)
            except Communication_Error as ce:
                terminationmessage(ce.error_code, ce.message)
                os._exit(1)
            
            xml = ElementTree.fromstring(response.content)
            sid = xml.find('SID').text
            if sid != '0000000000000000':
                return sid
        else:
            if sid != '0000000000000000':
                return sid
        return None

class logindialog:
    def __init__(self):
        self.toplevel = tk.Tk()
        self.toplevel.title("Fritzbox Login")

        self.entry_frame = tk.Frame(self.toplevel)
        self.entry_frame.pack(pady=10)

        self.username_label = tk.Label(self.entry_frame, text="Username")
        self.username_entry = tk.Entry(self.entry_frame)
        self.password_label = tk.Label(self.entry_frame, text="Password")
        self.password_entry = tk.Entry(self.entry_frame, show="*")
        self.address_label = tk.Label(self.entry_frame, text="Fritzbox Address\n\" http://xxx.xxx.xxx.xxx\"")
        self.address_entry = tk.Entry(self.entry_frame)

        self.username_label.grid(row=0, column=0, sticky='ew')
        self.username_entry.grid(row=0, column=1, sticky='ew')
        self.password_label.grid(row=1, column=0, sticky='ew')
        self.password_entry.grid(row=1, column=1, sticky='ew')
        self.address_label.grid(row=2, column=0, sticky='ew')
        self.address_entry.grid(row=2, column=1, sticky='ew')

        self.button_frame = tk.Frame(self.toplevel)
        self.button_frame.pack(pady=20)

        self.login_button = tk.Button(self.button_frame, text="Login", command=self.login)
        self.cancel_button = tk.Button(self.button_frame, text="Cancel", command=self.cancel)

        self.login_button.pack(side='left')
        self.cancel_button.pack(side='left', padx=10)

        self.toplevel.columnconfigure(0, weight=1)
        self.toplevel.columnconfigure(1, weight=1)

        self.toplevel.bind('<Escape>', lambda _: self.cancel())
        self.toplevel.bind('<Return>', lambda _: self.login())

        self.toplevel.update_idletasks()
        width = self.toplevel.winfo_width()
        height = self.toplevel.winfo_height()
        x = (self.toplevel.winfo_screenwidth() // 2) - (width // 2)
        y = (self.toplevel.winfo_screenheight() // 2) - (height // 2)
        
        self.toplevel.geometry("300x" + str(height) + "+" + str(x) + "+" + str(y))
        
        self.toplevel.wait_window(self.toplevel)

    def login(self):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        self.address = self.address_entry.get()
        if self.username == "" and self.password == "":
            terminationmessage(0, "Login data not valid!")
            return
        if not self.url_test(self.address):
            terminationmessage(0, "Not a valid URL for Fritzbox!")
            return

        self.toplevel.destroy()
    
    def cancel(self):
        self.username = None
        self.password = None
        self.address = None
        
        self.toplevel.destroy()

    def url_test(self, string):
        regex = r'https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

        if re.search(regex, string, re.IGNORECASE) or string == "http://fritz.box":
            return True
        else:
            return False

class DeviceDialog:
    def __init__(self, tuples):
        self.toplevel = tk.Tk()
        self.toplevel.transient()
        self.toplevel.grab_set()
        self.toplevel.bind('<Escape>', lambda event: self.cancel())
        self.toplevel.bind('<Return>', lambda event: self.ok())
        self.tuples = tuples
        self.toplevel.title("Device Selection")

        treeview_frame = tk.Frame(self.toplevel)
        treeview_frame.pack(padx=10, pady=10, fill='both', expand=True)

        scrollbar = tk.Scrollbar(treeview_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.treeview = ttk.Treeview(treeview_frame, columns=('Tuple 1', 'Tuple 2'), show='headings', yscrollcommand=scrollbar.set)
        self.treeview.heading('Tuple 1', text='Name')
        self.treeview.heading('Tuple 2', text='Identifier')

        for t in tuples:
            self.treeview.insert('', 'end', values=t)
        self.treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.treeview.yview)
        
        button_frame = tk.Frame(self.toplevel)
        button_frame.pack(padx=10, pady=10, anchor='s')
        ok_button = tk.Button(button_frame, text="OK", command=self.ok)
        ok_button.grid(row=0, column=0, padx=10)
        cancel_button = tk.Button(button_frame, text="Cancel", command=self.cancel)
        cancel_button.grid(row=0, column=1, padx=10)
        
        self.toplevel.update_idletasks()
        window_width = self.toplevel.winfo_reqwidth()
        window_height = self.toplevel.winfo_reqheight()
        position_right = int(self.toplevel.winfo_screenwidth()/2 - window_width/2)
        position_down = int(self.toplevel.winfo_screenheight()/2 - window_height/2)
        self.toplevel.geometry("+{}+{}".format(position_right, position_down))

        self.toplevel.wait_window(self.toplevel)

    def ok(self):
        selected_items = self.treeview.selection()
        if not selected_items:
            messagebox.showerror("Error", "Please select a tuple.")
            return
        else:
            selected_item = selected_items[0]
            self.result = self.treeview.item(selected_item)['values']
        self.toplevel.destroy()

    def cancel(self):
        self.result = None
        self.toplevel.destroy()