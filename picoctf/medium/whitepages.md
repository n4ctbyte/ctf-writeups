# [WhitePages]

- **CTF Name:** picoCTF 2019
- **Category:** Forensics
- **Difficulty:** Medium
- **Hint:** There is data encoded somewhere... there might be an online decoder.
- **Challenge Author:** JOHN HAMMOND
- **Writeup Author:** Nakata Christian (n4ctbyte)
- **Date:** January 12, 2026
- **Source:** [Link to Challenge](https://play.picoctf.org/practice/challenge/51?category=4&difficulty=2&page=4&search=)

---

## Challenge Description

![WhitePages Description](img/whitepages.png)

## 1. Executive Summary

**Objective:**
To investigate a text file that appears to be empty and recover a hidden flag by analyzing non-printable characters and decoding them from a binary format.

**Result:**
The investigation identified a "Whitespace Steganography" technique. By mapping two distinct Unicode/ASCII space characters to binary bits (0 and 1), the hidden message was successfully decoded: `picoCTF{not_all_spaces_are_created_equal_bbc4f54c75763bd78dc840f05eb7a752}`.

**Method:**
The method involved Hexadecimal Analysis (`xxd`), Pattern Recognition, and Custom Python Scripting to automate the binary-to-ASCII conversion.

---

## 2. Evidence Identification

This section provides details regarding the initial evidence file.

- **Filename:** `whitepages.txt`
- **Size:** `2.7 KB`
- **SHA-256:** `fa8b6d303e49bc5ff3ef90478e2a7c5d0ad9aac2e1ff72d4bdfd5b17d80f1bf8`

**Initial Check:**
Verifying file type using signature headers (Magic Bytes).

```bash
$ file whitepages.txt
whitepages.txt: Unicode text, UTF-8 text, with very long lines (1296), with no line terminators
```

---

## 3. Investigation Steps

### Step 1: Hexadecimal Analysis

Since the file was not empty but displayed no text, I inspected the raw bytes using a Hex Editor to identify non-printable characters.

**Command:**

```bash
$ xxd whitepages.txt | head
00000000: e280 83e2 8083 e280 83e2 8083 20e2 8083  ............ ...
00000010: 20e2 8083 e280 8320 2020 e280 83e2 8083   ......   ......
00000020: e280 83e2 8083 e280 8320 20e2 8083 20e2  .........  ... .
00000030: 8083 e280 8320 e280 8320 20e2 8083 e280  ..... ...  .....
00000040: 83e2 8083 2020 e280 8320 20e2 8083 2020  ....  ...  ...
00000050: 2020 e280 8320 e280 83e2 8083 e280 83e2    ... ..........
00000060: 8083 2020 e280 8320 e280 8320 e280 8320  ..  ... ... ...
00000070: e280 83e2 8083 e280 8320 e280 83e2 8083  ......... ......
00000080: e280 8320 20e2 8083 e280 83e2 8083 e280  ...  ...........
00000090: 83e2 8083 20e2 8083 20e2 8083 e280 83e2  .... ... .......
```

**Discovery:** Two repeating patterns were identified:

1. `e2 80 83` (Unicode: En Space)
2. `20` (ASCII: Regular Space)

### Step 2: Binary Deduction

The presence of exactly two repeating patterns strongly suggested a Binary Encoding scheme. In this scenario:

- `e2 80 83` represents bit `1`
- `20` represents bit `0`

**Note:** If the initial decoding fails, the polarity is likely reversed.

### Step 3: Automated Decoding

To handle the 15 KB of data, I developed a Python script to automate the replacement and conversion process.

**Script:**

```python
with open("whitepages.txt", "rb") as f:
    data = f.read()

binary_str = data.replace(b'\xe2\x80\x83', b'1').replace(b' ', b'0')

flag = ""
for i in range(0, len(binary_str), 8):
    byte = binary_str[i:i+8]
    if len(byte) == 8:
        flag += chr(int(byte, 2))

print(flag.strip())
```

**Command:**

```python
$ python3 solve.py
picoCTF

SEE PUBLIC RECORDS & BACKGROUND REPORT
5000 Forbes Ave, Pittsburgh, PA 15213
picoCTF{not_all_spaces_are_created_equal_bbc4f54c75763bd78dc840f05eb7a752}
```

---

## 4. Conclusion

This challenge demonstrates that files appearing empty can contain significant amounts of information hidden in the "negative space" of the document. Standard forensic procedures, starting from raw byte analysis (Hex), are essential when high-level tools (like `cat` or text editors) fail to render data.
