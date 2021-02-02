import pygame
from pygame import Rect
import random
from time import time


class Chip8:
    # Virtual Memory
    memory = [0] * 4096

    # Stack
    stack = [0] * 16

    # Register
    v = [0] * 16

    # Program Counter, Index and opcode
    pc = 0x200  # stores current executed address
    index = 0  # stores memory address Aka I

    # Timer
    delay_timer = 0
    sound_timer = 0
    last_time = 0

    # Display and Screen Stuff
    draw_flag = True
    display_array = [0] * 64 * 32
    screen = 0  # Later used for Pygame
    color1 = 0, 0, 0  # Black
    color2 = 255, 255, 255  # White
    colors = [color1, color2]
    icon = 0
    clock = 0

    # Keyboard and Keys
    keyboard = [0] * 16
    keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_c,
            pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_d,
            pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_e,
            pygame.K_a, pygame.K_0, pygame.K_b, pygame.K_f]

    # var to check if running or not
    running = True

    def __init__(self):
        self.memory = [0] * 4096
        self.stack = [0] * 16
        self.v = [0] * 16
        self.draw_flag = True
        self.display_array = [0] * 64 * 32
        self.screen = 0
        self.color1 = 0, 0, 0
        self.color2 = 255, 255, 255
        self.colors = [self.color1, self.color2]
        self.pc = 0x200
        self.index = 0
        self.opcode = 0
        self.delay_timer = 0
        self.sound_timer = 0
        self.last_time = time()

    def init_screen(self, name_of_rom):
        pygame.init()
        pygame.display.set_caption(f"Chip8-Emulator - {name_of_rom}")
        self.icon = pygame.image.load("icon/cow.ico")
        pygame.display.set_icon(self.icon)
        self.clock = pygame.time.Clock()
        self.clock.tick(60)
        self.screen = pygame.display.set_mode((64 * 10, 32 * 10))

    def clear_screen(self):
        self.display_array = [0] * 64 * 32
        self.screen.fill((0, 0, 0))
        pygame.display.flip()

    def draw_on_screen(self, width, height):
        width = 64
        height = 32
        for x in range(64):
            for y in range(32):
                self.screen.fill(self.colors[self.display_array[x + (y * 64)]], Rect(x * 10, y * 10, 10, 10))

        pygame.display.flip()
        self.draw_flag = False

    def rom_loader(self, rom_name):
        print("Loading  ROM into Memory...")
        file = open(rom_name, "rb")
        rom = file.read()
        for i in range(len(rom)):
            self.memory[self.pc + i] = rom[i]
        print("ROM loaded.")
        file.close()

    def execute_opcode(self):
        self.opcode = self.memory[self.pc] << 8 | self.memory[self.pc + 1]
        print("Opcode:", hex(self.opcode))
        x = (self.opcode & 0x0F00) >> 8
        y = (self.opcode & 0x00F0) >> 4
        foo = (self.opcode & 0xF000)

        if foo == 0x0000:  # 0NNN
            if self.opcode == 0x00E0:  # 00E0
                # print("Clears the  Screen")
                self.clear_screen()
            elif self.opcode == 0x00EE:  # 00EE
                # print("Returns from a subroutine")
                self.pc = self.stack.pop()

        elif foo == 0x1000:  # 1NNN
            self.pc = (self.opcode & 0x0FFF) - 2
        # print("Jumps to address NNN")

        elif foo == 0x2000:  # 2NNN
            # print("Calls subroutine at NNN")
            self.stack.append(self.pc)
            self.pc = (self.opcode & 0x0FFF) - 2

        elif foo == 0x3000:  # 3XNN
            if self.v[x] == (self.opcode & 0x00FF):
                self.pc = self.pc + 2
            # print("Skips the next instruction if VX equals NN")

        elif foo == 0x4000:  # 4XNN
            if self.v[x] != (self.opcode & 0x00FF):
                self.pc = self.pc + 2
            # print("Skips the next instruction if VX doesn't equal NN")

        elif foo == 0x5000:  # 5XY0
            if self.v[x] == self.v[y]:
                self.pc = self.pc + 2
            # print("	Skips the next instruction if VX equals VY")

        elif foo == 0x6000:  # 6XNN
            self.v[x] = (self.opcode & 0x00FF)
        # print("Sets VX to NN")

        elif foo == 0x7000:  # 7XNN
            self.v[x] = self.v[x] + (self.opcode & 0x00FF)
            self.v[x] &= 0xFF
        # print("Adds NN to VX")

        elif foo == 0x8000:
            foo2 = (self.opcode & 0x000F)
            if foo2 == 0x0000:  # 8XY0
                self.v[x] = self.v[y]
            # print("Sets VX to the value of VY")
            elif foo2 == 0x0001:  # 8XY1
                self.v[x] |= self.v[y]
            # print("Sets VX to VX or VY(Bitwise OR)")
            elif foo2 == 0x0002:  # 8XY2
                self.v[x] &= self.v[y]
            # print("Sets VX to VX and VY(Bitwise AND)")
            elif foo2 == 0x0003:  # 8XY3
                self.v[x] ^= self.v[y]
            # print("Sets VX to VX xor VY(Bitwise XOR)")
            elif foo2 == 0x0004:  # 8XY4
                self.v[x] += self.v[y]
                if self.v[x] > 0xFF:
                    self.v[0xF] = 1
                else:
                    self.v[0xF] = 0
                self.v[x] &= 0xFF
            # print("Adds VY to VX. VF is set to 1 when there's a carry, and to 0 when there isn'")
            elif foo2 == 0x0005:  # 8XY5
                if self.v[x] < self.v[y]:
                    self.v[0xF] = 0
                else:
                    self.v[0xF] = 1
                self.v[x] -= self.v[y]
                self.v[x] &= 0xFF
            # print("VY is subtracted from VX. VF is set to 0 when there's a borrow, and 1 when there isn't")
            elif foo2 == 0x0006:  # 8XY6
                self.v[0xF] = self.v[x] & 0x1
                self.v[x] = self.v[x] >> 1
            # print("	Stores the least significant bit of VX in VF and then shifts VX to the right by 1")
            elif foo2 == 0x0007:  # 8XY7
                self.v[0xF] = 0
                if self.v[x] > self.v[y]:
                    self.v[0xF] = 1
                self.v[x] = self.v[x] - self.v[y]
            # print("Sets VX to VY minus VX. VF is set to 0 when there's a borrow, and 1 when there isn't")
            elif foo2 == 0x000E:  # 8XYE
                self.v[0xF] = (self.v[x] & 0x80)
                self.v[x] = self.v[x] << 1
            # print("Stores the most significant bit of VX in VF and then shifts VX to the left by 1")

        elif foo == 0x9000:  # 9XY0
            if self.v[x] != self.v[y]:
                self.pc = self.pc + 2
        # print("Skips the next instruction if VX doesn't equal VY")

        elif foo == 0xA000:  # ANNN
            self.index = (self.opcode & 0x0FFF)
        # print("Sets I to the address NNN")

        elif foo == 0xB000:  # BNNN
            self.pc = (self.opcode & 0x0FFF) + self.v[0] - 2
        # print("Jumps to the address NNN plus V0")

        elif foo == 0xC000:  # CXNN
            rand = random.randint(0, 0xFF)
            self.v[x] = rand & (self.opcode & 0x00FF)
        # print("Sets VX to the result of a bitwise and operation on a random number (Typically: 0 to 255) and NN")

        elif foo == 0xD000:  # DXYN
            pos_x = self.v[x]
            pos_y = self.v[y]
            height = (self.opcode & 0x000F)
            self.v[0xF] = 0
            sprite = 0

            for y_cord in range(height):
                sprite = self.memory[self.index + y_cord]
                for x_cord in range(8):
                    f = pos_x + x_cord + ((pos_y + y_cord) * 64)
                    if sprite & (0x80 >> x_cord) != 0 and not (y_cord + pos_y >= 32 or x_cord >= 64):
                        if self.display_array[f] == 1:
                            self.v[0xF] = 1
                        self.display_array[f] ^= 1
            self.draw_flag = True
        # print("Draws a sprite at coordinate (VX, VY) that has a width of 8 pixels and a height of N+1 pixels")
        # print("Each row of 8 pixels is read as bit-coded starting from memory location I")
        # print("I value doesn’t change after the execution of this instruction")
        # print( "As described above, VF is set to 1 if any screen pixels are flipped from set to unset when the sprite is drawn, and to 0 if that doesn’t happen")

        elif foo == 0xE000:
            foo2 = self.opcode & 0x00FF
            if foo2 == 0x009E:  # EX9E
                if self.keyboard[self.v[x]] == 1:
                    self.pc = self.pc + 2
            if foo2 == 0x00A1:  # EXA1
                if self.keyboard[self.v[x]] == 0:
                    self.pc = self.pc + 2

        elif foo == 0xF000:
            foo2 = self.opcode & 0x00FF
            if foo2 == 0x0007:  # FX07
                self.v[x] = self.delay_timer
            elif foo2 == 0x000A:  # FX0A
                key = -1
                for i in range(len(self.keys)):
                    if self.keyboard[i] == 1:
                        key = i
                        break
                if key >= 0:
                    self.v[x] = key
                else:
                    self.pc = self.pc - 2
            elif foo2 == 0x0015:  # FX15
                self.delay_timer = self.v[x]
            # print("Sets the delay timer to VX")
            elif foo2 == 0x0018:  # FX18
                self.sound_timer = self.v[x]
            #  print("Sets the sound timer to VX")
            elif foo2 == 0x001E:  # FX1E
                self.index += self.v[x]
            #  print("Adds VX to I. VF is not affected")
            elif foo2 == 0x0029:  # FX29
                self.index = self.v[x] * 5
            #  print("Sets I to the location of the sprite for the character in VX")
            #  print("Characters 0-F (in hexadecimal) are represented by a 4x5 font")
            elif foo2 == 0x0033:  # FX33
                self.memory[self.index] = self.v[x] // 100
                self.memory[self.index + 1] = (self.v[x] // 10) % 10
                self.memory[self.index + 2] = (self.v[x] % 100) % 10
            elif foo2 == 0x0055:  # FX55
                for n in range(0, x):
                    self.memory[n + self.index] = self.v[n]
            #  print("Stores V0 to VX (including VX) in memory starting at address I")
            # print("The offset from I is increased by 1 for each value written, but I itself is left unmodified")

            elif foo2 == 0x0065:  # FX65
                for ri in range(0, x):
                    self.v[ri] = self.memory[self.index + ri]
            # print("Fills V0 to VX (including VX) with values from memory starting at address")
            # print("The offset from I is increased by 1 for each value written, but I itself is left unmodified")
            else:
                self.pc -= 2
        else:
            print("Unknown Opcode :", hex(self.opcode))

        self.pc += 2

        timer = time()

        if timer - self.last_time >= 1.0 / 60:
            if self.delay_timer > 0:
                self.delay_timer -= 1
            if self.sound_timer > 0:
                beep = pygame.mixer.Sound("sound/electro_beep.mp3")
                beep.play()
                self.sound_timer -= 1
            self.last_time = timer

    def key_events(self, events):
        for event in events:
            event_type = -1
            if event.type == pygame.KEYDOWN:
                event_type = 1
            elif event.type == pygame.KEYUP:
                event_type = 0
            elif event.type == pygame.QUIT:
                print("Quitting...")
                pygame.quit()

            if event_type == 0 or event_type == 1:
                if event.key in self.keys:
                    i = self.keys.index(event.key)
                    self.keyboard[i] = event_type

    def run(self):

        while True:
            self.execute_opcode()
            if self.draw_flag:
                self.draw_on_screen(64, 32)

            events = pygame.event.get()
            self.key_events(events)
