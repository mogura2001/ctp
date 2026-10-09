"""Finite x86 byte emitter, extending the existing H1 Recipe only.

No assembler/compiler installation. Every emitted instruction is independently
decoded by Capstone before use. Operands are registers or base+disp32 memory.
"""
import sys, struct
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'score-h1'))
from build import Recipe
REG={'eax':0,'ecx':1,'edx':2,'ebx':3,'esp':4,'ebp':5,'esi':6,'edi':7}
def u32(n):return struct.pack('<I',n&0xffffffff)
def mem(base,disp=0):return (base,disp)
class X86(Recipe):
 def op(self,name,b):self.emit(name,bytes(b).hex())
 def rm(self,reg,operand):
  if isinstance(operand,str):return bytes([0xc0|(reg<<3)|REG[operand]])
  base,disp=operand;n=REG[base]
  return bytes([0x80|(reg<<3)|n])+ (b'\x24' if n==4 else b'')+u32(disp)
 def ins(self,name,opcode,reg,operand):self.op(name,bytes.fromhex(opcode)+self.rm(reg,operand))
 def mov(self,dst,src):
  if isinstance(src,int):
   if isinstance(dst,str):self.op(f'mov {dst},{src}',bytes([0xb8+REG[dst]])+u32(src))
   else:self.op(f'mov {dst},{src}',b'\xc7'+self.rm(0,dst)+u32(src))
  elif isinstance(dst,str):self.ins(f'mov {dst},{src}','8b',REG[dst],src)
  else:self.ins(f'mov {dst},{src}','89',REG[src],dst)
 def lea(self,dst,operand):self.ins(f'lea {dst},{operand}','8d',REG[dst],operand)
 def load(self,dst,operand,kind):self.ins(f'{kind} {dst},{operand}',{'sx16':'0fbf','zx16':'0fb7','sx8':'0fbe'}[kind],REG[dst],operand)
 def word(self,dst,src):self.ins(f'mov word {dst},{src}','6689',REG[src],dst)
 def alu(self,name,dst,src):
  table={'add':(0,'03'),'or':(1,'0b'),'adc':(2,'13'),'sbb':(3,'1b'),'and':(4,'23'),'sub':(5,'2b'),'xor':(6,'33'),'cmp':(7,'3b')}
  group,op=table[name]
  if isinstance(src,int):self.op(f'{name} {dst},{src}',b'\x81'+self.rm(group,dst)+u32(src))
  elif isinstance(dst,str):self.ins(f'{name} {dst},{src}',op,REG[dst],src)
  else:self.ins(f'{name} {dst},{src}',{'add':'01','adc':'11','sub':'29','sbb':'19','cmp':'39','or':'09','and':'21','xor':'31'}[name],REG[src],dst)
 def test(self,dst,src):
  if isinstance(src,int):self.op(f'test {dst},{src}',b'\xf7'+self.rm(0,dst)+u32(src))
  else:self.ins(f'test {dst},{src}','85',REG[src],dst)
 def push(self,src):
  if isinstance(src,int):self.op(f'push {src}',b'\x68'+u32(src))
  elif isinstance(src,str):self.op('push '+src,bytes([0x50+REG[src]]))
  else:self.ins(f'push {src}','ff',6,src)
 def pop(self,reg):self.op('pop '+reg,bytes([0x58+REG[reg]]))
 def shift(self,kind,dst,n):self.op(f'{kind} {dst},{n}',b'\xc1'+self.rm({'shl':4,'shr':5,'sar':7}[kind],dst)+bytes([n]))
 def imul(self,dst,src,n):self.op(f'imul {dst},{src},{n}',b'\x69'+self.rm(REG[dst],src)+u32(n))
 def unary(self,kind,dst):self.ins(f'{kind} {dst}','ff',{'inc':0,'dec':1,'call':2}[kind],dst)
 def j(self,kind,label):self.branch(kind+' '+label,{'jmp':'e9','call':'e8','je':'0f84','jne':'0f85','jz':'0f84','jnz':'0f85','jl':'0f8c','jle':'0f8e','jg':'0f8f','jge':'0f8d','jb':'0f82','ja':'0f87','jae':'0f83','jbe':'0f86','jo':'0f80','js':'0f88','jp':'0f8a'}[kind],label)
 def prologue(self,n):
  self.push('ebp');self.mov('ebp','esp')
  for a in ('ebx','esi','edi'):self.push(a)
  self.alu('sub','esp',n)
 def epilogue(self,n,pop):
  self.alu('add','esp',n)
  for a in ('edi','esi','ebx','ebp'):self.pop(a)
  self.op(f'ret {pop}',b'\xc2'+struct.pack('<H',pop))
 def zero(self,ptr,n):
  self.mov('edi',ptr);self.mov('eax',0);self.mov('ecx',n//4);self.op('cld',b'\xfc');self.op('rep stosd',b'\xf3\xab')
 def fp(self,name,opcode,group,operand):self.op(f'{name} {operand}',bytes.fromhex(opcode)+self.rm(group,operand))
