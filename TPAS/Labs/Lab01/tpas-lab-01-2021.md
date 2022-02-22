# TPAS - Lab 01 - Linux Introduction

With this guide, you should learn more about commands and explore the Linux terminal. We will also configure and install the required tools for the classes.

## 1 - Network configuration

Please access https://tpas-desafios.alunos.dcc.fc.up.pt. Please ignore the current SSL errors and proceed (problem will be solved ASAP). If you can access the platform, please ignore this section.

If you're using the lab computers, it's possible that the challenge server does not resolve correctly. If necessary, please configure an alternative DNS server on your network settings. Please remember to click `Apply` or restart the network adapter after changing your network settings.

Example for Ubuntu:

https://tpas.alunos.dcc.fc.up.pt/images/lab/network-settings-ece6089f61fc526046f77d934e626959b390de83.png

https://tpas.alunos.dcc.fc.up.pt/images/lab/dns-config-3e1276f210df4bdcf917972b6a0b2792f5e4a763.png

You should now have access to https://tpas-desafios.alunos.dcc.fc.up.pt

## 2 - Account creation

Create an account on `tpas-desafios` with your preferred 1337 hacker username, but please remember to sign up with **your student email**.

## 3 - Generic commands

Use the Windows key to open the terminal by writing "terminal" on the search bar. Or you can use the shortcut `CTRL+ALT+T`.

- Change directory:
```bash
user@ubuntu:~$ cd Desktop
```
- Go to the parent directory:
```bash
user@ubuntu:~$ cd ..
```
- Create a directory:
```bash
user@ubuntu:~$ mkdir new-folder
```
- View the current path:
```bash
user@ubuntu:~$ pwd
```
- List files and folders in the current directory:
```bash
user@ubuntu:~$ ls
```
- Create an empty file on the `Documents` directory:
```bash
user@ubuntu:~$ cd Documents
user@ubuntu:~$ touch file1.txt
user@ubuntu:~$ cd ..
```
- List relative or absolute paths:
```bash
user@ubuntu:~$ ls Documents
file1.txt
user@ubuntu:~$ ls /home/ciencia/Documents
file1.txt
```
- View the current user information:
```bash
user@ubuntu:~$ whoami
```
- Run a command as root (higher privileges):
```bash
user@ubuntu:~$ sudo whoami
```
- Update the operative system/distribution:
```bash
user@ubuntu:~$ sudo apt update
user@ubuntu:~$ sudo apt upgrade
```
or
```bash
user@ubuntu:~$ sudo apt-get update
user@ubuntu:~$ sudo apt-get upgrade
```
- Example: Installing the `terminator` software from the repositories:
```bash
user@ubuntu:~$ sudo apt update
user@ubuntu:~$ sudo apt install terminator
```

## 4 - Terminal commands assignment

Send the solutions to the professor via email to andre.baptista@fc.up.pt or show them in person during the class. If all answers are correct, you'll get points for the `Lab 01` challenge on https://tpas-desafios.alunos.dcc.fc.up.pt

**EN**

- How can you change the directory to your home folder?
- How can you change to the previous directory (not the parent directory)?
- How can you obtain the type of a given file?
- How can you list hidden files in your home folder?
- How can you change to the root user persistently?
- How can you change your user password?
- How can you list all the users on the machine?
- How can you change the password of any user?
- How can you retrieve details about your current user? (i.e, viewing the ID and groups)
- How can you retrieve the current Linux kernel version?
- How can you obtain more information about a given command through the man pages?
- How can you obtain a web page through the terminal. What tools can you use?
- How can you retrieve your private/internal IP address? What about the public/external IP address?

**PT**

- Como mudar de directório para a nossa home folder?
- Como voltar para o directório em que estavamos antes da última mudança de directório?
- Como obter o tipo de um ficheiro?
- Como listar ficheiros ocultos na home folder?
- Como mudar o utilizador para root de forma permanente?
- Como alterar a password do utilizador através do terminal?
- Como listar todos os utilizadores da máquina?
- Como alterar a password de qualquer utilizador?
- Como obter detalhes sobre o nosso utilizador actual com maior detalhe? (i.e, obter o seu ID, grupo)
- Como obter a versão do kernel Linux actual?
- Como obter mais informações sobre um comando através das man pages?
- Como obter uma página web através do terminal? Que ferramentas existem?
- Como obter o nosso endereço IP privado/interno? E o público/externo?

## 5 - Important: Installing software that we’ll need

- `nmap`
- `wireshark`
- `exiftool`
- `Metasploit framework` (https://github.com/rapid7/metasploit-framework/wiki/Nightly-Installers)
- `aircrack-ng` (https://www.aircrack-ng.org/doku.php?id=install_aircrack#installing_pre-compiled_binaries)
- `john-the-ripper`
- `exiftool`
- `gdb-gef` (https://github.com/hugsy/gef)
- `pwntools` (https://github.com/Gallopsled/pwntools)
- `Ghidra` (https://ghidra-sre.org/)
- `relative-url-extractor` (https://github.com/jobertabma/relative-url-extractor)
- `waybackurls` (https://github.com/tomnomnom/waybackurls)
- `Dirsearch` (https://github.com/maurosoria/dirsearch)
- `Ffuf` (https://github.com/ffuf/ffuf)
- `Sublist3r` (https://github.com/aboul3la/Sublist3r)
- `subfinder` (https://github.com/subfinder/subfinder)
- `Aquatone` (https://github.com/michenriksen/aquatone)
- `Nuclei` (https://github.com/projectdiscovery/nuclei)
- `Burp Suite - Community` (https://portswigger.net/burp)

## 6 - Exploring tools and solving challenges

After installing tools, you can start exploring features or go ahead and try solving a few basic challenges on the `tpas-desafios` platform.

**Important:** Please don't target any public IP address, but feel free to scan the host `tpas.alunos.dcc.fc.up.pt` (e.g. with nmap).