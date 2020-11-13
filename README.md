# Mail.Rip v1
<p><i>Basic SMTP checker / SMTP cracker for testing mailpass combolists.</i></p>

<h2>Legal Notices</h2>
<p>This tool ist for educational purposes only. You are not allowed to use it for any kind of illegal activity nor law enforcement at any time.</p>

<h2>Overview</h2>
<p><b>STILL IN DEVELOPMENT -- ERRORS MAY OCCUR WHILE USING IT! SEE DETAILS BELOW.</b></p>
<p><i>Mail.Rip v1 is written in Python 3 and uses smtplib. Though being still improved, it is already functional and mostly working fast. The goal is to offer a tool which is easy to use and providing stable results over time. There is still a lot of work to be done, but Mail.Rip v1 is already worth testing it.</i></p>

<h3>Requirements</h3>
<p><i>For runninng Mail.Rip v1 you need <b>Python 3</b> to be installed on your system. It has been tested on:</i></p>
<p>
  <ul>
    <li>Windows 10,</li>
    <li>KALI Linux and</li>
    <li>macOS.</li>
  </ul>
</p>
<p><b>Required modules are:</b></p>
<p>
  <ul>
    <li>ctypes,</li>
    <li>os,</li>
    <li>smtplib,</li>
    <li>socket,</li>
    <li>sys,</li>
    <li>ssl,</li>
    <li>threading,</li>
    <li>time and</li>
    <li>colorama.</li>
  </ul>
</p>
<p><i>Moreover, PyInstaller can be used for creating a *.EXE. Tested on Windows 10.</i></p>

<h3>Features</h3>
<p><i>As said before, Mail.Rip is a bsic SMTP checker / SMTP cracker. There are only a few "features" so far:</i></p>
<p>
  <ul>
    <li>Tests mailpass combolists for working SMTP logins,</li>
    <li>hostdata for common SMTP providers is included in the ccode,</li>
    <li>checks for most common SMTP subdomains if no hostdata is defined,</li>
    <li>supports multi-threading,</li>
    <li>stats are shown in window title if run on Windows,</li>
    <li>option to skip e-mail providers like Google, hotmail.com etc. and</li>
    <li>results are saved to textfiles for further investigation.</li>
  </ul>
</p>

<h3>Work still to be done ...</h3>
<p><i>There is still some work left to be done. Planned improvements are:</i></p>
<p>
  <ul>
    <li><del>Add SMTP ports to connection,</del> - <b>done, 2020-11-13</b></li>
    <li><del>include improved SSL support for better results,</del> - <b>done, 2020-11-13</b></li>
    <li><b>add mail send to checking process (validation of cracked SMTP, inbox check)</b></li>
    <li><del><b>improve subdomain checking for unknown mailhosts,</b></del> - <b>done, 2020-11-13</b></li>
    <li>speed up checking process / improve performance,</li>
    <li><b>add proxy support (SOCKS4 and SOCKS5, especially rotating proxys)</b> and</li>
    <li>some other stuff ...</li>
  </ul>
</p>

<h3>How to use ...</h3>
<p><i>Just download the *.PY file, install modules (see above) if needed and copy any maillpass combolist to the same directory. Then type:</i></p>

```
python3 mailripV1.py
```

<p><i>... and follow the text on your screen. Of course, you may rename the file for easier usage.</i></p>

<h4>Support Mail.Rip v1</h4>
<p><i>If you want to support this project, consider a donation in Bitcoin (BTC). Every donation is appreciated and helps with motivation for working on this tools. Special donators may be named on starting sceen of Mail.Rip v1! In this case, contact me before donating, please!</i></p>
<p><b>Donation Wallet:</b>   1M8PrpZ3VFHuGrnYJk63MtoEmoJxwiUxYf</p>

<h5>Changelog</h5>
<p><i>2020-10-18 -- releasing code version 0.3, creating repo, writing readme etc.</i><br>
<i>Last changes: 2020-11-13 -- releasing code version 0.5, many improvements (see comment on changes of *.py-file).</i></p>
