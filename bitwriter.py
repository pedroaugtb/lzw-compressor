# bitwriter.py

class BitWriter:
    def __init__(self, file):
        self.file = file
        self.current_byte = 0
        self.bits_filled = 0

    def write_bits(self, bits, num_bits):
        while num_bits > 0:
            remaining_bits_in_byte = 8 - self.bits_filled
            bits_to_write = min(remaining_bits_in_byte, num_bits)
            shifted_bits = (bits >> (num_bits - bits_to_write)) & ((1 << bits_to_write) - 1)
            self.current_byte = (self.current_byte << bits_to_write) | shifted_bits
            self.bits_filled += bits_to_write
            num_bits -= bits_to_write
            if self.bits_filled == 8:
                self.file.write(bytes([self.current_byte]))
                self.current_byte = 0
                self.bits_filled = 0

    def flush(self):
        if self.bits_filled > 0:
            self.current_byte = self.current_byte << (8 - self.bits_filled)
            self.file.write(bytes([self.current_byte]))
            self.current_byte = 0
            self.bits_filled = 0