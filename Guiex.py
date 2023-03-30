#  https://realpython.com/python-gui-tkinter/

#import tkinter as tk
from tkinterweb import HtmlFrame #import the HTML browser
try:
  import tkinter as tk #python3
except ImportError:
  import Tkinter as tk #python2



window = tk.Tk()
window.title("Simple GUI")

window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

webframe = HtmlFrame(window)
frm_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
btn_open = tk.Button(frm_buttons, text="Open")
btn_save = tk.Button(frm_buttons, text="Save As...")

btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5)

frm_buttons.grid(row=0, column=0, sticky="ns")
webframe.grid(row=0, column=1, sticky="nsew")

#webframe.load_website("Leaflet.html") #load a website
#webframe.pack(fill="both", expand=True) #attach the HtmlFrame widget to the parent window
webframe.load_file('file://C:\\Users\\624445\\Downloads\\Python\\Logbook\\Leaflet.html') #load a file 


#webview.create_window('tutorialspoint', 'https://www.tutorialspoint.com')
#webview.start()

window.mainloop()

