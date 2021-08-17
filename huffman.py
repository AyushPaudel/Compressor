import json


class HeapNode():

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return self.left, self.right


class HuffmanCoding:
    def __init__(self):
        self.path = ""
        self.frequency_dict = {}
        self.code = {}
        self.reverse_map = {}

    def make_frequency_dict(self, string):
        freq = {}
        for c in string:
            if c not in freq:
                freq[c] = 0
            freq[c] += 1
        return sorted(freq.items(), key=lambda x: x[1], reverse=True)

    # merge nodes to create a heap

    def build_heap(self, nodes):
        while len(nodes) > 1:
            (key1, c1) = nodes[-1]
            (key2, c2) = nodes[-2]
            nodes = nodes[:-2]

            node = HeapNode(key2, key1)
            nodes.append((node, c1 + c2))

            nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
        return nodes

    def make_code_tree(self, node, left=True, binString=''):
        if type(node) is str:
            return {node: binString}
        (l, r) = node.children()
        self.code.update(self.make_code_tree(l, True, binString + '0'))
        self.code.update(self.make_code_tree(r, False, binString + '1'))
        self.reverse_map = {y: x for x, y in self.code.items()}

        return self.code

    def get_encoded_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.code[character]

        # print(self.code)
        return encoded_text

    def pad_encoded_text(self, encoded_text):

        extra_padding = 8 - len(encoded_text) % 8

        for i in range(extra_padding):
            encoded_text += "0"
        #
        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def get_byte_array(self, padded_encoded_text):

        if (len(padded_encoded_text) % 8 != 0):
            print("Not padded")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i + 8]
            b.append(int(byte, 2))
        return b

    def encode(self, string):
        self.frequency_dict = self.make_frequency_dict(string)
        heap_node = self.build_heap(self.frequency_dict)
        self.make_code_tree(heap_node[0][0])

    def compress(self, path=None):
        if path is None:
            string = 'datastructures'
            self.encode(string)
            print(' Char | Huffman code')
            for (char, frequency) in self.frequency_dict:
                print(' %-5s|%7s' % (char, self.code[char]))

        else:
            output_path = "compressed" + ".bin"

            with open(path, 'r+') as file, open(output_path, 'wb') as output:
                text = file.read()
                text = text.rstrip()

                self.encode(text)

                encoded_text = self.get_encoded_text(text)
                padded_encoded_text = self.pad_encoded_text(encoded_text)
                b = self.get_byte_array(padded_encoded_text)
                output.write(bytes(b))

            with open("key.json", "w") as key:
                json.dump(self.reverse_map, key)
            print("mapping key at", "key.json")

            return output_path

    """
    Decode
    """

    def remove_padding(self, padded_encoded_text):

        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:]
        encoded_text = padded_encoded_text[:-1 * extra_padding]

        return encoded_text

    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if (current_code in self.reverse_map):
                character = self.reverse_map[current_code]
                decoded_text += character
                current_code = ""

        return decoded_text

    def decompress(self, input_path, reverse_mapping=None):

        if reverse_mapping:
            self.reverse_map = reverse_mapping

        output_path = "decompressed" + ".txt"

        with open(input_path, 'rb') as file, open(output_path, 'w') as output:
            bit_string = ""

            byte = file.read(1)
            while (len(byte) > 0):
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)

            encoded_text = self.remove_padding(bit_string)

            decompressed_text = self.decode_text(encoded_text)

            output.write(decompressed_text)

        print("Decompressed")
        return output_path

# h = HuffmanCoding()
# h.compress()
