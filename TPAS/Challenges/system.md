# System

Inspecting the binary in [Ghidra](https://github.com/NationalSecurityAgency/ghidra), we can see the following function,

```c
undefined8 check_flag(char *param_1)

{
  int iVar1;
  size_t sVar2;
  undefined8 uVar3;
  
  sVar2 = strlen(param_1);
  if (sVar2 == 0x19) {
    iVar1 = strncmp("ecrimectf{",param_1,10);
    if (iVar1 == 0) {
      if (param_1[0x18] == '}') {
        if (((param_1[0xd] == '_') && (param_1[0x11] == '_')) && (param_1[0x14] == '_')) {
          if (param_1[10] == 'y') {
            if (param_1[0xe] == 'a') {
              if (param_1[0x12] == 's') {
                if (param_1[0x15] == 'l') {
                  if ((int)param_1[0x16] == param_1[0x15] + -3) {
                    if ((int)param_1[0x17] == param_1[10] + -5) {
                      if ((int)param_1[0xb] == *param_1 + -0x35) {
                        if (param_1[0xb] == param_1[0x13]) {
                          if (param_1[2] == param_1[0xf]) {
                            if ((int)param_1[0x10] == param_1[0xb] + 3) {
                              if ((byte)(param_1[9] ^ param_1[0xc]) == 0xe) {
                                uVar3 = 1;
                              }
                              else {
                                uVar3 = 0;
                              }
                            }
                            else {
                              uVar3 = 0;
                            }
                          }
                          else {
                            uVar3 = 0;
                          }
                        }
                        else {
                          uVar3 = 0;
                        }
                      }
                      else {
                        uVar3 = 0;
                      }
                    }
                    else {
                      uVar3 = 0;
                    }
                  }
                  else {
                    uVar3 = 0;
                  }
                }
                else {
                  uVar3 = 0;
                }
              }
              else {
                uVar3 = 0;
              }
            }
            else {
              uVar3 = 0;
            }
          }
          else {
            uVar3 = 0;
          }
        }
        else {
          uVar3 = 0;
        }
      }
      else {
        uVar3 = 0;
      }
    }
    else {
      uVar3 = 0;
    }
  }
  else {
    uVar3 = 0;
  }
  return uVar3;
}
```

Performing the necessary calculations, we can see that the flag is `ecrimectf{y0u_ar3_s0_lit}`