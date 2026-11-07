import sys
from pathlib import Path
sys.path.insert(0, 'tools/python')
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
EXE = Path(r'C:\Program Files (x86)\Steam\steamapps\common\HereSphere\HereSphere\Binaries\Win64\HereSphere-Win64-Shipping.exe')
SOURCE = EXE.with_name(EXE.name+'.cn-original')
if not SOURCE.exists():
    SOURCE = EXE
pe = pefile.PE(str(SOURCE), fast_load=True)
base = pe.OPTIONAL_HEADER.ImageBase
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True
def dis(start, size):
    for i in md.disasm(pe.get_data(start-base, size), start):
        print(f'{i.address:x}  {i.mnemonic:8} {i.op_str}')
if __name__ == '__main__':
    dis(int(sys.argv[1],16), int(sys.argv[2],16))
