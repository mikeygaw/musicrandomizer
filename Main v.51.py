# Music Randomizer

# imports

import random
import sqlite3

conn = sqlite3.connect('music.db')
conn.row_factory = lambda cursor, row: row[0]
cursor = conn.cursor()
global selection

def transferband():


    def moveband():

        # Starts by getting the band the user wishes to move as well as the favorite level the band is being moved to.
        # Current favorite level is pulled from the database.
        # Database is then checked to see if the band is there and spelled correctly.
        # Afterwords the band is removed from the old favorite level and the weighting for that section is updated.
        # Finally the band is added to the new favorite level and the weighting for that section is updated.

        bandname = input('Enter the name of the band you wish to move. ')
        bandname = bandname.title()
        newfavlevel = input('Enter the Favorite Level the band is being move to. ')
        newfavlevel = newfavlevel.title()

        favlevels = cursor.execute('SELECT FavLevel FROM FavLevelWeight').fetchall()
        if newfavlevel not in favlevels:
            print('That is not an existing favorite level.')
            return tbmenu()

        currentfavlevel = cursor.execute('SELECT FavLevel FROM Bandlist WHERE Band = ?', (bandname, )).fetchall()
        print(currentfavlevel)
        currentfavlevel = currentfavlevel[0]
        print(currentfavlevel)

        oldbands = cursor.execute('SELECT Band FROM Bandlist WHERE FavLevel = ?', (currentfavlevel, )).fetchall()
        print(oldbands)
        print(len(oldbands))
        if bandname not in oldbands:
            print('That band is not on the list!')
            return tbmenu()
        oldbands.remove(bandname)

        cursor.execute('DELETE FROM Bandlist WHERE Band = ?', (bandname, ))
        numofbands = len(oldbands)
        currentfavweight = cursor.execute('SELECT Weight FROM FavLevelWeight WHERE FavLevel = ?', (currentfavlevel, )).fetchall()
        currentfavweight = currentfavweight[0]
        newweight = currentfavweight / numofbands

        cursor.execute('UPDATE Bandlist SET Weight = ? WHERE Favlevel = ?', (newweight, currentfavlevel, ))

        cursor.execute('INSERT INTO Bandlist (Band, FavLevel) VALUES (?,?)', (bandname, newfavlevel, ))
        newbands = cursor.execute('SELECT Band FROM Bandlist WHERE FavLevel = ?', (newfavlevel, )).fetchall()
        numofbands = len(newbands)
        newfavweight = cursor.execute('SELECT Weight FROM FavLevelWeight WHERE FavLevel = ?', (newfavlevel, )).fetchall()
        newfavweight = newfavweight[0]
        newweight = newfavweight / numofbands
        cursor.execute('UPDATE Bandlist SET Weight = ? WHERE Favlevel = ?', (newweight, newfavlevel, ))

        conn.commit()
        return tbmenu()


    def tbdisplay():

        # Gets Favorite level from the user, imports the bands assigned to that level from the database and then prints
        # the bands.

        favlevels = cursor.execute('SELECT FavLevel FROM FavLevelWeight').fetchall()
        print(favlevels)

        favlevelselection = input('Show which favorite level? ')
        favlevelselection = favlevelselection.title()
        bands = cursor.execute('SELECT Band FROM BandList WHERE FavLevel = ?', (favlevelselection, )).fetchall()
        for i in range(len(bands)):
            print(bands[i])

        return tbmenu()


    def tbselector():

        # Evaluates user input from menu function and runs the appropriate function.
        # The submenu function is rerun if the entry is not found.

        if tbselection == 'Print Favorites':
            tbdisplay()
        elif tbselection == 'Transfer Band':
            moveband()
        elif tbselection == 'Return To Main Menu':
            return menu()
        else:
            print('That was not a valid entry!')
            return tbmenu()


    def tbmenu():

        # Submenu for transferring bands between favorite levels.

        trbmenu = ['Print Favorites', 'Transfer Band', 'Return To Main Menu']
        print(trbmenu)
        global tbselection
        tbselection = input('Make a selection. ')
        tbselection = tbselection.title()

        tbselector()

    tbmenu()


def addband():

    # Asks the user for a band name and favorite level. After recalculating the weight for tha favorite level,
    # the band is added and the new weight is set in the database.

    fl = input('Enter the favorite level you are adding a band too. ')
    fl = fl.title()
    bandname = input('Enter the name of the band you are adding. ')
    bandname = bandname.title()

    bands = cursor.execute('SELECT Band FROM Bandlist WHERE FavLevel = ?', (fl, )).fetchall()
    bands.append(bandname)

    flw = cursor.execute('SELECT Weight FROM FavLevelWeight WHERE FavLevel = ?', (fl, )).fetchall()
    flw = flw[0]
    numbands = len(bands)
    weight = flw/numbands
    band = (bandname,fl,weight)
    cursor.execute('INSERT INTO Bandlist (Band, FavLevel, Weight) VALUES (?, ?, ?)', band)
    print('Band successfully added.')
    return menu()


def addalbum():

    # Gets a single album (and band name) rom the user and adds it's to the database.

    bandname = input('Enter the name of the band you are adding an album too? ')
    bandname = bandname.title()
    albumname = input('Enter the name of the album to add. ')
    albumname = albumname.title()

    cursor.execute('INSERT INTO Albums (AlbumName, Band) VALUES (?,?)', (albumname, bandname, ))
    conn.commit()

    return addalbummenu()


def albumsbulkimport():

    # Bulk imports albums to the database.

    bandname = input('Enter the name of the band your are importing albums from. ')
    bandname = bandname.title()
    albums = [i.strip() for i in open('Albums.txt').readlines()]

    for i in range(len(albums)):
        album = (albums[i],bandname)
        cursor.execute('INSERT INTO Albums (AlbumName,Band) VALUES (?,?)', (albums[i], bandname, ))

    conn.commit()
    print('Import successful.')
    return addalbummenu()


def returnmainmenu():
    return menu()


def aaselector():

    # If statement to evaluate user input from the Add Album menu

    if aaselection == 'Add An Album':
        addalbum()
    elif aaselection == 'Bulk Import':
        albumsbulkimport()
    elif aaselection == 'Return To Main Menu':
        menu()
    else:
        print('That was not a valid selection. ')
        return menu()


def addalbummenu():

    # Menu for adding an album

    aamenu = ['1. Add An Album', '2. Bulk Import', '3. Return to Main Menu']

    #print(aamenu)
    #global aaselection
    #aaselection = input('Choose an option. ')
    #aaselection = aaselection.title()
    #aaselector

    for i in range(len(aamenu)):
        print(aamenu[i])

    try:
        aaselection = int(input('Choose an option by entering the appropriate number. \n'))
    except ValueError:
        print('That is not a valid entry!')
        return addalbummenu()

    aaselectdict = {
        1: addalbum,
        2: albumsbulkimport,
        3: returnmainmenu
    }

    try:
        aaselectdict[aaselection]()
    except KeyError:
        print('That is not a valid entry!')
        return aamenu()

def randomizer():

    # Randomizer
    # This function starts by importing the bands and weights from the database

    bands = cursor.execute('SELECT Band FROM Bandlist').fetchall()
    weightimport = (cursor.execute('SELECT Weight FROM Bandlist').fetchall())
    for i in range(len(weightimport)):
        weightimport[i] = float(weightimport[i])

    try:
        numtochoose = int(input('Enter the number of albums to pick. '))
    except ValueError:
        print('That is not a number!')
        return menu()

    #bandselection = []
    #bandselection = random.choices(bands, weightimport, k=numtochoose)

    results = []

    #for i in range(len(bandselection)):
    #    band = bandselection[i]
    #    albums = cursor.execute('SELECT AlbumName FROM Albums WHERE Band = ?', (band, )).fetchall()
    #    lengthalbums = len(albums)
    #    lengthalbums = lengthalbums - 1
    #    albumselection = random.randint(0, lengthalbums)
    #    album = albums[albumselection]
    #   results.append(band + ' - ' + album)
    #    results.sort()

    for i in range(numtochoose):
        band = random.choices(bands, weightimport)
        band = band[0]
        print(band)
        albums = cursor.execute('SELECT AlbumName FROM Albums WHERE Band = ?', (band,)).fetchall()
        lengthalbums = len(albums)
        lengthalbums = lengthalbums - 1
        albumselection = random.randint(0, lengthalbums)
        album = albums[albumselection]
        result = band + ' - ' + album
        if result not in results:
            results.append(result)
        else:
            i = i - 1

    results.sort()
    for i in range(len(results)):
        print(results[i])

    return menu()


def removeband():

    # Remove band from the database.
    # This function get the band name from the user then gets the favorite level and weight from the database.
    # After the band is deleted from the database, the weighting is recalculated and saved to the database associated
    # with the appropriate bands. Afterwords, the menu function is run again to continue the program.

    bands = cursor.execute('SELECT Band FROM Bandlist').fetchall()
    for i in range(len(bands)):
        band = bands[i]
        print(band)

    bandname = input('Enter the name of the band to remove. ')
    bandname = bandname.title()

    if bandname not in bands:
        print('That band is not in the list!')
        return menu()

    favlevelweight = cursor.execute('SELECT Weight FROM FavLevelWeight WHERE FavLevel = ?', (favlevel, )).fetchall()
    favlevelweight = favlevelweight[0]

    cursor.execute('DELETE FROM Bandlist WHERE Band = ?', (bandname, ))
    bands = cursor.execute('SELECT Band FROM BandList WHERE FavLevel = ?', (favlevel, )).fetchall()
    bandslength = len(bands)
    updatedweight = favlevelweight/bandslength

    cursor.execute('UPDATE Bandlist SET Weight = ? WHERE FavLevel = ?', (updatedweight, favlevel, ))

    cursor.execute('DELETE FROM Albums WHERE Band = ?', (bandname, ))
    conn.commit()
    print('Band removed successfully.')

    return menu()


def removealbum():

    # Removes album from database.

    albumname = input('Enter the name of the album to remove. ')
    albums = cursor.execute('SELECT AlbumName FROM ALBUMS').fetchall

    if albumname not in albums:
        print("That album is not on the list!")
        return menu()

    cursor.execute('DELETE FROM Albums WHERE AlbumName = ?', (albumsname, ))
    conn.commit()
    return menu()


def end():

    # Exits the program

    cursor.close()
    exit


#def selector(selection):

    # If statements evaluating the selection the user input at the menu prompt.
    # If the input is invalid, the menu function is run again.

    #selectdict = {'1': addband(), '2': addalbummenu(), '3': randomizer(), '4': removeband(), '5': transferband(), '6': quit()}

    #func = selectdict(selection)
    #func()

    #global selection
    #if selection == 'Add Band':
        #addband()
    #elif selection == 'Add Album':
        #addalbummenu()
    #elif selection == 'Pick Album':
        #randomizer()
    #elif selection == 'Remove Band':
        #removeband()2
    #elif selection == 'Transfer Band':
        #transferband()
    #elif selection == 'Quit':
        #end()
    #else:
        #print('That is not a valid selection.')
        #return menu()


def menu():

    # Main menu. The user is prompted to choose an option. The user's input is then evaluated and the appropriate
    # function is run

    menu = ['1. Add Band', '2. Add Album', '3. Pick Album', '4. Remove Band', '5. Transfer Band', '6. Quit']
    for i in range(len(menu)):
        print(menu[i])

    try:
        selection = int(input('Make a selection by entering the appropriate number. '))
    except ValueError:
        print('That is not a valid entry!')
        return menu()

    selectdict = {
        1: addband,
        2: addalbummenu,
        3: randomizer,
        4: removeband,
        5: transferband,
        6: quit
    }

    if (selection > 0) and (selection < 7):
        selectdict[selection]()
    else:
        print('That is not a valid entry!')
        return menu()


menu()
