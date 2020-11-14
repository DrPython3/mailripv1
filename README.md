# Mail.Rip v1
<p><i>A SMTP checker / SMTP cracker including an inbox check for testing mailpass combolists.</i></p>

<h2>Legal Notices</h2>
<p>
  <b><u>The code published here is for educational purposes only!</u></b><br>
  You are not allowed to use it for any kind of illegal activity nor law enforcement at any time.
</p>

<h2>Overview</h2>
<p>
  <i>Mail.Rip v1 is written in Python 3.8 and still being improved though it is already functional and delivering results very fast.<br>
    The goal of this project is to offer a tool which is easy to use, providing stable results over time.<br>
    There is still work to be done, but Mail.Rip v1 is worth testing it.</i>
</p>

<h3>Requirements</h3>
<p><i>For runninng Mail.Rip v1 you need <b>Python 3.8+</b> to be installed on your system. It has been tested on:</i></p>
<p>
  <ul>
    <li>Windows 10,</li>
    <li>KALI Linux and</li>
    <li>macOS.</li>
  </ul>
</p>
<p><b>Used modules are:</b></p>
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
    <li>SMTPEmail and</li>
    <li>uuid.</li>
  </ul>
</p>
<p>
  Moreover, <i>PyInstaller</i> can be used for creating a *.EXE.<br>
  Tested on Windows 10.
</p>

<h3>Features</h3>
<p><i>Mail.Rip is a basic SMTP checker / SMTP cracker. There are only a few, but essential "features":</i></p>
<p>
  <ul>
    <li>Tests mailpass combolists for working SMTP logins,</li>
    <li>hostdata for common SMTP providers is included,</li>
    <li>checks for most common SMTP (sub)domains if no host is found in included lists,</li>
    <li>supports multi-threading,</li>
    <li>stats are shown in window title (if run on Windows),</li>
    <li>option to skip e-mail providers like Google, hotmail.com etc. and</li>
    <li>results are saved to textfiles for further investigation.</li>
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
    <li><b>add msg send to checking process (validation of cracked SMTP, inbox check)</b></li>
    <li><del><b>improve subdomain checking for unknown mailhosts,</b></del> - <b>done, 2020-11-13</b></li>
    <li>speed up checking process / improve performance,</li>
    <li>add a config.json to provide easier access to dictionaries and lists used by the checker<br>
      (request by <a href="https://github.com/Trustdee" target=_blank>Trustdee</a>) and</li>
    <li>some other stuff ...</li>
  </ul>
</p>

<h3>How to use ...</h3>
<p>
  <i>Just download the *.PY file, install modules (see above) if needed and copy any maillpass combolist to the same directory.<br>
    Then type:</i>
</p>

```
python3 mailripV1.py
```

<p>
  <i>... and follow the text on your screen. Of course, you may rename the file for easier usage.</i>
</p>

<h3>Support Mail.Rip v1</h3>
<p>
  <i>If you want to support this project, consider a donation in Bitcoin (BTC).<br>
    Every donation is appreciated and helps with motivation for working on this tools.<br>
    Special donators may be named on starting sceen of Mail.Rip v1!<br>
    In this case, contact me before donating, please!</i>
</p>
<p>
  <b>Donation Wallet:</b>   1M8PrpZ3VFHuGrnYJk63MtoEmoJxwiUxYf
</p>

<h4>Changelog</h4>
<p>
  <i>2020-10-18: releasing code version 0.3, creating repo, writing readme etc.</i><br>
  <i>2020-11-13: releasing code version 0.5, many improvements (see comment on changes of *.py-file).</i>
</p>
