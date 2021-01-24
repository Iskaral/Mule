import os
from os import path
import exifread
import piexif
import shutil
import requests
import sys
from GPSPhoto import gpsphoto
import folium
import webbrowser

if path.exists(sys.argv[1]):
    pass
else:
    raise ValueError("WRONG PHOTOS PATH!")
    exit()


if path.exists(sys.argv[2]) or path.exists(os.getcwd() + "\\" + sys.argv[2]):
    pass
else:
    try:
        os.mkdir(os.getcwd() + '\\' + str(sys.argv[2]))
    except:
        os.mkdir(str(sys.argv[2]))

if path.exists(os.getcwd() + '\\' + str(sys.argv[2]) + '\\' + 'unknown'):
    pass
else:
    os.mkdir(os.getcwd() + '\\' + str(sys.argv[2]) + '\\' + 'unknown')

def year_folder(data):
    year_path = os.getcwd() + '\\' + str(sys.argv[2]) + '\\' + str((data['Date'].split('/'))[2] + "-" + (data['Date'].split('/'))[1] + "-" + (data['Date'].split('/'))[0])
    return year_path

def location_folder(year_path):
    location_path = year_path
    if os.path.isdir(f'{location_path}'):
        pass
    else:
        os.mkdir(f'{year_path}')


def move_images(year_path, a):
    location_folder = year_path
    try:
        if sys.argv[4] == "-x":
            shutil.move(sys.argv[1] + f'\\{a}',location_folder + f'\\{a}')
        else:
            shutil.copy(sys.argv[1] + f'\\{a}',location_folder + f'\\{a}')
    except:
        shutil.copy(sys.argv[1] + f'\\{a}',location_folder + f'\\{a}')

image_list = os.listdir(sys.argv[1])
image_list = [a for a in image_list if a.endswith('jpg')]
print("image list: ", image_list)

fol_map = folium.Map(location=[50.087810, 14.420460], zoom_start=4)

for a in image_list:
    data = gpsphoto.getGPSData(sys.argv[1] + f'\\{a}')
    try:
        long = data['Longitude']
        lat = data['Latitude']
    except:
        continue
    folium.Marker(location=[lat, long], popup=a, tooltip="click for photo name").add_to(fol_map)


filepath = os.getcwd() + '/' + 'The_Map.html'


for a in image_list:
    data = gpsphoto.getGPSData(sys.argv[1] + f'\\{a}')
    try:
        if sys.argv[4] == "-x":
            try:
                if data['Date']:
                    year_path = year_folder(data)
                else:
                    continue
            except:
                shutil.move(sys.argv[1] + f'\\{a}', os.getcwd() + '\\' + str(sys.argv[2]) + '\\' + 'unknown')
                continue
        else:
            try:
                if data['Date']:
                    year_path = year_folder(data)
                else:
                    continue
            except:
                shutil.copy(sys.argv[1] + f'\\{a}', os.getcwd() + '\\' + str(sys.argv[2]) + '\\' + 'unknown')
                continue
    except:
        try:
            if data['Date']:
                year_path = year_folder(data)
            else:
                continue
        except:
            shutil.copy(sys.argv[1] + f'\\{a}', os.getcwd() + '\\' + str(sys.argv[2]) + '\\' + 'unknown')
            continue
    location_folder(year_path)
    move_images(year_path, a)

try:
    if sys.argv[3] == "-m":
        fol_map.save('The_Map.html')
        webbrowser.open('file://' + filepath)
    else:
        print("no map for you")
except:
    print("no map for you")






