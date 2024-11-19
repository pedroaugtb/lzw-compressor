# bitreader.py

class BitReader:
    def __init__(self, file):
        self.file = file
        self.current_byte = 0
        self.bits_remaining = 0

    def read_bits(self, num_bits):
        result = 0
        while num_bits > 0:
            if self.bits_remaining == 0:
                byte = self.file.read(1)
                if not byte:
                    return None  # End of file
                self.current_byte = byte[0]
                self.bits_remaining = 8
            bits_to_read = min(self.bits_remaining, num_bits)
            shift = self.bits_remaining - bits_to_read
            mask = (1 << bits_to_read) - 1
            result = (result << bits_to_read) | ((self.current_byte >> shift) & mask)
            self.bits_remaining -= bits_to_read
            num_bits -= bits_to_read
            self.current_byte &= (1 << self.bits_remaining) - 1  # Mask out the bits we've read
        return result