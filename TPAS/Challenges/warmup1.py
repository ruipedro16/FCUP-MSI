#!/usr/bin/env python3

import hashlib

print('TPAS{' + hashlib.sha256(b'welcome').hexdigest() + '}')
