"""
__name__ = "Automated batch radiance image"
__description__ = "Create all the sky and oct files for all daytime hours for and generate bat files for each camera, then run the simulations"
__author__ = "Byron Mardas, byron@byronmardas.com"
__date__ = "September 2017"
__version__ = "0.2.1"
__version_date__ = "May 2021"
__status__ =  "creating_stage"
__changelog__ = "added field of view functionality"
__todo__ = ...
"""


# load packages
import os
import glob
import tkinter as tk
from tkinter.filedialog import askdirectory, askopenfilename
from fnmatch import fnmatch
import urllib.request
from shutil import copyfile


# check if view360stereo.cal library is downloaded, if not download it
# if not os.path.isfile("C:\\Radiance\\lib\\view360stereo.cal"):
#     urllib.request.urlretrieve(
#        "https://www.radiance-online.org/cgi-bin/viewcvs.cgi/ray/src/cal/cal/view360stereo.cal?revision=1.3",
#        "C:\\Radiance\\lib\\view360stereo.cal")
# else:
#    pass


# pop-up when initiating the script to define the folder
root = tk.Tk()
root.geometry("2x2")
f = askdirectory()  # create pop up to select folder
root.withdraw()  # close pop up window
directory = str(f)  # get string of directory set above


# Convert any datetime to HOY
def date2Hour(month, day, hour):
    numOfDays = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    # dd = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    JD = numOfDays[int(month) - 1] + int(day)
    return (JD - 1) * 24 + float(hour)


# read the IMG.bat file to get the camera / views and use them to generate the bat files.
def IMGBatFile():
    vpX = [];    vpY = [];    vpZ = [];    vdX = [];    vdY = [];    vdZ = []; vuX = []; vuY = []; vuZ = []; Quality = [];
    j = ((glob.glob(directory + "/*IMG.bat")[0]))
    for lines in (open(j, "r")).readlines():
        if lines.count("rpict") == 1:
            vpX.append(round(float(lines.split("-vp")[1].split(" ")[1]),2))
            vpY.append(round(float(lines.split("-vp")[1].split(" ")[2]),2))
            vpZ.append(round(float(lines.split("-vp")[1].split(" ")[3]),2))

            vdX.append(round(float(lines.split("-vd")[1].split(" ")[1]),2))
            vdY.append(round(float(lines.split("-vd")[1].split(" ")[2]),2))
            vdZ.append(round(float(lines.split("-vd")[1].split(" ")[3]),2))

            vuX.append(round(float(lines.split("-vu")[1].split(" ")[1]),2))
            vuY.append(round(float(lines.split("-vu")[1].split(" ")[2]),2))
            vuZ.append(round(float(lines.split("-vu")[1].split(" ")[3]),2))

            Quality.append(" -ps" + str(lines.split("-ps")[1].split("-e")[0]))
        else: None
    return len(vpX), vpX , vpY, vpZ, vdX, vdY, vdZ, vuX, vuY, vuZ, Quality[0]


# colours
bg_colour = "white"
button_colour = "wheat1"
general_bg_colour = "grey87"
# "LightSteelBlue3"


# create the tkinter interface
main = tk.Tk()  # create a window for tkinter
main.geometry("400x950")  # define the size of the window
main.configure(background=general_bg_colour)
main.title("BM - Radiance Image Automation")  # title for the window


"""
Start of all the option drop-downs
for Sky type
analysis period
"""


# create drop-down menu for sky type
Sky_type_Var = tk.StringVar(main)
choices = ['Climate', 'Sunny']
Sky_type_Var.set(choices[1])
popupMenu = tk.OptionMenu(main, Sky_type_Var, *choices)
tk.Label(main, text="Choose sky type", background=general_bg_colour, font=("Helvetice", 12)).place(x=47, y=67)
popupMenu["menu"].config(bg=button_colour, activebackground=general_bg_colour, activeforeground="black")
popupMenu.config(bg=button_colour, bd="0", activebackground=general_bg_colour, activeforeground="black")
popupMenu.place(x=275, y=67)


# function to call the drop-down choice
def SkyType():
    return Sky_type_Var.get()


# create drop-down menu for simulation period
Period_Var = tk.StringVar(main)
periods = ['Annual','Daily','Single Hour','Annual-10min']
Period_Var.set(periods[0])
popupMenu = tk.OptionMenu(main, Period_Var, *periods)
tk.Label(main, text="Simulation period", background=general_bg_colour, font=("Helvetice", 12)).place(x=47, y=100)
popupMenu["menu"].config(bg=button_colour, activebackground=general_bg_colour, activeforeground="black")
popupMenu.config(bg=button_colour, bd="0", activebackground=general_bg_colour, activeforeground="black")
popupMenu.place(x=275, y=100)


# function to call the drop-down choice
def Period_DropDown():
    return Period_Var.get()


# create drop-down menu for simulation period
DailyMonth_Var = tk.StringVar(main)
DailyMonths = ['January','February','March','April','May','June','July','August','September','October','November','December']
DailyMonth_Var.set(DailyMonths[2])
popupMenu = tk.OptionMenu(main, DailyMonth_Var, *DailyMonths)
tk.Label(main, text="Month", background=general_bg_colour, font=("Helvetice", 9)).place(x=47, y=138)
popupMenu["menu"].config(bg=button_colour, activebackground=general_bg_colour, activeforeground="black")
popupMenu.config(bg=button_colour, bd="0", activebackground=general_bg_colour, activeforeground="black")
popupMenu.place(x=40, y=160)


# function to call the drop-down choice
def Month_DropDown():
    return DailyMonth_Var.get()


# create drop-down menu for simulation period
DailyDay_Var = tk.StringVar(main)
DailyDays = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
DailyDay_Var.set(DailyDays[20])
popupMenu = tk.OptionMenu(main, DailyDay_Var, *DailyDays)
tk.Label(main, text="Day", background=general_bg_colour, font=("Helvetice", 9)).place(x=167, y=138)
popupMenu["menu"].config(bg=button_colour, activebackground=general_bg_colour, activeforeground="black")
popupMenu.config(bg=button_colour, bd="0", activebackground=general_bg_colour, activeforeground="black")
popupMenu.place(x=160, y=160)


# function to call the drop-down choice
def Day_DropDown():
    return DailyDay_Var.get()


# create drop-down menu for simulation period
DailyHour_Var = tk.StringVar(main)
DailyHours = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24']
DailyHour_Var.set(DailyHours[11])
popupMenu = tk.OptionMenu(main, DailyHour_Var, *DailyHours)
tk.Label(main, text="Hour", background=general_bg_colour, font=("Helvetice", 9)).place(x=287, y=138)
popupMenu["menu"].config(bg=button_colour, activebackground=general_bg_colour, activeforeground="black")
popupMenu.config(bg=button_colour, bd="0", activebackground=general_bg_colour, activeforeground="black")
popupMenu.place(x=280, y=160)


# function to call the drop-down choice
def Hour_DropDown():
    return DailyHour_Var.get()


# input area for number of cpu cores to use
north_label = tk.Label(main, width=48, text="Angle to rotate sky (if needed) :", background=general_bg_colour,
                     font=("Helvetica", 12)).place(x=-70, y=220)
north = tk.Entry(main, width=5, background=bg_colour, justify="center")  # create an entry box
north.insert(0,"0")
north.place(x=285, y=224)  # entry box in grid
north.focus_set()


# function to call the value set in entry box
def north_lim():
    return north.get()


"""
End of all the option drop-downs
for Sky type
analysis period

"""


# create function to make the parallel execution bat
def Parallel_Basefile(filename, bats, cores):
    f_parallel = open(directory + "\\parallel_" + filename + ".bat", "w")
    f_parallel.write("@echo off\n")
    f_parallel.write("setlocal enableDelayedExpansion\n")
    f_parallel.write("\n\n")
    f_parallel.write('if /i "%~1" equ "/O" (\n')
    f_parallel.write('  set "lockHandle=1"\n')
    f_parallel.write('  set "showOutput=1"\n')
    f_parallel.write(') else (\n')
    f_parallel.write('  set "lockHandle=1^>nul 9"\n')
    f_parallel.write('  set "showOutput="\n')
    f_parallel.write(')\n\n')
    for i in range(len(bats)):
        f_parallel.write('::: start /min ' + str(bats[i]) + '\n')  # "/min" will make sure that everything runs in the background
    f_parallel.write('\n')
    f_parallel.write('set "maxProc=' + str(int(cores)) + '"\n')
    f_parallel.write('\n')
    f_parallel.write('for /l %%N in (1 1 %maxProc%) do set "cpu%%N="\n')
    f_parallel.write('  set "lock="\n')
    f_parallel.write('  for /f "skip=1 delims=-+ " %%T in ')
    f_parallel.write("('2^>nul wmic os get localdatetime') do (\n")
    f_parallel.write('      set "lock=%%T"\n')
    f_parallel.write("      goto :break\n")
    f_parallel.write("  )\n")
    f_parallel.write("  :break\n")
    f_parallel.write('  set "lock=%temp%\\lock%lock%_%random%_"\n')
    f_parallel.write("\n")
    f_parallel.write('  set /a "startCount=0, endCount=0"\n')
    f_parallel.write("\n")
    f_parallel.write('  for /l %%N in (1 1 %macProc%) do set "endProc%%N="\n')
    f_parallel.write("\n")
    f_parallel.write("  set launch=1\n")
    f_parallel.write('  for /f "tokens=* delims=:" %%A in ')
    f_parallel.write("('findstr /b ")
    f_parallel.write('"')
    f_parallel.write(":::")
    f_parallel.write('"')
    f_parallel.write(" ")
    f_parallel.write('"')
    f_parallel.write("%~f0")
    f_parallel.write('"')
    f_parallel.write("') do (\n")
    f_parallel.write("      if !startCount! lss %maxProc% (\n")
    f_parallel.write('          set /a "startCount+=1, nextProc=startCount"\n')
    f_parallel.write("      ) else (\n")
    f_parallel.write("          call :wait\n")
    f_parallel.write("      )\n")
    f_parallel.write("      set cmd!nextProc!=%%A\n")
    f_parallel.write("      if defined showOutput echo ---------------------------------\n")
    f_parallel.write("      echo !time! - proc!nextProc!: starting %%A\n")
    f_parallel.write("      2>nul del %lock%!nextProc!\n")
    f_parallel.write('      start /b "" cmd /c %lockHandle%^>"%lock%!nextProc!" 2^>^&1 !cpu%%N! %%A\n')
    f_parallel.write("  )\n")
    f_parallel.write('  set "launch="\n')
    f_parallel.write("\n")
    f_parallel.write(":wait\n")
    f_parallel.write("  for /l %%N in (1 1 %startCount%) do 2>nul (\n")
    f_parallel.write('      if not defined endProc%%N if exist "%lock%%%N" 9>>"%lock%%%N" (\n')
    f_parallel.write("          if defined showOutput echo =================================\n")
    f_parallel.write("          echo !time! - proc%%N: finished !cmd%%N!\n")
    f_parallel.write('          if defined showOutput type "%lock%%%N"\n')
    f_parallel.write("          if defined launch (\n")
    f_parallel.write("              set nextProc=%%N\n")
    f_parallel.write("              exit /b\n")
    f_parallel.write("          )\n")
    f_parallel.write('          set /a "endCount+=1, endProc%%N=1"\n')
    f_parallel.write("      )\n")
    f_parallel.write("  )\n")
    f_parallel.write("  if %endCount% lss %startCount% (\n")
    f_parallel.write("      1>nul 2>nul ping /n 2 ::1\n")
    f_parallel.write("      goto :wait\n")
    f_parallel.write("  )\n")
    f_parallel.write("\n")
    f_parallel.write("2>nul del %lock%*\n")
    f_parallel.write("if defined showOutput echo =====================================\n")


# add function to copy epw into working folder for later use (make sure to call this function only once)
def LoadEPW():
    f_loadEpw = askopenfilename()
    copyfile(f_loadEpw, directory + "\\" + (f.split("/"))[-1])


# button to execute the above copy of the epw file
Load_EPW_Button = tk.Button(main, text="Load EPW file", width=48, background=bg_colour,
                            activebackground=general_bg_colour,
                            activeforeground="black", font=("Helvetica", 9), command=lambda: LoadEPW())
Load_EPW_Button.place(x=30, y=15)  # SavePercentages_button.grid(row=3,column = 0)


# read the epw from the working directory and get important values
# Longitude, Latitude, Meridian Hour, Diffuse Radiation, Direct Radiation, Month, Day and Hour
# all these will be used later to filter the data and create the appropriate sky files.
def Read_EPW(HOY):
    f_epw = open((glob.glob(directory + "/*.epw")[0]), "r")
    lines = f_epw.readlines()
    longitude = []
    latitude = []
    meridian = []
    DiffuseRadiation = []
    DirectRadiation = []
    month = []
    day = []
    hour = []
    longitude.append(str(float(lines[0].split(",")[7]) * (-1)))
    latitude.append(lines[0].split(",")[6])
    meridian.append(str((float(lines[0].split(",")[8]) * (-1) * 60) / 4))
    DiffuseRadiation.append(lines[HOY + 8].split(",")[15])
    DirectRadiation.append(lines[HOY + 8].split(",")[14])
    month.append(lines[HOY + 8].split(",")[1])
    day.append(lines[HOY + 8].split(",")[2])
    hour.append(lines[HOY + 8].split(",")[3])
    return longitude, latitude, meridian, DiffuseRadiation, DirectRadiation, month, day, hour


def EPW_Datetime():
    f_epw = open((glob.glob(directory + "/*.epw")[0]), "r")
    lines = f_epw.readlines()
    month = []
    day = []
    hour = []
    radiation = []
    if Period_DropDown() == "Annual" or Period_DropDown() == "Annual-10min":
        for i in range(8760):
            radiation.append(lines[i + 8].split(",")[15])
            month.append(lines[i + 8].split(",")[1])
            day.append(lines[i + 8].split(",")[2])
            hour.append(lines[i + 8].split(",")[3])
    elif Period_DropDown() == "Daily":
        DailyHOY = int(date2Hour((DailyMonths.index(Month_DropDown())+1),Day_DropDown(),1))
        for j in range(DailyHOY-1,DailyHOY+23):
            radiation.append(lines[j + 8].split(",")[15])
            month.append(lines[j + 8].split(",")[1])
            day.append(lines[j + 8].split(",")[2])
            hour.append(lines[j + 8].split(",")[3])
    elif Period_DropDown() == "Single Hour":
        HourlyHOY = int(date2Hour((DailyMonths.index(Month_DropDown())+1),Day_DropDown(),Hour_DropDown()) - 1)
        radiation.append(lines[HourlyHOY + 8].split(",")[15])
        month.append(lines[HourlyHOY + 8].split(",")[1])
        day.append(lines[HourlyHOY + 8].split(",")[2])
        hour.append(lines[HourlyHOY + 8].split(",")[3])
    return month, day, hour, radiation


# function to read all the relevant options and create sky files
# this will read the type of sky used and either create generic CIE skies or use the EPW to generate climate based
# sky files
def Sky_File(longitude, latitude, meridian, month, day, hour, HOY):
    if len(north_lim()) == 0:
        NorthArrow = "0"
    else: NorthArrow = str(int(north_lim()))
    Directory = directory.replace("/", "\\")
    Temp_Sky_Directory = Directory + "\\SKYs"
    if not os.path.exists(Temp_Sky_Directory):
        os.makedirs(Temp_Sky_Directory)
    if SkyType() == "Sunny":
        f_sky = open(Temp_Sky_Directory + "\\" + str("%04d" % HOY) + "_" + month + "_" + day + "_" + str('%.2f' % float(hour)) + ".sky", "w")
        f_sky.write(
            "!gensky " + month + " " + day + " " + str(hour) + " +s -a " + longitude + " -o " + latitude + " -m " + meridian + " | xform -rz " + NorthArrow + "\n")
        f_sky.write("skyfunc glow sky_mat\n")
        f_sky.write("0\n0\n4\n")
        f_sky.write(".97 .97 1.431538 0\n")
        f_sky.write("sky_mat source sky\n0\n0\n4\n0 0 1 180\n")
        f_sky.write("skyfunc glow ground_glow\n")
        f_sky.write("0\n0\n4\n.3 .3 .3 0\n")
        f_sky.write("ground_glow source ground\n0\n0\n4\n0 0 -1 180\n")
        f_sky.close()
    if SkyType() == "Climate":
        f_sky = open(Temp_Sky_Directory + "\\" + str("%04d" % HOY) + "_" + month + "_" + day + "_" + str('%.2f' % float(hour)) + ".sky", "w")
        f_sky.write(
            "!gendaylit " + month + " " + day + " " + str(hour) + " -a " + Read_EPW(9)[1][0] + " -o " + Read_EPW(9)[0][
                0] + " -m " + Read_EPW(9)[2][0] + " -W " + Read_EPW(HOY)[4][0] + " " + Read_EPW(HOY)[3][
                0] + " -O 0 | xform -rz 0.0\n")
        f_sky.write("skyfunc glow sky_mat\n")
        f_sky.write("0\n0\n4\n")
        f_sky.write(".97 .97 1.431538 0\n")
        f_sky.write("sky_mat source sky\n0\n0\n4\n0 0 1 180\n")
        f_sky.write("skyfunc glow ground_glow\n")
        f_sky.write("0\n0\n4\n.3 .3 .3 0\n")
        f_sky.write("ground_glow source ground\n0\n0\n4\n0 0 -1 180\n")
        f_sky.close()


# function and button to execute the sky and oct file functions
def Create_Sky_Files():
    _longitude = Read_EPW(9)[1][0]
    _latitude = Read_EPW(9)[0][0]
    _meridian = Read_EPW(9)[2][0]
    _month = EPW_Datetime()[0]
    _day = EPW_Datetime()[1]
    _hour = EPW_Datetime()[2]
    _radiation = EPW_Datetime()[3]
    if Period_DropDown() == "Annual":
        for i in range(8760):
            if int(_radiation[i]) > 10:
                (Sky_File(_longitude, _latitude, _meridian, _month[i], _day[i], _hour[i], i))
                (CreateBats(_month[i], _day[i], _hour[i], i))
    elif Period_DropDown() == "Annual-10min":
        for i in range(8760):
            if int(_radiation[i]) > 10:
                for m in [0.17,0.33,0.5,0.67,0.83,1]:
                    _hourM = int(_hour[i]) + m
                    (Sky_File(_longitude, _latitude, _meridian, _month[i], _day[i], _hourM, i))
                    (CreateBats(_month[i], _day[i], _hourM, i))
    elif Period_DropDown() == "Daily":
        DailyHOY = date2Hour((DailyMonths.index(Month_DropDown())+1),Day_DropDown(),1)
        for j in range(24):
            DHoy = DailyHOY + j
            if int(_radiation[j]) > 10:
                (Sky_File(_longitude, _latitude, _meridian, _month[j], _day[j], _hour[j], DHoy))
                (CreateBats(_month[j], _day[j], _hour[j], DHoy))
    elif Period_DropDown() == 'Single Hour':
        HourlyHOY = date2Hour((DailyMonths.index(Month_DropDown())+1),Day_DropDown(),Hour_DropDown()) - 1
        if int(_radiation[0]) > 10:
            (Sky_File(_longitude, _latitude, _meridian, _month[0], _day[0], _hour[0], HourlyHOY))
            (CreateBats(_month[0], _day[0], _hour[0], HourlyHOY))


# input area for number of cpu cores to use
low_label = tk.Label(main, width=48, text="Number of cpu cores to use :", background=general_bg_colour,
                     font=("Helvetica", 12)).place(x=-70, y=250)
low = tk.Entry(main, width=5, background=bg_colour, justify="center")  # create an entry box
low.insert(0,"12")
low.place(x=285, y=254)  # entry box in grid
low.focus_set()


# function to call the value set in entry box
def low_lim():
    return low.get()


# define the list of all .bat files
def OctBats():  # create function to list all files within folder and subfolder names *Rad.bat
    BATS = []
    for path, subdirs, files in os.walk(directory + "\\OCTs"):
        for name in files:
            if fnmatch(name, "*.bat"):
                BATS.append(
                    os.path.join(path, name))  # join the path of the file with the file name to get the full file path
    return BATS


# get the x,y,z out of the pts file and create a list with each grid point
def Points():
    # find and open any pts file located within the folder.
    g = open((glob.glob(directory + "/*.pts")[0]), "r")
    lines = g.readlines()
    pointsX = []
    pointsY = []
    pointsZ = []
    for x in lines:
        pointSplit = x.split("\t")
        pointsX.append(pointSplit[0])
        pointsY.append(pointSplit[1])
        pointsZ.append(pointSplit[2])
    return pointsX, pointsY, pointsZ


# title for radiance setup and execution section
tk.Label(main, text="Setup Radiance scene and run simulation", background=general_bg_colour,
         font=("Helvetice", 12)).place(x=47, y=300)


# create drop-down menu for simulation quality
RadQ_Var = tk.StringVar(main)
RadQualities = ['As Base Image','Draft (choose this for Annual)','Good','Best']
RadQ_Var.set(RadQualities[1])
popupMenu = tk.OptionMenu(main, RadQ_Var, *RadQualities)
tk.Label(main, text="Image Quality", background=general_bg_colour, font=("Helvetice", 12)).place(x=47, y=515)
popupMenu["menu"].config(bg=button_colour, activebackground=general_bg_colour, activeforeground="black")
popupMenu.config(bg=button_colour, bd="0", activebackground=general_bg_colour, activeforeground="black")
popupMenu.place(x=170, y=520)


# function to call the drop-down choice
def RadQ_DropDown():
    return RadQ_Var.get()


# create drop-down menu for camera type
CameraType = tk.StringVar(main)
Cameras = ['FishEye','Perspective','Panorama']
CameraType.set(Cameras[0])
popupMenu = tk.OptionMenu(main, CameraType, *Cameras)
tk.Label(main, text="Camera type", background=general_bg_colour, font=("Helvetice", 12)).place(x=47, y=370)
popupMenu["menu"].config(bg=button_colour, activebackground=general_bg_colour, activeforeground="black")
popupMenu.config(bg=button_colour, bd="0", activebackground=general_bg_colour, activeforeground="black")
popupMenu.place(x=170, y=370)


# function to call the drop-down choice
def CameraType_down():
    return CameraType.get()


# input area for field of view angle Horizontal
vh_label = tk.Label(main, width=48, text="horizontal view angle (vh) :", background=general_bg_colour,
                     font=("Helvetica", 12)).place(x=-70, y=405)
vh_fov = tk.Entry(main, width=5, background=bg_colour, justify="center")  # create an entry box
vh_fov.insert(0,"60")
vh_fov.place(x=285, y=410)  # entry box in grid
vh_fov.focus_set()


# function to call the value set in entry box
def hor_fov():
    return vh_fov.get()
    

# input area for field of view angle Horizontal
vv_label = tk.Label(main, width=48, text="vertical view angle (vv) :", background=general_bg_colour,
                     font=("Helvetica", 12)).place(x=-70, y=435)
vv_fov = tk.Entry(main, width=5, background=bg_colour, justify="center")  # create an entry box
vv_fov.insert(0,"40")
vv_fov.place(x=285, y=440)  # entry box in grid
vv_fov.focus_set()


# function to call the value set in entry box
def ver_fov():
    return vv_fov.get()


# create a single .bat file for each grid point
# this is to create a .bat file for radiance 360° view with stereoscopic cameras
def CreateBats(month, day, hour, HOY):
    if RadQ_DropDown() == "Draft (choose this for Annual)":
        radQual = ("  -ps 8 -pt 0.15 -pj 0.6 -dj 0 -ds 0.5 -dt 0.5 -dc 0.25 -dr 0 -dp 64 -st 0.85 "
                "-ab 1 -ad 512 -as 256 -ar 128 -aa 0.500 -lr 4 -lw 0.050 -av 0 0 0    ")
    elif RadQ_DropDown() == "As Base Image":
        radQual = (str(IMGBatFile()[10]))
    elif RadQ_DropDown() == "Good":
        radQual = ("  -ps 8 -pt 0.15 -pj 0.6 -dj 0 -ds 0.5 -dt 0.5 -dc 0.25 -dr 0 -dp 64 -st 0.85 "
                "-ab 4 -ad 1024 -as 512 -ar 128 -aa 0.1500 -lr 4 -lw 0.050 -av 0 0 0    ")
    elif RadQ_DropDown() == "Best":
        radQual = ("  -ps 8 -pt 0.15 -pj 0.6 -dj 0 -ds 0.5 -dt 0.5 -dc 0.25 -dr 0 -dp 64 -st 0.85 "
                "-ab 6 -ad 2056 -as 1024 -ar 512 -aa 0.100 -lr 4 -lw 0.050 -av 0 0 0    ")
    OCTBATS = OctBats()
    Directory = directory.replace("/", "\\")
    Temp_Oct_Directory = directory + "\\OCTs"
    Temp_Bat_Directory = Directory + "\\BATs"
    Temp_HDR_Directory = Directory + "\\HDRs"
    if not os.path.exists(Temp_Oct_Directory):
        os.makedirs(Temp_Oct_Directory)
    if not os.path.exists(Temp_Bat_Directory):
        os.makedirs(Temp_Bat_Directory)
    if not os.path.exists(Temp_HDR_Directory):
        os.makedirs(Temp_HDR_Directory)
    h = open(Temp_Bat_Directory + "\\" + str("%04d" % HOY) + "_" + month + "_" + day + "_" + str('%.2f' % float(hour)) + "_glare.bat", "w")
    h.write("SET RAYPATH=.;C:/Radiance/lib\n")
    h.write("PATH=C:\\Radiance\\bin\\;$PATH\n")
    # e.write("REM HOY: " + str(HOY) + "\n")
    h.write("oconv -r 2048 -f " + (glob.glob(directory + "\\*.rad")[1]) + " ")
    h.write(Directory + "\\SKYs\\" + str("%04d" % HOY) + "_" + month + "_" + day + "_" + str('%.2f' % float(hour)) + ".sky ")
    h.write((glob.glob(directory + "\\*.rad")[
                 0]) + " > " + Temp_Oct_Directory + "\\" + str(
        "%04d" % HOY) + "_" + month + "_" + day + "_" + str('%.2f' % float(hour)) + ".oct")
    h.write("\n")
    # for i in range(len(Points()[0])):
    for g in range(IMGBatFile()[0]):
        if CameraType_down() == "Perspective":
            ambfile = str("%04d" % HOY) + "_" + month + "_" + day + "_" + str(hour) + "_" + str(g) + ".amb"
            unffile = str("%04d" % HOY) + "_" + month + "_" + day + "_" + str(hour) + "_" + str(g) + ".unf"
            hdrfile = str("%04d" % HOY) + "_" + month + "_" + day + "_" + str(hour) + "_" + str(g) + ".hdr"
            temp =  str("%04d" % HOY) + "_" + month + "_" + day + "_" + str(hour) + "_" + str(g) + ".txt"
            h.write("rpict -t 10 -vth -vp " + str(IMGBatFile()[1][g]) + " " + str(IMGBatFile()[2][g]) + " " + str(IMGBatFile()[3][g]) + " "
                    "-vd " + str(IMGBatFile()[4][g]) + " " + str(IMGBatFile()[5][g]) + " " + str(IMGBatFile()[6][g]) + " "
                    "-vu " + str(IMGBatFile()[7][g]) + " " + str(IMGBatFile()[8][g]) + " " + str(IMGBatFile()[9][g]) + " "
                    "-vh " + hor_fov() + " -vv " + ver_fov() + " -vs 0.000 -vl 0.000 -x 800 -y 800 -af ")
            h.write(Temp_Bat_Directory + "\\" + ambfile)
            h.write(radQual)
            h.write(Temp_Oct_Directory + "\\" + str("%04d" % HOY) + "_" + month + "_" + day + "_" + str('%.2f' % float(hour)) + ".oct")
            h.write(" > ")
            h.write(Temp_Bat_Directory + "\\" + unffile)
            h.write("\npfilt -1 -r .6 -x/2 -y/2 ")
            h.write(Temp_Bat_Directory + "\\" + unffile)
            h.write(" > ")
            h.write(Temp_HDR_Directory + "\\" + hdrfile)
            h.write("\n")
            h.write("\n")
            h.write("\ndel " + Temp_Bat_Directory + "\\" + unffile + "\n")
            h.write("\ndel " + Temp_Bat_Directory + "\\" + ambfile + "\n")
        elif CameraType_down() == "FishEye":
            ambfile = str("%04d" % HOY) + "_" + month + "_" + day + "_" + str(hour) + "_" + str(g) + ".amb"
            unffile = str("%04d" % HOY) + "_" + month + "_" + day + "_" + str(hour) + "_" + str(g) + ".unf"
            hdrfile = str("%04d" % HOY) + "_" + month + "_" + day + "_" + str(hour) + "_" + str(g) + ".hdr"
            temp =  str("%04d" % HOY) + "_" + month + "_" + day + "_" + str(hour) + "_" + str(g) + ".txt"
            h.write("rpict -t 10 -vth -vp " + str(IMGBatFile()[1][g]) + " " + str(IMGBatFile()[2][g]) + " " + str(IMGBatFile()[3][g]) + " "
                    "-vd " + str(IMGBatFile()[4][g]) + " " + str(IMGBatFile()[5][g]) + " " + str(IMGBatFile()[6][g]) + " "
                    "-vu " + str(IMGBatFile()[7][g]) + " " + str(IMGBatFile()[8][g]) + " " + str(IMGBatFile()[9][g]) + " "
                    "-vh 180.000 -vv 180.000 -vs 0.000 -vl 0.000 -x 800 -y 800 -af ")
            h.write(Temp_Bat_Directory + "\\" + ambfile)
            h.write(radQual)
            h.write(Temp_Oct_Directory + "\\" + str("%04d" % HOY) + "_" + month + "_" + day + "_" + str('%.2f' % float(hour)) + ".oct")
            h.write(" > ")
            h.write(Temp_Bat_Directory + "\\" + unffile)
            h.write("\npfilt -1 -r .6 -x/2 -y/2 ")
            h.write(Temp_Bat_Directory + "\\" + unffile)
            h.write(" > ")
            h.write(Temp_HDR_Directory + "\\" + hdrfile)
            h.write("\n")
            h.write("\n")
            h.write("\ndel " + Temp_Bat_Directory + "\\" + unffile + "\n")
            h.write("\ndel " + Temp_Bat_Directory + "\\" + ambfile + "\n")
        elif CameraType_down() == "Panorama" :
            finalOct = str("%04d" % HOY) + "_" + month + "_" + day + "_" + hour + "_" + str(g) +  "_glare.bat"
            h = open(Temp_Bat_Directory + "\\" + finalOct, "w")
            h.write("SET RAYPATH=.;C:/Radiance/lib\n")
            h.write("PATH=C:/Radiance/bin/;$PATH\n\n")
            ambfile = str("%04d" % HOY) + "_" + month + "_" + day + "_" + str(hour) + "_" + str(g) + ".amb"
            unffile = str("%04d" % HOY) + "_" + month + "_" + day + "_" + str(hour) + "_" + str(g) + ".unf"
            hdrfile = str("%04d" % HOY) + "_" + month + "_" + day + "_" + str(hour) + "_" + str(g) + ".hdr"
            temp = str("%04d" % HOY) + "_" + month + "_" + day + "_" + str(hour) + "_" + str(g) + ".txt"
            h.write("set X=2048\n")
            h.write("set Y=2048\n")
            h.write('cnt %Y% %X% | rcalc -f view360stereo.cal -e "XD:%X%;YD:%Y%;X:')
            h.write(str(IMGBatFile()[1][g]))
            h.write(';Y:')
            h.write(str(IMGBatFile()[2][g]))
            h.write(';Z:')
            h.write(str(IMGBatFile()[1][g]))
            h.write(';IPD:0.06;EX:0;EZ:0" | rtrace ')
            h.write("-dp 1024 -ar 128 -ds 0.1 -dj 0.9 -dt 0.05 -dc 0.75 -dr 3 -ss 16 -st 0.01 -ab 4 -aa 0.15 -ad 1024 -as 512 -lr 12 -lw 1e-5")
            h.write(' -x %X% -y %Y% -fac ' + (Temp_Oct_Directory + "\\" + str("%04d" % HOY) + "_" + month + "_" + day + "_" + str('%.2f' % float(hour)) + ".oct") + '  > ')
            h.write(Temp_HDR_Directory + "\\" + hdrfile)
            h.write("\ndel " + Temp_Bat_Directory + "\\" + unffile + "\n")
            h.write("\ndel " + Temp_Bat_Directory + "\\" + ambfile + "\n")
    h.write("\ndel " + Temp_Oct_Directory.replace("/","\\") + "\\" + str("%04d" % HOY) + "_" + month + "_" + day + "_" + str('%.2f' % float(hour)) + ".oct")
    h.write("\nexit")
    h.close()


# define the list of all .bat files
def RadBats():  # create function to list all files within folder and subfolder names *Rad.bat
    BATS = []
    for path, subdirs, files in os.walk(directory + "\\BATs"):
        for name in files:
            if fnmatch(name, "*_glare.bat"):
                BATS.append(
                    os.path.join(path, name))  # join the path of the file with the file name to get the full file path
    return BATS


# execute the bat files in parallel mode, according to the core limit provided lower
def RunRadBats():
    Create_Sky_Files()
    Parallel_Basefile("bats", RadBats(), int(low_lim()))
    os.system((directory + "\\parallel_bats.bat"))


# button in the tkinger interface to execute the .bat files
RunRadsButton = tk.Button(main, text="Execute Radiance simulation", width=48, background=button_colour,
                          activebackground=general_bg_colour, activeforeground="black", font=("Helvetica", 9),
                          command=lambda: RunRadBats())
RunRadsButton.place(x=30, y=605)  # SavePercentages_button.grid(row=3,column = 0)


# Create mask if needed.
# define the list of all .HDR files
def HDRimages():  # create function to list all files within folder and subfolder names *Rad.bat
    HDRs = []
    for path, subdirs, files in os.walk(directory + "\\HDRs"):
        for name in files:
            if fnmatch(name, "*.HDR"):
                HDRs.append(
                    os.path.join(path, name))  # join the path of the file with the file name to get the full file path
    return HDRs


# label to separate for HDR section
tk.Label(main, text="Generate False Colour and Human HDRs", background=general_bg_colour, font=("Helvetica", 12)).place(
    x=47, y=690)


# create all the HDR bats for parallel processing
def Create_HDR_Bats():
    Directory = directory.replace("/", "\\")
    Temp_Directory = Directory + "\\temp_hdr"
    JPG_Directory = Directory + "\\jpgs"
    if not os.path.exists(Temp_Directory):
        os.makedirs(Temp_Directory)
    if not os.path.exists(JPG_Directory):
        os.makedirs(JPG_Directory)
    for i in (glob.glob(directory + "\\HDRs\\*.hdr")):
        HDR_bat = i.replace(".hdr", "_HDR.bat").replace(directory, Temp_Directory).replace("\\HDRs","").replace("/", "\\")
        FC = i.replace(".hdr", "_f.hdr").replace(directory, Temp_Directory).replace("\\HDRs","").replace("/", "\\")
        FC_jpg = i.replace("\\HDRs\\", "\\").replace("_.hdr", "_fc.jpg").replace(directory, JPG_Directory).replace("/", "\\")
        Human = i.replace(".hdr", "_h.hdr").replace(directory, Temp_Directory).replace("\\HDRs","").replace("/", "\\")
        Human_JPG = i.replace("\\HDRs\\", "\\").replace("_.hdr", "_h.jpg").replace(directory, JPG_Directory).replace("/", "\\")
        g = open(HDR_bat, "w")
        g.write("SET RAYPATH=.;C:\\Radiance\\lib\n")
        g.write("PATH=c:\\radiance\\bin\\;'c:\\Program Files\\ImageMagick-7.0.3-Q16\\';\n")
        g.write("ra_tiff " + i + " " + Human.replace("_h.hdr", ".tif"))
        g.write(" & falsecolor2 -i " + i + " -s 5000.0 -n 10 -mask 0.1 -l cd/m2 -m 179 -spec -z > " + FC)
        g.write(" & pcond -h+ " + i + " " + Human)
        g.write(" & ra_tiff " + Human + " " + Human.replace(".hdr", ".tif"))
        g.write(" & ra_tiff " + FC + " " + FC.replace(".hdr", ".tif"))
        g.write(" & convert " + FC.replace(".hdr", ".tif") + " -gravity West -chop 100x0 " + FC.replace("_f.hdr", "_fc.tif"))
        g.write(" & convert " + FC.replace("_f.hdr", "_fc.tif") + " " + FC_jpg)
        g.write(" & convert " + Human.replace(".hdr", ".tif") + " " + Human_JPG)
        #g.write("\ndel " + FC.replace("_f.hdr", "_fc.tif"))
        #g.write("\ndel " + Human.replace(".hdr", ".tif"))
        #g.write("\ndel " + FC.replace("_f.hdr", "_f.tif"))
        g.write("\nexit")
        g.close()


# define the list of all .bat files
def HDR_Bats():  # create function to list all files within folder and subfolder names *Rad.bat
    # Create_HDR_Bats()
    BATS = []
    for path, subdirs, files in os.walk(directory + "\\temp_hdr"):
        for name in files:
            if fnmatch(name, "*_HDR.bat"):
                BATS.append(
                    os.path.join(path, name))  # join the path of the file with the file name to get the full file path
    return BATS


# execute the bat files in parallel mode, according to the core limit provided lower
def HDR_all():
    Create_HDR_Bats()
    Parallel_Basefile("HDR", HDR_Bats(), int(low_lim()))
    os.system((directory + "\\parallel_HDR.bat"))


# button for HDRs
Run_All_Button = tk.Button(main, text="FC and Human", width=48, background=button_colour,
                           activebackground=general_bg_colour, activeforeground="black", font=("Helvetica", 9),
                           command=lambda: HDR_all())
Run_All_Button.place(x=30, y=720)  # SavePercentages_button.grid(row=3,column = 0)


# use imagemagick to convert tiffs into jpgs
def Convert_Jpg():
    Directory = directory.replace("/", "\\")
    os.system("copy " + Directory + "\\temp_hdr\\*_f.tif " + Directory + "\\temp_hdr\\*_fc.tif\n")
    os.system("mogrify -gravity West -chop 100x0 " + Directory + "\\temp_hdr\\*_fc.tif\n")
    os.system("del " + Directory + "\\temp_hdr\\*_f.tif\n")
    os.system("mogrify -format jpg " + Directory + "\\temp_hdr\\*.tif\n")
    for g in range(IMGBatFile()[0]):
        if not os.path.exists(Directory + "\\jpgs\\" + str(g) + "\\Base\\"):
            os.makedirs(Directory + "\\jpgs\\" + str(g) + "\\Base\\")
        if not os.path.exists(Directory + "\\jpgs\\" + str(g) + "\\Human\\"):
            os.makedirs(Directory + "\\jpgs\\" + str(g) + "\\Human\\")
        if not os.path.exists(Directory + "\\jpgs\\" + str(g) + "\\FC\\"):
            os.makedirs(Directory + "\\jpgs\\" + str(g) + "\\FC\\")
        os.system("copy " + Directory + "\\temp_hdr\\*" + str(g) + ".jpg " + Directory + "\\jpgs\\" + str(g) + "\\Base\\*" + str(g) + ".jpg")
        os.system("copy " + Directory + "\\temp_hdr\\*" + str(g) + "_h.jpg " + Directory + "\\jpgs\\" + str(g) + "\\Human\\*" + str(g) + "_h.jpg")
        os.system("copy " + Directory + "\\temp_hdr\\*" + str(g) + "_fc.jpg " + Directory + "\\jpgs\\" + str(g) + "\\FC\\*" + str(g) + "_fc.jpg")
    os.system("del " + Directory + "\\temp_hdr\\*.jpg ")


# button for jpgs
Run_ConvertJpg_Button = tk.Button(main, text="Convert Tiffs to JPGs", width=48, background=button_colour,
                                  activebackground=general_bg_colour, activeforeground="black", font=("Helvetica", 9),
                                  command=lambda: Convert_Jpg())
Run_ConvertJpg_Button.place(x=30, y=760)  # SavePercentages_button.grid(row=3,column = 0)


# add option to delete all temp HDRs
def Clean_HDR():
    Directory = directory.replace("/", "\\")
    os.system("rmdir /S /Q " + Directory + "\\temp_hdr\ny\n")
    os.system("rmdir /S /Q " + Directory + "\\OCTs\ny\n")
    os.system("rmdir /S /Q " + Directory + "\\BATs\ny\n")
    os.system("rmdir /S /Q " + Directory + "\\SKYs\ny\n")


tk.Label(main, text="Clean Temp folders and files", background=general_bg_colour, font=("Helvetica", 12)).place(x=47,
                                                                                                                y=790)

# button for cleaning up temp folders
Run_Temp_Clean_Button = tk.Button(main, text="Clean temp files", width=48, background="white",
                                  activebackground=general_bg_colour, activeforeground="black", font=("Helvetica", 9),
                                  command=lambda: Clean_HDR())
Run_Temp_Clean_Button.place(x=30, y=815)  # SavePercentages_button.grid(row=3,column = 0)


main.mainloop()
