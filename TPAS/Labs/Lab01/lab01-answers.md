# Lab 01 - Linux Introduction

## 4 - Terminal commands

- How can you change the directory to your home folder? ``cd``
- How can you change to the previous directory (not the parent directory)? ``cd -``
- How can you obtain the type of a given file? ``file <filename>``
- How can you list hidden files in your home folder? ``ls -a $HOME``
- How can you change to the root user persistently? ``sudo su``
- How can you change your user password? ``sudo passwd <username>``
- How can you list all the users on the machine? ``cat /etc/passwd``
- How can you change the password of any user? ``sudo passwd <username>``
- How can you retrieve details about your current user? (i.e, viewing the ID and groups) ``who``
- How can you retrieve the current Linux kernel version? ``uname -r``
- How can you obtain more information about a given command through the man pages? ``man <command>``
- How can you obtain a web page through the terminal. What tools can you use? ``wget``, ``curl``
- How can you retrieve your private/internal IP address? What about the public/external IP address? ``hostname -I | awk '{print $1}'`` (private), ``curl ifconfig.me.`` (public)

