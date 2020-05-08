# The Sorting Chime v2
# by John Lee

# Description: This program takes input through a crude GUI and produces all
# possible schedules based on how many/what kinds of concerts each chimesmaster
# needs and the preferences that each has indicated. Will catch all user input 
# errors that would otherwise cause the program to malfunction.

# ------------------------------------------------------------------------------

from Tkinter import *
import tkMessageBox
from collections import OrderedDict

# ------------------------------------------------------------------------------
# root window

# instructions window
def instructions():
    tkMessageBox.showinfo('Instructions', '1. Enter the number of chimesmasters.' +\
                                          '\n' +\
                                          '\n2. Input each chimesmaster\'s initials and numbers of' +\
                                          '\nmorning, afternoon, and evening concerts to be assigned.' +\
                                          '\nInitials must have less than eight characters.' +\
                                          '\n' +\
                                          '\n3. Indicate each chimesmaster\'s preferences.' +\
                                          '\n' +\
                                          '\n4. Output schedules with or without specific preferences.' +\
                                          '\nThe window will remain open, so different combinations of' +\
                                          '\nspecific preferences may be tried.')

# about window
def about():
    tkMessageBox.showinfo('About', 'The Sorting Chime (c) 2016 John G. Lee \'18')

# window setup
top = Tk()
top.wm_title('The Sorting Chime') # top.geometry('500x600')
menubar = Menu(top)
optionmenu = Menu(menubar, tearoff = 0)
optionmenu.add_command(label = 'Instructions', command = instructions)
optionmenu.add_command(label = 'About', command = about)
menubar.add_cascade(label = 'Options', menu = optionmenu)
top.config(menu = menubar)

# ------------------------------------------------------------------------------
# global variables, sorted by function use

# start()
step1 = [] # stepX global variable contains all widget objects of window X

# inputCMs()
step2 = []
rawInput = OrderedDict()

# inputPrefs()
uniqueCM = []
chimesmasters = {'M': [], 'A': [], 'E': []}
days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
step3 = []

# inputPrefs(), relay()
concerts = ['Sunday morning', 'Monday morning', 'Tuesday morning', 
            'Wednesday morning', 'Thursday morning', 'Friday morning', 
            'Saturday morning', 'Sunday afternoon', 'Monday afternoon',
            'Tuesday afternoon', 'Wednesday afternoon', 'Thursday afternoon',
            'Friday afternoon', 'Saturday afternoon', 'Sunday evening',
            'Monday evening', 'Tuesday evening', 'Wednesday evening',
            'Thursday evening', 'Friday evening', 'Saturday evening']
rawPrefs = OrderedDict()
for concert in concerts:
    rawPrefs[concert] = []

# relay()
prefs = OrderedDict()

# assign()
daytime = {'Sunday': 0, 'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 
           'Thursday': 4, 'Friday': 5, 'Saturday': 6, 'morning': 0,
           'afternoon': 1, 'evening': 2,}
prefinal = [['', '', '', '', '', '', ''], 
            ['', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '']]
final = []

# printResults()
step4 = []
rawSpec = OrderedDict()

# printPrefResults()
abbDT = {'Sun.': 0, 'Mon.': 1, 'Tue.': 2, 'Wed.': 3, 
         'Thu.': 4, 'Fri.': 5, 'Sat.': 6, 'M': 0,
         'A': 1, 'E': 2,}

# ------------------------------------------------------------------------------
# input/output functions

# Displays instructions and asks for the number of chimesmasters.
def start():
    numberLabel = Label(top, text = "Number of chimesmasters:")
    numberLabel.grid(row = 0, column = 0, sticky = W)
    number = Entry(top, width = 5)
    number.grid(row = 0, column = 1)
    step1.append(numberLabel)
    step1.append(number)
    number.bind('<Return>', inputCMs)
    instructions()

# Based on the number of chimesmasters, asks for info on each chimesmaster
# (initials and number of morning, afternoon, and evening concerts).
def inputCMs(event):
    # make sure input is int > 0
    try:
        num = int(event.widget.get())
        if num <= 0:
            raise Exception()
    except:
        tkMessageBox.showinfo('Error', 'Entry must be an integer greater than 0.')
        raise Exception()
    # remove step1
    step1[0].destroy()
    step1[1].destroy()
    # create labels for CM/prefs input
    c1 = Label(top, text = 'CM')
    c2 = Label(top, text = 'M')
    c3 = Label(top, text = 'A')
    c4 = Label(top, text = 'E')
    c1.grid(row = 0, column = 1)
    c2.grid(row = 0, column = 2)
    c3.grid(row = 0, column = 3)
    c4.grid(row = 0, column = 4)
    step2.append(c1)
    step2.append(c2)
    step2.append(c3)
    step2.append(c4)
    # input CMs and time of day requirements
    for i in range(num):
        # chimesmaster
        inputCMLabel = Label(top, text = str(i + 1))
        inputCMLabel.grid(row = i + 1, column = 0)#, sticky = W)
        step2.append(inputCMLabel)
        inputCM = Entry(top, width = 10)
        inputCM.grid(row = i + 1, column = 1)
        step2.append(inputCM)
        rawInput[inputCM] = []
        # morning
        inputM = Entry(top, width = 5)
        inputM.grid(row = i + 1, column = 2)
        step2.append(inputM)
        rawInput[inputCM].append(inputM)
        # afternoon
        inputA = Entry(top, width = 5)
        inputA.grid(row = i + 1, column = 3)
        step2.append(inputA)
        rawInput[inputCM].append(inputA)
        # evening
        inputE = Entry(top, width = 5)
        inputE.grid(row = i + 1, column = 4)
        step2.append(inputE)
        rawInput[inputCM].append(inputE)
    # input button
    enterAll = Button(top, text = 'Input', command = inputPrefs)
    enterAll.grid(columnspan = 5)
    step2.append(enterAll)

# Based on the chimesmaster info given in inputCMs(), produces checkboxes to
# take each chimesmaster's preferences for each day/time. 
def inputPrefs():
    # make sure there are 7 total assignments for each of M, A, and E
    try:
        del uniqueCM[:]
        MAE = {'M': 0, 'A': 0, 'E': 0}
        for CM in rawInput:
            MAE['M'] += int(rawInput[CM][0].get())
            MAE['A'] += int(rawInput[CM][1].get())
            MAE['E'] += int(rawInput[CM][2].get())
            uniqueCM.append(CM.get().upper())
        if (MAE['M'] == 7) & (MAE['A'] == 7) & (MAE['E'] == 7):
            for CM in rawInput:
                times = ['M', 'A', 'E']
                i = 0
                for time in rawInput[CM]:
                    for conc in range(int(time.get())):
                        chimesmasters[times[i]].append(CM.get().upper())
                    i += 1
                CM.destroy()
            for widg in step2:
                widg.destroy()
        else:
            raise Exception()
    except:
        tkMessageBox.showinfo('Error', 'There must be 7 total assignments for each of M, A, and E.')
        raise Exception()
    # input prefs for each day/time
    rows = 0
    for time in ['Morning', 'Afternoon', 'Evening']:
        timeLabel = Label(top, text = time + ':')
        timeLabel.grid(row = rows, column = 0, sticky = W)
        step3.append(timeLabel)
        addRows = 0
        currCol = 1
        for day in days:
            currRows = rows
            dayLabel = Label(top, text = day[0:3] + '.')
            dayLabel.grid(row = currRows, column = currCol, sticky = W)
            step3.append(dayLabel)
            # make checkboxes for each CM
            unique = []
            for CM in chimesmasters[time[0]]:
                if CM not in unique:
                    currRows += 1
                    checkVar = IntVar()
                    check = Checkbutton(top, text = CM, variable = checkVar, onvalue = 1, offvalue = 0)
                    check.var = checkVar
                    check.grid(row = currRows, column = currCol, sticky = W)
                    step3.append(check)
                    rawPrefs[day + ' ' + time.lower()].append(check)
                    unique.append(CM)
            currCol += 1
            addRows = currRows
        rows = addRows + 1
    # input button
    inputAll = Button(top, text = 'Input', command = relay)
    inputAll.grid(columnspan = 8)
    step3.append(inputAll)

# Function between inputPrefs() and assign(), because assign() is recursive and
# having it handle raising an exception would be messy. Calls printResults()
# if assign() was successful.
def relay():
	# prepare global variable, prefs
    for concert in concerts:
        prefs[concert] = []
    # process rawPrefs to prefs
    for conc in rawPrefs:
        for box in rawPrefs[conc]:
            if box.var.get() == 1:
                prefs[conc].append(box.cget('text'))
    assign(prefs, prefinal, chimesmasters)
    if len(final) == 0:
        tkMessageBox.showinfo('Error', 'There are no schedules accomodating the given preferences.')
        raise Exception()
    else:
        # remove step3 and call printResults()
        for widg in step3:
            widg.destroy()
        printResults()

# Recursive depth-first function that finds every possible schedule given each
# chimesmaster's info and prefs that have been input. Appends each possible
# schedule to global variable, final.
def assign(tempPrefs, tempFinal, tempCMs):
    # copy tempPrefs
    prefsCopy = OrderedDict()
    for day in tempPrefs:
        if day != tempPrefs.keys()[0]:
            prefsCopy[day] = []
    for i in tempPrefs:
        if i != tempPrefs.keys()[0]:
            for i2 in tempPrefs[i]:
                prefsCopy[i].append(i2)
    today = tempPrefs.keys()[0]
    for j in tempPrefs[today]:
        # copy tempFinal
        draft = [['', '', '', '', '', '', ''], 
                 ['', '', '', '', '', '', ''],
                 ['', '', '', '', '', '', '']]
        for k in range(0,3):
            for l in range(0,7):
                draft[k][l] = tempFinal[k][l]
        # copy tempCMs
        MAE = {'M': [], 'A': [], 'E': []}
        for m in tempCMs:
            for m2 in tempCMs[m]:
                MAE[m].append(m2)
        # assign
        day = daytime[today[:today.find(' ')]]
        time = daytime[today[today.find(' ') + 1:]] 
        draft[time][day] = j
        try:
            MAE[today[today.find(' ') + 1:][0].upper()].remove(j)
            if (MAE['M'] == []) and (MAE['A'] == []) and (MAE['E'] == []):
                if draft not in final:
                    final.append(draft)
            else:
                assign(prefsCopy, draft, MAE)
        except:
            pass

# The last window, which displays the total number of possible schedules. There
# are options for indicating specific preferences, which will filter the output.
# This window remains open, so different combinations of specific preferences
# may be used to output. Calls printPrefResults() to print the output.
def printResults():
	# setup format of the  window
    for concert in concerts:
        rawSpec[concert] = []
    rows = 2
    for time in ['Morning', 'Afternoon', 'Evening']:
        timeLabel = Label(top, text = time + ':')
        timeLabel.grid(row = rows, column = 0, sticky = W)
        step4.append(timeLabel)
        most = 0 
        currCol = 1
        for day in days:
            currRows = rows
            dayLabel = Label(top, text = day[0:3] + '.')
            dayLabel.grid(row = currRows, column = currCol, sticky = W)
            step4.append(dayLabel)
            # make checkboxes for each CM pref
            unique = []
            today = prefs[day + ' ' + time.lower()]
            for CM in today:
                if CM not in unique:
                    currRows += 1
                    checkVar = IntVar()
                    check = Checkbutton(top, text = CM, variable = checkVar, onvalue = 1, offvalue = 0)
                    check.var = checkVar
                    check.grid(row = currRows, column = currCol, sticky = W)
                    step4.append(check)
                    rawSpec[day + ' ' + time.lower()].append(check)
                    unique.append(CM)
            currCol += 1
            if currRows > most:
                most = currRows
        rows = most + 1
    # top 2 rows of text and the output button
    total = Label(top, text = 'Total number of possible schedules: ' + str(len(final)))
    total.grid(row = 0, columnspan = 8, sticky = W)
    step4.append(total)
    accom = Label(top, text = 'Accommodate specific preferences (optional):')
    accom.grid(row = 1, columnspan = 8, sticky = W)
    step4.append(accom)
    dispAccom = Button(top, text = 'Output', command = printPrefResults)
    dispAccom.grid(columnspan = 8)
    step4.append(dispAccom)

# Takes specific preferences given in the final window, if any, and prints 
# possible schedules. Will print all possible schedules if no specific
# preferences are given.
def printPrefResults():
    # process specific preferences
    uniquePos = []
    specPrefs = OrderedDict()
    for concert in rawSpec:
        for CM in rawSpec[concert]:
            if CM.var.get() == 1:
                conc = concert.split()
                pos = [daytime[conc[1]], daytime[conc[0]]]
                if pos not in uniquePos:
                    uniquePos.append(pos)
                    specPrefs[daytime[conc[1]], daytime[conc[0]]] = CM.cget('text')
                else:
                    tkMessageBox.showinfo('Error', 'For each concert, only one chimesmaster may indicate a specific preference.')
                    raise Exception()
    # check if there are schedules that accomodate the given specific preferences
    subFinal = []
    for perm in final:
        count = 0
        for pos in specPrefs:
            if perm[pos[0]][pos[1]] == specPrefs[pos]:
                count += 1
        if count == len(specPrefs):
            subFinal.append(perm)
    if len(subFinal) == 0:
        tkMessageBox.showinfo('Error', 'There are no schedules accomodating the indicated specific preferences.')
        raise Exception()
    # print output
    print 'Output:' 
    print
    for perm in range(len(subFinal)):
        mae = ['M', 'A', 'E']
        count = 0
        print '[' + str(perm + 1) + ']'
        print '--------------------------------------------------------------'
        print '      Sun.    Mon.    Tue.    Wed.    Thu.    Fri.    Sat.    '
        print '--------------------------------------------------------------'
        for row in subFinal[perm]:
            copy = []
            for cm in range(0,7):
                copy.append(row[cm])
                copy[cm] += (' ' * (8 - len(copy[cm])))
            print mae[count] + ':    ' + ''.join(copy)
            count +=  1
        print '--------------------------------------------------------------'
        print

# ------------------------------------------------------------------------------
# run everything

start()
top.mainloop()
