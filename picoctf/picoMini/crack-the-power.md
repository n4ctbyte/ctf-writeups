# [Crack the Power]

* **CTF Name:** picoMini by CMU-Africa
* **Category:** Cryptography
* **Difficulty:** Medium
* **Hint:**
    * When certain values in the encryption setup are smaller than usual, it opens up unexpected shortcuts to recover the plaintext.
    * Consider whether you can invert the encryption without factoring n.
    * Read more about Coppersmith's_attack [here](https://en.wikipedia.org/wiki/Coppersmith's_attack).
* **Challenge Author:** YAHAYA MEDDY
* **Writeup Author:** Nakata Christian (n4ctbyte)
* **Date:** March 7, 2026
* **Source:** [Link to Challenge](https://play.picoctf.org/practice/challenge/522?category=2&difficulty=2&page=1)

---

## Challenge Description

![Crack the Power Description](../img/crack-the-power.png)

## 1. Executive Summary

**Objective:**
To recover the plaintext message from an RSA-encrypted ciphertext where the public exponent (e) is small and the message (m) is relatively short, causing the modular reduction to be bypassed.

**Result:**
The investigation identified that the ciphertext (c) was smaller than the modulus (n), indicating that `m^e` < `n`. By performing an integer 20 root operation on the ciphertext, the original message was successfully recovered: `picoCTF{t1ny_e_ee65653a}`.

**Method:**
The methodology involved parameter analysis (e vs n), numerical comparison (c vs n), and high precision root extraction using the `gmpy2` library to avoid floating point errors.

---

## 2. Evidence Identification

This section provides details regarding the initial evidence file.

- **Filename:** `message.txt`
- **Size:** `2.4 KB`
- **SHA-256:** `a2f4abc8a6600410a9525424029cf859c5b391e00f79a10585489ca27d9330cb`

**Initial Check:**
Verifying file type using signature headers (Magic Bytes).

```bash
$ file message.txt
message.txt: ASCII text, with very long lines (1237)
```

---

## 3. Investigation Steps

### Step 1: Identifying the "Invisible Modulo" Vulnerability

In standard RSA, the encryption formula is c≡me(modn). However, if `m^e` < `n`, the modulo operator has no effect on the result because if `n` = `100` and `x` = `50`, then `50 (mod 100)` is still `50`. After analyzing the parameters in message.txt, I identified that:

* **Modulus (n):** A massive 1233-digit integer (approximately 4092 bits).
* **Ciphertext (c):** A 1149-digit integer.
* **Exponent (e):** 20

By comparing these values, it is evident that c is significantly smaller than n. This confirms that the equation simplifies to a basic power operation `c = m^e`. Given this condition, it is highly probable that the original message `m` was never wrapped around the modulus.

### Step 2: Mathematical Derivation

To reverse the encryption, we can simply apply the inverse power (root) without needing the private key (d) or factoring n: `m = root e of c`. Since e = 20, we need to find the 20th integer root of c.

### Step 3: Implementing High Precision Decryption

Standard floating point math in Python (`c**(1/20)`) would fail due to precision limits on such a massive integer. I used the `gmpy2` library for exact integer root calculation.

**Solver Script:**
```python
import gmpy2

c = 64063743081040685750056670209627408417063999094079642745278953058264655950335199408463064281952951291663884605487699712549861067275986054704451302618915590178794848448240336292710162627268783368733897527458680647677352131905115256
e = 20

m, exact = gmpy2.iroot(c, e)
flag = bytes.fromhex(hex(m)[2:]).decode()
print(f"Flag: {flag}")
```

### Step 4: Flag Recovery

Upon execution, the script calculated the integer root and converted the resulting large integer into its ASCII representation.

**Terminal Output:**
```plaintext
$ python3 a.py
Flag: picoCTF{t1ny_e_ee65653a}
```

---

## 4. Conclusion

This challenge demonstrates a critical implementation flaw: Lack of Padding.

1. **Deterministic Risk:** Without a padding scheme like OAEP (Optimal Asymmetric Encryption Padding), small messages remain small even after exponentiation.

2. **Root Vulnerability:** If `m^e` < `n`, RSA loses its one-way function property and becomes a simple problem.