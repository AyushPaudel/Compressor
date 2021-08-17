from time import sleep
import json
import os

import tkinter as tk
from tkinter import filedialog

from huffman import HuffmanCoding


def open_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename()


def compress_file():
    print("Open .txt file")
    sleep(1)
    path = open_file()

    h = HuffmanCoding()

    output_path = h.compress(path)
    print("Compressed file path: " + output_path)


def decompress_file():
    print("Open .bin or")
    sleep(1)

    try:
        with open("key.json", "r") as key:
            data = key.read()
    except FileNotFoundError:
        print("No key found to map the code")
        exit()
    reverse_mapping = json.loads(data)

    path = open_file()
    h = HuffmanCoding()
    decom_path = h.decompress(path, reverse_mapping)
    print("Decompressed file path: " + decom_path)


def choose_own_file():
    print("Welcome, press 1 to compress a file and 2 to decompress a file, or anything else to exit")
    try:
        a = int(input())
        if a == 1:
            compress_file()
        elif a == 2:
            decompress_file()
        else:
            exit()
    except ValueError:
        exit()


def compress_decompress():
    path = "sample.txt"

    h = HuffmanCoding()

    output_path = h.compress(path)
    print("Compressed file is: " + output_path)

    decom_path = h.decompress(output_path)
    print("Decompressed file is: " + decom_path)


def check_file_size():
    original_size = os.path.getsize("sample.txt")
    compressed_size = os.path.getsize("compressed.bin")
    decompressed_size = os.path.getsize("decompressed.txt")
    print(f'Original size:{original_size} > compressed size:{compressed_size} {original_size > compressed_size}')
    print(
        f'Original size:{original_size} == decompressed size:{decompressed_size} {original_size == decompressed_size}')


compress_decompress()
# choose_own_file()
check_file_size()
