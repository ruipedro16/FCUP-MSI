# TPAS - Lab 04 - Password cracking and exploitation

In this assignment, we'll look at password cracking and exploitation with metasploit.

## 1 - Tools

Please install:

- `metasploit`
```bash
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall && chmod 755 msfinstall && ./msfinstall
```
- `hashcat`
```bash
sudo apt-get install hashcat
```

## 2 - Tasks

There's no need to send solutions for this assignment, flags should be submitted directly on [tpas-desafios](https://tpas-desafios.alunos.dcc.fc.up.pt), except for the optional task for extra points. You can send your solution for the optional task via email to andre.baptista@fc.up.pt.

**EN**

1. Solve the `Crackstation` challenge on [tpas-desafios](https://tpas-desafios.alunos.dcc.fc.up.pt) with `hashcat`. More details are available in the challenge description. Useful link: https://hashcat.net/wiki/doku.php?id=mask_attack

2. Solve the `MSF` challenge on [tpas-desafios](https://tpas-desafios.alunos.dcc.fc.up.pt) with `metasploit`.
    - Identify the software running behind Nginx and search for exploits on `msfconsole`.
    - Recommended payload: `payload/generic/shell_bind_tcp`
    - Avaialble ports for binding: `5050-5070`
    - After opening a shell session, run `cat /flag.txt` 

3. Special task (optional):
    - Implement the exploit of the `msf` challenge in a programming language of your choice (50 points).
