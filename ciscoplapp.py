import datetime
import tkinter.ttk as ttk
import webbrowser
from tkinter import *
from tkinter import messagebox
from zeroconf import ZeroConf
import psutil
import os

PROGRAM_NAME = "ScanPL-APP"


class ScanPlApp:

    def __init__(self):
        self.root = Tk()
        self.root.geometry('600x400')
        self.root.option_add("*font", 'Verdana 10')
        self.root.title(PROGRAM_NAME)

        base_folder = os.path.dirname(__file__)
        image_path = os.path.join(base_folder, 'icons')

        img = PhotoImage(file=image_path + '/scan.gif')
        self.root.tk.call('wm', 'iconphoto', self.root, img)

        self.start_icon = PhotoImage(file=image_path + '/start.gif')

        self.listbox = None
        self.treeview = None
        self.line_number_bar = None
        self.entry_search = None
        self.scale_request_count = None

        self.button_start = None
        self.button_stop = None

        self.running_scan = False

        self.make_menu_bar()
        self.make_short_cut_and_line_bar()

        self.headers = ['Host', 'Address', 'Port']
        self.headers_type = ['string', 'string', 'string', int]

        self.make_treeview_widget(self.headers)

        self.root.mainloop()

    def make_menu_bar(self):
        menu_bar = Menu(self.root)
        file_menu = Menu(menu_bar, tearoff=0)

        file_menu.add_command(label='Exit', accelerator='Alt+F4', command=self.exit)
        menu_bar.add_cascade(label='File', menu=file_menu)

        about_menu = Menu(menu_bar, tearoff=0)
        about_menu.add_command(label='About', command=self.about)
        about_menu.add_command(label='Help', command=self.help)
        menu_bar.add_cascade(label='About', menu=about_menu)

        self.root.config(menu=menu_bar)  # menu ends

    def make_short_cut_and_line_bar(self):
        # add top shortcut bar & left line number bar
        shortcut_bar = Frame(self.root, height=25, background='light sea green')
        shortcut_bar.pack(expand='no', fill='x')

        self.button_start = Button(shortcut_bar, text='Start', image=self.start_icon, relief=FLAT, command=self.start)
        self.button_start.pack(side=LEFT, padx=2, pady=2)

    def make_text_widget_and_scroll_bar_widget(self):
        # add the main content Text widget and Scrollbar widget
        content_text = Text(self.root, wrap='word')
        content_text.pack(expand='yes', fill='both')
        scroll_bar = Scrollbar(content_text)
        content_text.configure(yscrollcommand=scroll_bar.set)
        scroll_bar.config(command=content_text.yview)
        scroll_bar.pack(side='right', fill='y')

    def make_listbox_widget_and_scroll_bar_widget(self):
        self.listbox = Listbox(self.root)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=1)

        y_scroll = Scrollbar(self.listbox, orient=VERTICAL)
        x_scroll = Scrollbar(self.listbox, orient=HORIZONTAL)

        self.listbox.configure(xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)

        y_scroll.config(command=self.listbox.yview)
        x_scroll.config(command=self.listbox.xview)
        y_scroll.pack(side='right', fill='y')
        x_scroll.pack(side='bottom', fill='x')

        for n in range(100):
            self.listbox.insert(END, "linea" + str(n))

    def start(self):

        if self.avahi_running():

            self.treeview.delete(*self.treeview.get_children())  # operatore splat
            self.running_scan = True
            zc = ZeroConf()
            services = zc.search(name=None, type="_http._tcp", domain="local")

            for s in services:
                service_key = s[0]
                item = service_key.split(':', 2)
                if len(item) == 2:
                    name = item[1]
                    host = item[0]
                    if name == 'cisco-pl-app':
                        pl_app_list = [host, services[s]['address'], services[s]['port']]
                        print(name, host, services[s]['address'], services[s]['port'])
                        self.treeview_insert(pl_app_list)
            self.running_scan = False
        else:
            messagebox.showerror('Error', 'Avahi services not running ...\nInstall avahi-daemon package.')

    def make_treeview_widget(self, headers):

        self.treeview = ttk.Treeview(self.root, column=headers, show="headings")

        self.treeview.pack(side=LEFT, fill=BOTH, expand=1)

        y_scroll = Scrollbar(self.treeview, orient=VERTICAL)
        x_scroll = Scrollbar(self.treeview, orient=HORIZONTAL)

        self.treeview.configure(xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)

        y_scroll.config(command=self.treeview.yview)
        x_scroll.config(command=self.treeview.xview)
        y_scroll.pack(side='right', fill='y')
        x_scroll.pack(side='bottom', fill='x')

        for h in headers:
            index = headers.index(h)
            if index > 0:
                self.treeview.heading(h, text=h.title(),
                                      command=lambda each_=index: self.treeview_sort_column(self.treeview, each_,
                                                                                            False))
            else:
                self.treeview.heading(h, text=h.title())

        self.treeview.bind('<Double-Button-1>', self.go_web_service)

    def go_web_service(self, event):

        item = self.treeview.selection()
        item_text = self.treeview.item(item, 'values')

        ip_address = item_text[1]
        port = item_text[2]
        #print(item_text)
        webbrowser.open_new_tab('http://' + ip_address + ':' + port)

    def treeview_insert(self, values_list):

        if self.running_scan:
            self.treeview.insert('', 'end', values=values_list, tags="human")

    def get_key_int(self, item):
        return int(item[0])

    def get_key_float(self, item):
        return float(item[0])

    def get_key_string(self, item):
        return item[0].lower()

    def get_key_date(self, item):
        return datetime.datetime.strptime(item[0], "%d/%m/%Y")

    def treeview_sort_column(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]

        # print(self.headers_type[col])

        if self.headers_type[col] == 'int':
            l.sort(key=self.get_key_int, reverse=reverse)
        elif self.headers_type[col] == 'float':
            l.sort(key=self.get_key_float, reverse=reverse)
        elif self.headers_type[col] == 'string':
            l.sort(key=self.get_key_string, reverse=reverse)
        elif self.headers_type[col] == 'date':
            l.sort(key=self.get_key_date, reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        # reverse sort next time
        tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))

    def about(self):
        messagebox.showinfo('About',
                            'Scan Raspberry Pi board with Cisco PL-App.\n\nAuthor: Augusto Costantini.\nEmail: augustocostantini@gmail.com.')

    def help(self):
        messagebox.showinfo('Help',
                            'Press Play button for scan.\n\nClick on item list for connnect a device with a default browser.')

    def exit(self):

        if self.running_scan:
            messagebox.showwarning('Warning', 'Scan is still in progress. Wait for the action to terminate')
        else:
            self.root.quit()

    def avahi_running(self):

        for proc in psutil.process_iter(attrs=['pid', 'name']):

            if proc.info['name'] == 'avahi-daemon':
                print(proc.info)
                return True
        return False


if __name__ == "__main__":
    ScanPlApp()
