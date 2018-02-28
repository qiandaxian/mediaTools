# -*- coding: UTF-8 -*-
import binascii
import re

data = "7E 01 00 00 21 00 00 00 00 86 27 00 06 00 00 00 00 00 00 00 00 00 48 42 2D 52 30 33 47 42 38 36 32 37 00 00 00 02 D4 C1 42 30 30 30 30 30 9A 7E"

rule_str = "1/2/5/1"

send_data = bytes().fromhex(data)

send_data_str = str(binascii.b2a_hex(send_data)).upper()[2:-1]

send_data_str_hex =  re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", send_data_str)

print(send_data_str_hex)


#TODO