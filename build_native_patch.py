"""Patch FString-to-FText calls used to draw dropdowns and action titles.

The original option FStrings, comparison callbacks and saved values stay intact.
The leaf wrapper uses relative addressing, and static FString pointers have
standard PE base relocations so ASLR continues to work.
"""
import hashlib
import json
import struct
from inspect_native import SOURCE, pe, base
from keystone import Ks, KS_ARCH_X86, KS_MODE_64
from translate_catalog import translations
from translate_bindings import labels as binding_labels

ROOT = __import__('pathlib').Path(__file__).parent
data = SOURCE.read_bytes()
assert not any(s.Name.startswith(b'.hscn') for s in pe.sections)
catalog = dict(translations)
catalog.update({
    'Perspective': '透视', 'Fisheye': '鱼眼', 'Equirectangular': '等距柱状',
    'Equirectangular 360': '等距柱状 360°', 'Cubemap': '立方体贴图',
    'Equiangular Cubemap': '等角立方体贴图', 'Mono': '单目',
    'Side-By-Side': '左右格式', 'Top-Bottom': '上下格式',
    'Full Side-By-Side': '全宽左右格式', 'Autodetect': '自动检测',
    'Standard': '标准', 'High Definition': '高清', 'Wide Screen': '宽屏',
    'Custom': '自定义', 'Up': '向上', 'Down': '向下', 'Manual': '手动',
    'Global Setting': '全局设置', 'Chroma Key': '色度抠像', 'Alpha Packed': '打包透明通道',
    'None': '无', 'Linear': '线性', 'Nearest': '最近邻', 'Cubic': '三次插值',
    'Bilinear': '双线性', 'Bicubic': '双三次', 'Lanczos': 'Lanczos',
    'Media Foundation': 'Media Foundation', 'DirectShow': 'DirectShow',
})
catalog.update(binding_labels)
catalog = {s:t for s,t in catalog.items() if s and s != t and '\n' not in s and '\r' not in s}
align = lambda n,a: (n+a-1)//a*a
section_rva = align(pe.sections[-1].VirtualAddress + pe.sections[-1].Misc_VirtualSize,0x1000)
section_raw = align(len(data),0x200)
table_offset = 0x100
table_size = (len(catalog)+1)*16
payload = bytearray(table_offset+table_size)
relocations = []
for index,(source,target) in enumerate(sorted(catalog.items())):
    source_at = len(payload)
    payload.extend((source+'\0').encode('utf-16-le'))
    target_at = len(payload)
    payload.extend((target+'\0').encode('utf-16-le'))
    payload.extend(b'\0'*(align(len(payload),8)-len(payload)))
    string_at = len(payload)
    count = len((target+'\0').encode('utf-16-le'))//2
    payload.extend(struct.pack('<Qii',base+section_rva+target_at,count,count))
    relocations.append(section_rva+string_at)
    struct.pack_into('<iiii',payload,table_offset+index*16,
                     len((source+'\0').encode('utf-16-le'))//2,
                     source_at-table_offset,string_at-table_offset,0)

start = base+section_rva
ks = Ks(KS_ARCH_X86,KS_MODE_64)
code = bytearray()
labels, fixups = {}, []
def emit(text):
    encoded,_=ks.asm(text,addr=start+len(code))
    code.extend(encoded)
def lea(reg,va):
    emit(f'lea {reg}, [rip + {va-(start+len(code)+7)}]')
def branch(op,label):
    # All internal branches use explicit rel32 encoding.
    opcode={'je':b'\x0f\x84','jne':b'\x0f\x85','jmp':b'\xe9'}[op]
    code.extend(opcode)
    fixups.append((len(code),label))
    code.extend(b'\0'*4)
lea('r10',start+table_offset)
emit('mov r8d, dword ptr [rdx+8]; mov r9, qword ptr [rdx]')
labels['next']=len(code)
emit('cmp dword ptr [r10], 0')
branch('je','original')
emit('cmp r8d, dword ptr [r10]')
branch('jne','advance')
emit('movsxd r11, dword ptr [r10+4]')
lea('rax',start+table_offset)
emit('add r11, rax; xor eax, eax')
# Compare one UTF16 word at a time.
# R9 advances locally and is reset for each candidate; RDX remains canonical.
emit('mov r9, qword ptr [rdx]; mov r8d, dword ptr [rdx+8]')
labels['char']=len(code)
emit('movzx eax, word ptr [r9]; cmp ax, word ptr [r11]')
branch('jne','advance')
emit('add r9, 2; add r11, 2; dec r8d')
branch('jne','char')
emit('movsxd rax, dword ptr [r10+8]')
lea('rdx',start+table_offset)
emit('add rdx, rax')
branch('jmp','original')
labels['advance']=len(code)
emit('add r10, 16; mov r8d, dword ptr [rdx+8]')
branch('jmp','next')
labels['original']=len(code)
emit('jmp 0x140d06900')
for at,label in fixups:
    struct.pack_into('<i',code,at,labels[label]-(at+4))
assert len(code)<table_offset
payload[:len(code)] = code

# Preserve every original relocation; append DIR64 records for static strings.
payload.extend(b'\0'*(align(len(payload),4)-len(payload)))
reloc_at = len(payload)
directory = pe.OPTIONAL_HEADER.DATA_DIRECTORY[5]
payload.extend(pe.get_data(directory.VirtualAddress,directory.Size))
for page in sorted(set(r & ~0xfff for r in relocations)):
    entries = [0xa000 | (r-page) for r in relocations if r & ~0xfff == page]
    if len(entries)%2: entries.append(0)
    payload.extend(struct.pack('<II',page,8+len(entries)*2))
    payload.extend(struct.pack('<'+'H'*len(entries),*entries))
reloc_size = len(payload)-reloc_at
virtual_size = len(payload)
payload.extend(b'\0'*(align(len(payload),0x200)-len(payload)))
edits=[]
def edit(at,new):
    edits.append({'offset':at,'before':data[at:at+len(new)].hex(),'after':new.hex()})
hook_calls = [0x140bcd144, 0x140bcdc4d, 0x140bb65fe]
for va in hook_calls:
    at=pe.get_offset_from_rva(va-base)
    assert data[at:at+5] == b'\xe8'+struct.pack('<i',0x140d06900-va-5)
    edit(at,b'\xe8'+struct.pack('<i',start-va-5))
edit(pe.FILE_HEADER.get_field_absolute_offset('NumberOfSections'),struct.pack('<H',len(pe.sections)+1))
edit(pe.OPTIONAL_HEADER.get_field_absolute_offset('SizeOfImage'),struct.pack('<I',align(section_rva+virtual_size,0x1000)))
edit(directory.get_file_offset(),struct.pack('<II',section_rva+reloc_at,reloc_size))
at=pe.sections[-1].get_file_offset()+40
assert at+40<=pe.OPTIONAL_HEADER.SizeOfHeaders and data[at:at+40]==bytes(40)
edit(at,struct.pack('<8sIIIIIIHHI',b'.hscn\0\0\0',virtual_size,section_rva,len(payload),section_raw,0,0,0,0,0x60000020))
patched=bytearray(data)
for e in edits:
    p=e['offset']; n=bytes.fromhex(e['after']); patched[p:p+len(n)]=n
patched.extend(bytes(section_raw-len(patched)))
patched.extend(payload)
report={'original_sha256':hashlib.sha256(data).hexdigest(),'patched_sha256':hashlib.sha256(patched).hexdigest(),
        'original_bytes':len(data),'append_offset':section_raw,'edits':edits,'translations':len(catalog),
        'hook_calls':[hex(va) for va in hook_calls],
        'previous_patched_sha256':['f34f0e7b16bcb9652f5f010a22897e434d20a329b0e28393e9afa3ce4fcfc540']}
(ROOT/'release/native-section.bin').write_bytes(payload)
(ROOT/'release/native-patch.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
(ROOT/'native-test.exe').write_bytes(patched)
print(json.dumps({k:v for k,v in report.items() if k!='edits'},indent=2))
