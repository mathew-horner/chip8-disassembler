# CHIP-8 Disassembler

A disassembler for binaries written for the CHIP-8 system.

## How to Use

```
python3 main.py <ROM File>
```

This will print the disassembly to standard output. Each instruction is prefixed with what it's location would be in memory on the CHIP-8 system. [Most CHIP-8 programs are loaded into the same memory address (0x200 or 512)]

