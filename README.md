# Mail.Rip v1
<p>
  <i>A SMTP Checker / SMTP Cracker with SOCKS support and e-mail delivery test (inbox check) for mailpass combolists.</i>
</p>
<p>
  <b>Mail.Rip v2 has already been released: <a href="https://github.com/DrPython3/MailRipV2">click here!</a> It is faster, more reliable and still easy to use!</b>
</p>

<h2>Legal Notices</h2>
<p>
  <b><u>The code published here is for educational purposes only!</u></b><br>
  You are not allowed to use it for any kind of illegal activity nor law enforcement at any time.
</p>

<h2>Overview</h2>
<p>
  <i>Mail.Rip v1 is a SMTP checker / SMTP cracker written in Python 3.8 for mailpass combolists.<br>
  It looks up the SMTP host for every combo and tries to verify the login data. For valid SMTP logins,<br>
  Mail.Rip will also try to send an e-mail to your address containing all the credentials. That way, it<br>
  performs an inbox test as well. It is fast and easy to use!</i>
</p>

<h3>Requirements</h3>
<p>
  <i>For runninng Mail.Rip v1 you need <b>Python 3.8+</b> to be installed on your system.<br>
  It has been tested on:</i>
</p>
<p>
  <ul>
    <li>Windows 10,</li>
    <li>KALI Linux and</li>
    <li>macOS Catalina.</li>
  </ul>
</p>
<p><b>Used packages are:</b></p>
<p>
  <ul>
    <li>ctypes,</li>
    <li>os,</li>
    <li>smtplib,</li>
    <li>socket,</li>
    <li>sys,</li>
    <li>ssl,</li>
    <li>threading,</li>
    <li>time,</li>
    <li>colorama,</li>
    <li>json,</li>
    <li>re,</li>
    <li>email.message,</li>
    <li>uuid,</li>
    <li>socks,</li>
    <li>random,</li>
    <li>urllib3 and</li>
    <li>certifi.</li>
  </ul>
</p>
<p>
  Moreover, <i>PyInstaller</i> can be used for creating a *.EXE.<br>
  Tested on Windows 10. Nevertheless, in case you experience any problems,<br>
  you can try "Auto PY to EXE" as well.
</p>

<h3>Features</h3>
<p>
  <ul>
    <li>Tests mailpass combolists for working SMTP logins,</li>
    <li>hostdata for common SMTP providers is included and can be edited,</li>
    <li>checks for most common SMTP (sub)domains if no host is found in included lists,</li>
    <li>tries to verify working SMTP logins by sending an e-mail to the user's address,</li>
    <li>supports multi-threading,</li>
    <li>stats are shown in window title,</li>
    <li>option to skip e-mail providers like Google, hotmail.com etc.,</li>
    <li>e-mail provider blacklist can be edited, too,</li>
    <li>results are saved to textfiles for further investigation and</li>
    <li>SOCKS4- and SOCKS5-support with auto-scraping using Proxyscrape.com.</li>
  </ul>
</p>
<p>
  <i>Note: Mail.Rip is now available as "proxyless" version (finished, released in v1.00) and "proxy" version!<br>
    <strong>The proxy-version can be used without proxys, too.</strong></i>
</p>

<h3>How to use ...</h3>
<p>
  <i>Just download / clone the files, install packages if needed and copy any mailpass combolist<br>
    to the same directory and load the script:</i>
</p>
<p>
  <b>1. Install packages:</b>
</p>

```
pip3 install certifi [...]
```

<p>
  <b>2. Start Mail.Rip v1:</b>
</p>

```
python3 mailripV1_proxy.py
```

<p>
  <i>... just follow the text on your screen. Of course, you may rename the file for easier usage.<br>
  Moreover, you can modify the config.json for your needs. Just add or delete entries to / from the lists<br>
  or dictionaries.</i>
</p>

<h4>WARNING "Proxy Usage":</h4>

<p>
  Please be aware of using free SOCKS-proxies may have a great impact on your results.<br>
  Mail.Rip v1 scrapes free proxies which may have already been used by others or may be<br>
  blacklisted. Therefor, your results may contain more false negatives and you may<br>
  receive even more errors from the mailsending feature.<br>
  <br>
  Used proxyless, Mail.Rip v1 works much faster and more reliable!
</p>

<h3>Support Mail.Rip v1</h3>
<p>
  <i>If you want to support this project, consider a donation!<br>
    Every donation is appreciated and helps with motivation for working on this tools.</i>
</p>
<p>
  <b>Donation Wallet (BTC):</b>   1M8PrpZ3VFHuGrnYJk63MtoEmoJxwiUxYf
</p>

<h3>Changelog</h3>
<p>
  <i>2020-10-18: releasing code version 0.3, creating repo, writing readme etc.</i><br>
  <i>2020-11-13: releasing code version 0.5, many improvements (see comment on commit of *.py-file).</i><br>
  <i>2020-11-15: releasing code version 0.9, big update (see comment on commit of *.py-file).</i><br>
  <i>2020-11-20: releasing code version 0.92, see commit comment for further information.</i><br>
  <i><b>2020-11-21: releasing code version 1.00 - now available for "proxyless" and "proxy" version!</b></i><br>
  <i>2020-11-27: releasing code version 1.07 for proxy-version, now supporting SOCKS4 and SOCKS5 proxies.</i><br>
  <i>2020-11-28: releasing code version 1.08 for proxy-version with minor tweaks and little improvements.</i><br>
  <i>2020-12-12: releasing code version 1.10 for proxy-version: see commit changes for details!</i><br>
  <i>2020-12-18: releasing code version 1.11 for proxy-version: see commit changes for details!</i>
</p>
