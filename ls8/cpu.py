"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] *  256
        self.pc = 0
        self.reg = [0] * 8

    def load(self):
        """Load a program into memory."""

        # address = 0

        file_name = sys.argv[1]

        # program = [
            # From print8.ls8
            # 0b10000010, # LDI R0,8
            # 0b00000000,
            # 0b00001000,
            # 0b01000111, # PRN R0
            # 0b00000000,
            # 0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
        address = 0
        with open(file_name) as f:
            for line in f:
                line = line.rstrip('\n')
                line = line.split('#')[0]
                
                if line:
                    value = int(line, 2)
                    self.ram[address] = value
                    address += 1


    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

# 10000010 # LDI R0,8
# 00000000
# 00001000
# 10000010 # LDI R1,9
# 00000001
# 00001001
# 10100010 # MUL R0,R1
# 00000000
# 00000001
# 01000111 # PRN R0
# 00000000
# 00000001 # HLT

    def run(self):
        """Run the CPU."""
        running = True

        def ldi():
            reg_num = self.ram_read(self.pc + 1)
            value = self.ram_read(self.pc + 2)
            self.reg[reg_num] = value
            self.pc += 3

        def prn():
            reg_num = self.ram_read(self.pc + 1)
            print(self.reg[reg_num])
            self.pc += 2

        def multi():
            reg_num = self.ram_read(self.pc + 1)
            reg_num2 = self.ram_read(self.pc + 2)
            self.reg[reg_num] *= self.reg[reg_num2]
            self.pc += 3

        def stop():
            running = False
            self.pc += 1 

        def errors():
            print(f'Unknown instruction {ir} at address {self.pc}')
            sys.exit(1)

        def call_table(n):

            branch_table = {
                1: ldi,
                2: prn, 
                3: multi,
                4: stop,
                5: errors
            }
        

        branch_table[n]()


        while running:
            ir = self.ram_read(self.pc)
            if ir == 0b10000010: # read from memory and setting it to register at cpu
                # reg_num = self.ram_read(self.pc + 1)
                # value = self.ram_read(self.pc + 2)
                # self.reg[reg_num] = value
                # self.pc += 3
                call_table(1)

            elif ir == 0b01000111:  # print
                # reg_num = self.ram_read(self.pc + 1)
                # print(self.reg[reg_num])
                # self.pc += 2
                call_ta ble(2)
            elif ir == 0b10100010:   # muliply
                # reg_num = self.ram_read(self.pc + 1)
                # reg_num2 = self.ram_read(self.pc + 2)
                # self.reg[reg_num] *= self.reg[reg_num2]
                # self.pc += 3
                call_table(3)

            elif ir ==  0b00000001:
                # running = False
                # self.pc += 1   
                call_table(4)

            else:
                # print(f'Unknown instruction {ir} at address {self.pc}')
                # sys.exit(1)
                call_table(5)
                

