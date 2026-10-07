"""CRT substitutes for offline x86 fixtures, preserving the caller's x87 mode.

These are executable stubs, not replacements for CTP binaries on disk.
"""
def ftol_stub():
    # Save CW, temporarily select RC=truncate, FISTP, restore CW, EDX:EAX result.
    return bytes.fromhex(
        '83ec10 d97c2408 668b442408 660d000c 668944240a '
        'd96c240a df3c24 d96c2408 58 5a 83c408 c3')

def floor_stub():
    # cdecl double at old ESP+4; preserve CW/precision, select RC=downward.
    return bytes.fromhex(
        '83ec08 d97c2400 668b0424 6625fff3 660d0004 6689442402 '
        'd96c2402 dd44240c d9fc d96c2400 83c408 c3')

def ceil_stub():
    # As floor, but RC=upward. Used only inside offline emulation.
    return bytes.fromhex(
        '83ec08 d97c2400 668b0424 6625fff3 660d0008 6689442402 '
        'd96c2402 dd44240c d9fc d96c2400 83c408 c3')
