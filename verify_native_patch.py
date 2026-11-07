"""Execute the emitted x64 leaf wrapper against every translation under ASLR."""
import sys
sys.path.insert(0,'tools/python')
import struct
from pathlib import Path
import pefile
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64
from unicorn.x86_const import UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_RSP

p=pefile.PE('native-test.exe',fast_load=True)
original_base=p.OPTIONAL_HEADER.ImageBase
directory=p.OPTIONAL_HEADER.DATA_DIRECTORY[5]
reloc=p.get_data(directory.VirtualAddress,directory.Size)
fixups=[]
offset=0
while offset<len(reloc):
    page,size=struct.unpack_from('<II',reloc,offset)
    assert size>=8 and size%4==0
    for at in range(offset+8,offset+size,2):
        item,=struct.unpack_from('<H',reloc,at)
        if item>>12==10: fixups.append(page+(item&0xfff))
    offset+=size
section=p.sections[-1]
assert section.Name.startswith(b'.hscn')
for shift in [0,0x12500000]:
    loaded_base=original_base+shift
    mapped=bytearray(section.get_data())
    for rva in fixups:
        if section.VirtualAddress<=rva<section.VirtualAddress+len(mapped):
            at=rva-section.VirtualAddress
            ptr,=struct.unpack_from('<Q',mapped,at)
            struct.pack_into('<Q',mapped,at,ptr+shift)
    uc=Uc(UC_ARCH_X86,UC_MODE_64)
    start=loaded_base+section.VirtualAddress
    uc.mem_map(start,(len(mapped)+0xfff)&~0xfff)
    uc.mem_write(start,bytes(mapped))
    scratch=0x60000000
    uc.mem_map(scratch,0x10000)
    stop=loaded_base+0xd06900
    table=p.get_data(section.VirtualAddress+0x100,0x100000)
    entries=[]
    for at in range(0,len(table),16):
        count,source,target,_=struct.unpack_from('<iiii',table,at)
        if not count: break
        text=table[source:source+count*2].decode('utf-16-le')[:-1]
        entries.append((text,start+0x100+target))
    for source,expected in entries+[('Untranslated filename',scratch),('',scratch),('perspective',scratch)]:
        raw=(source+'\0').encode('utf-16-le')
        uc.mem_write(scratch+0x100,raw)
        record=struct.pack('<Qii',scratch+0x100,len(raw)//2,len(raw)//2)
        uc.mem_write(scratch,record)
        uc.reg_write(UC_X86_REG_RCX,scratch+0x800)
        uc.reg_write(UC_X86_REG_RDX,scratch)
        uc.reg_write(UC_X86_REG_RSP,scratch+0xf000)
        uc.emu_start(start,stop,count=200000)
        assert uc.reg_read(UC_X86_REG_RCX)==scratch+0x800
        assert uc.reg_read(UC_X86_REG_RDX)==expected,(source,hex(uc.reg_read(UC_X86_REG_RDX)),hex(expected))
        assert uc.mem_read(scratch,16)==record
        if expected!=scratch:
            ptr,length,capacity=struct.unpack('<Qii',uc.mem_read(expected,16))
            assert ptr>=start and ptr<start+section.Misc_VirtualSize
            value=bytes(uc.mem_read(ptr,length*2)).decode('utf-16-le')
            assert value.endswith('\0') and length==capacity
    print(f'ASLR +0x{shift:x}: {len(entries)} translations and 3 passthrough cases passed')
