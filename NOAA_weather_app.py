'''
The NOAA Weather App allows you to view detailed information from weather.gov for any city in the US. 

Usage: In order to search for the weather, you need to enter the four-character station code for a particular city e.g. KNYC for New York City. 
       To find station codes, use the "Station Codes List" Tab, select the desired state from the drop-down menu and press the "Get Codes" button.
       This will retrieve a list of the station names and their codes for the selected state, which you can then use in the "Weather Conditions" Tab.

Created on 8 Jan 2018

@author: Sameer Tulshyan
'''

import tkinter as tk
import urllib.request
from tkinter import Menu
from tkinter import ttk
from tkinter import scrolledtext
from html.parser import HTMLParser
        
def _quit():
    """Function to exit the GUI"""
    win.quit()      
    win.destroy()
    exit() 

win = tk.Tk() #create the window   
win.title("Weather App") #add title 

menu_bar = Menu() #create a Menu Bar
win.config(menu=menu_bar)

# Add menu items
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Exit", command=_quit) #exit command calls the function to quit the app
menu_bar.add_cascade(label="File", menu=file_menu)
 
tabControl = ttk.Notebook(win)          #create Tab Control

tab1 = ttk.Frame(tabControl)            #create a tab 
tabControl.add(tab1, text='Weather Conditions') #display the tab

tab2 = ttk.Frame(tabControl)            #create a second tab
tabControl.add(tab2, text='Station Codes List')    

tabControl.pack(expand=1, fill="both")  
    
#Create a container frame to hold all other widgets
weather_conditions_frame = ttk.LabelFrame(tab1, text=' Current Weather Conditions ')
weather_conditions_frame.grid(column=0, row=1, padx=8, pady=4)

ENTRY_WIDTH = 25 #constant representing the width of each data entry

#Add a series of labels for each type of data
#---------------------------------------------
ttk.Label(weather_conditions_frame, text="Last Updated:").grid(column=0, row=1, sticky='E')         
updated = tk.StringVar()
updatedEntry = ttk.Entry(weather_conditions_frame, width=ENTRY_WIDTH, textvariable=updated, state='readonly')
updatedEntry.grid(column=1, row=1, sticky='W')
#---------------------------------------------
ttk.Label(weather_conditions_frame, text="Weather:").grid(column=0, row=2, sticky='E')              
weather = tk.StringVar()
weatherEntry = ttk.Entry(weather_conditions_frame, width=ENTRY_WIDTH, textvariable=weather, state='readonly')
weatherEntry.grid(column=1, row=2, sticky='W')                                  
#---------------------------------------------
ttk.Label(weather_conditions_frame, text="Temperature:").grid(column=0, row=3, sticky='E')
temp = tk.StringVar()
tempEntry = ttk.Entry(weather_conditions_frame, width=ENTRY_WIDTH, textvariable=temp, state='readonly')
tempEntry.grid(column=1, row=3, sticky='W')
#---------------------------------------------
ttk.Label(weather_conditions_frame, text="Dewpoint:").grid(column=0, row=4, sticky='E')
dew = tk.StringVar()
dewEntry = ttk.Entry(weather_conditions_frame, width=ENTRY_WIDTH, textvariable=dew, state='readonly')
dewEntry.grid(column=1, row=4, sticky='W')
#---------------------------------------------
ttk.Label(weather_conditions_frame, text="Relative Humidity:").grid(column=0, row=5, sticky='E')
rel_humi = tk.StringVar()
rel_humiEntry = ttk.Entry(weather_conditions_frame, width=ENTRY_WIDTH, textvariable=rel_humi, state='readonly')
rel_humiEntry.grid(column=1, row=5, sticky='W')
#---------------------------------------------
ttk.Label(weather_conditions_frame, text="Wind:").grid(column=0, row=6, sticky='E')
wind = tk.StringVar()
windEntry = ttk.Entry(weather_conditions_frame, width=ENTRY_WIDTH, textvariable=wind, state='readonly')
windEntry.grid(column=1, row=6, sticky='W')
#---------------------------------------------
ttk.Label(weather_conditions_frame, text="Visibility:").grid(column=0, row=7, sticky='E')
visi = tk.StringVar()
visiEntry = ttk.Entry(weather_conditions_frame, width=ENTRY_WIDTH, textvariable=visi, state='readonly')
visiEntry.grid(column=1, row=7, sticky='W')
#---------------------------------------------
ttk.Label(weather_conditions_frame, text="MSL Pressure:").grid(column=0, row=8, sticky='E')
msl = tk.StringVar()
mslEntry = ttk.Entry(weather_conditions_frame, width=ENTRY_WIDTH, textvariable=msl, state='readonly')
mslEntry.grid(column=1, row=8, sticky='W')
#---------------------------------------------
ttk.Label(weather_conditions_frame, text="Altimeter:").grid(column=0, row=9, sticky='E')
alti = tk.StringVar()
altiEntry = ttk.Entry(weather_conditions_frame, width=ENTRY_WIDTH, textvariable=alti, state='readonly')
altiEntry.grid(column=1, row=9, sticky='E')
#---------------------------------------------

#Increase the padding around each field
for child in weather_conditions_frame.winfo_children(): 
        child.grid_configure(padx=4, pady=2)    


#Create a container frame to store other widgets
weather_cities_frame = ttk.LabelFrame(tab1, text=' Latest Observation for ')
weather_cities_frame.grid(column=0, row=0, padx=8, pady=4)


ttk.Label(weather_cities_frame, text="Weather Station Code: ").grid(column=0, row=0) #create a new label for the Station Code

station_code = tk.StringVar()
station_code_combo = ttk.Combobox(weather_cities_frame, width=6, textvariable=station_code)   
                               
station_code_combo['values'] = ('KNYC') #set default to NYC Central Park Station
station_code_combo.grid(column=1, row=0)
station_code_combo.current(0) #highlight first city station code


def _get_station():
    """Function to be called when user presses get_weather_btn on Tab 1 of the GUI"""
    station = station_code_combo.get()
    get_weather_data(station)
    update_gui_from_dict()

get_weather_btn = ttk.Button(weather_cities_frame,text='Get Weather', command=_get_station).grid(column=2, row=0)

# Station City label
location = tk.StringVar()
ttk.Label(weather_cities_frame, textvariable=location).grid(column=0, row=1, columnspan=3)
# ---------------------------------------------------------------
for child in weather_cities_frame.winfo_children(): 
        child.grid_configure(padx=5, pady=4)    


#Dictionary containing keys that represent the XML Tags we are looking for
weather_data_tags_dict = {
    'observation_time': '',
    'weather': '',
    'temp_f':  '',
    'temp_c':  '',
    'dewpoint_f': '',
    'dewpoint_c': '',
    'relative_humidity': '',
    'wind_string':   '',
    'visibility_mi': '',
    'pressure_string': '',
    'pressure_in': '',
    'location': ''
    }


def get_weather_data(station_code='KLAX'):
    """Function to query the website for data based on the user-submitted station code and update the dictionary values"""
    url_general = 'http://www.weather.gov/xml/current_obs/{}.xml'
    url = url_general.format(station_code)
    request = urllib.request.urlopen( url )
    content = request.read().decode()

    # Using ElementTree to retrieve specific tags from the xml
    import xml.etree.ElementTree as ET
    xml_root = ET.fromstring(content)
    
    # Update the dictionary values with data from the xml
    for data_point in weather_data_tags_dict.keys():
            try:
                weather_data_tags_dict[data_point] = xml_root.find(data_point).text
            except: #handle the case where certain data points are not available for a station
                weather_data_tags_dict[data_point] = "-"
    

# ---------------------------------------------------------------
def update_gui_from_dict():   
    """Function to update the GUI with data from the dictionary"""   
    location.set(weather_data_tags_dict['location'])
    updated.set(weather_data_tags_dict['observation_time'].replace('Last Updated on ', ''))
    weather.set(weather_data_tags_dict['weather'])
    temp.set('{} \xb0F  ({} \xb0C)'.format(weather_data_tags_dict['temp_f'], weather_data_tags_dict['temp_c']))
    dew.set('{} \xb0F  ({} \xb0C)'.format(weather_data_tags_dict['dewpoint_f'], weather_data_tags_dict['dewpoint_c']))
    rel_humi.set(weather_data_tags_dict['relative_humidity'] + ' %')
    wind.set(weather_data_tags_dict['wind_string'])
    visi.set(weather_data_tags_dict['visibility_mi'] + ' miles')
    msl.set(weather_data_tags_dict['pressure_string'])
    alti.set(weather_data_tags_dict['pressure_in'] + ' in Hg')                         


# Second tab: Allows the user to search for Station Codes by State
weather_states_frame = ttk.LabelFrame(tab2, text=' Weather Station Codes ')
weather_states_frame.grid(column=0, row=0, padx=8, pady=4)

ttk.Label(weather_states_frame, text="Select a State: ").grid(column=0, row=0) #add a Label for this tab

state = tk.StringVar()
state_combo = ttk.Combobox(weather_states_frame, width=5, textvariable=state)         
state_combo['values'] = ('AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI',
                         'ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI',
                         'MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC',
                         'ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT',
                         'VT','VA','WA','WV','WI','WY'
                        )
state_combo.grid(column=1, row=0)
state_combo.current(0)                 # highlight first state in list (AL)


def _get_cities():
    """Function to be called when user presses get_weather_btn on Tab 2 of the GUI"""
    state = state_combo.get() #get the selected state
    get_city_station_codes(state) #call the function to get the list of codes and supply the state as an argument 

get_weather_btn = ttk.Button(weather_states_frame,text='Get Codes', command=_get_cities).grid(column=2, row=0)


scr = scrolledtext.ScrolledText(weather_states_frame, width=30, height=17, wrap=tk.WORD)
scr.grid(column=0, row=1, columnspan=3)

# ---------------------------------------------------------------
for child in weather_states_frame.winfo_children(): 
        child.grid_configure(padx=6, pady=6)   


# ---------------------------------------------------------------
def get_city_station_codes(state='ca'):
    """Function to obtain the list of cities and their station codes based on the selected state"""
    url_general = "http://w1.weather.gov/xml/current_obs/seek.php?state={}&Find=Find" #generic url missing state code
    state = state.lower()
    url = url_general.format(state) #format the url to include the selected state code
    request = urllib.request.urlopen(url) #open the url
    content = request.read().decode() #read, decode the HTML data and store it

    parser = WeatherHTMLParser() #create a parser object
    parser.feed(content) #feed the content from the webpage to the parser
    
    if len(parser.stations) != len(parser.cities): #check for data inconsistency
        print("Error: discrepancy between expected number of stations and actual")
        exit() #exit the app
    
    scr.delete('1.0', tk.END)  #clear scrolledText widget for next button click
    
    for i in range(len(parser.stations)):
        city_station = parser.cities[i] + ' (' + parser.stations[i] + ')'
        scr.insert(tk.INSERT, city_station + '\n')
    
class WeatherHTMLParser(HTMLParser):
    """Class that inherits from HTMLParser to specifically parse list of stations data from the weather.gov website"""
    def __init__(self):
        super().__init__()
        self.stations = []
        self.cities = []
        self.grab_data = False
    
    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if "display.php?stid=" in str(attr):
                cleaned_attr= str(attr).replace("('href', 'display.php?stid=", '').replace("')", '')
                self.stations.append(cleaned_attr)
                self.grab_data = True
                
    def handle_data(self, data):
        if self.grab_data:
            self.cities.append(data)
            self.grab_data = False
        


win.mainloop() #open the GUI and start the app
