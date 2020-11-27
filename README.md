# Mail.Rip v1
<p>
  <i>A SMTP checker / SMTP cracker including a mailsending check for testing mailpass combolists.</i>
</p>

<h2>Legal Notices</h2>
<p>
  <b><u>The code published here is for educational purposes only!</u></b><br>
  You are not allowed to use it for any kind of illegal activity nor law enforcement at any time.
</p>

<h2>Overview</h2>
<p>
  <i>Mail.Rip v1 is written in Python 3.8 and still being improved though it is already functional,<br>
    delivering results very fast. The goal of this project is to offer a tool which is easy to use,<br>
    providing stable results over time.<br><br>
    There is still work to be done, but Mail.Rip v1 is worth testing it.</i>
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
    <li>macOS.</li>
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
    <li>email.mime,</li>
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
  <i>Mail.Rip is a basic SMTP checker / SMTP cracker. There are the following essential<br>
  "features":</i>
</p>
<p>
  <ul>
    <li>Tests mailpass combolists for working SMTP logins,</li>
    <li>hostdata for common SMTP providers is included,</li>
    <li>checks for most common SMTP (sub)domains if no host is found in included lists,</li>
    <li>tries to verify working SMTP logins by sending an e-mail to the user's address,</li>
    <li>supports multi-threading,</li>
    <li>stats are shown in window title,</li>
    <li>option to skip e-mail providers like Google, hotmail.com etc.,</li>
    <li>results are saved to textfiles for further investigation and</li>
    <li>SOCKS4- and SOCKS5-support with auto-scraping using Proxyscrape.com.</li>
  </ul>
</p>

<h4>Upcoming Features</h4>
<p>
  <i>There is still some work left to be done. Planned improvements are:</i>
</p>
<p>
  <ul>
    <li><del>Add SMTP ports to connection,</del> - <b>done, 2020-11-13</b></li>
    <li><del>improve SSL support for better results,</del> - <b>done, 2020-11-13</b></li>
    <li><del>add msg send to checking process (validation of cracked SMTP, inbox check)</del> - <b>done, 2020-11-15</b></li>
    <li><del><b>improve subdomain checking for unknown mailhosts,</b></del> - <b>done, 2020-11-13</b></li>
    <li><del>add a config.json to provide easier access to dictionaries and lists used by the checker</del> - <b>done, 2020-11-15</b><br>
      (request by <a href="https://github.com/Trustdee" target=_blank>Trustdee</a>),</li>
    <li><del><b>add support for SOCKS-proxys,</b></del> - <b>done, 2020-11-21</b></li>
    <li>speed up checking process / improve performance and</li>
    <li>some other stuff ...</li>
  </ul>
</p>
<p>
  <i>Note: Mail.Rip is now available as "proxyless" version (finished, released in v1.00) and<br>
    "proxy" version (finished, released in v1.00)!</i>
</p>

<h3>How to use ...</h3>
<p>
  <i>Just download / clone the files, install packages (see above) if needed and copy any mailpass<br>
    combolist to the same directory. Then type:</i>
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
python3 mailripV1.py
```

<p>
  <i>... then follow the text on your screen. Of course, you may rename the file for easier usage.<br>
  Moreover, you can modify the config.json for your needs. Just add or delete entries to / from the lists<br>
  or dictionaries.</i>
</p>

<h3>Support Mail.Rip v1</h3>
<p>
  <i>If you want to support this project, consider a donation!<br>
    Every donation is appreciated and helps with motivation for working on this tools.</i>
</p>
<p>
  <b>Donation Wallet (BTC):</b>   1M8PrpZ3VFHuGrnYJk63MtoEmoJxwiUxYf
</p>

<h4>Changelog</h4>
<p>
  <i>2020-10-18: releasing code version 0.3, creating repo, writing readme etc.</i><br>
  <i>2020-11-13: releasing code version 0.5, many improvements (see comment on commit of *.py-file).</i><br>
  <i>2020-11-15: releasing code version 0.9, big update (see comment on commit of *.py-file).</i><br>
  <i>2020-11-20: releasing code version 0.92, see commit comment for further information.</i><br>
  <i><b>2020-11-21: releasing code version 1.00 - now available for "proxyless" and "proxy" version!</b></i>
  <i>2020-11-27: releasing code version 1.07 for proxy-version, now supporting SOCKS4 and SOCKS5 proxies.</i>
</p>
