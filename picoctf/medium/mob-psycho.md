# [Mob psycho]

* **CTF Name:** picoCTF 2024
* **Category:** Forensics, browser_webshell_solvable, apk
* **Difficulty:** Medium
* **Hint:**
    * 1. Did you know you can unzip APK files?
    * 2. Now you have the whole host of shell tools for searching these files
* **Challenge Author:** NGIRIMANA SCHADRACK
* **Writeup Author:** Nakata Christian (n4ctbyte)
* **Date:** January 11, 2026
* **Source:** [Link to Challenge](https://play.picoctf.org/practice/challenge/420?category=4&difficulty=2&page=1&search=)

---

## Challenge Description

![Mob psycho Description](img/mob-psycho.png)

## 1. Executive Summary

**Objective:**
To investigate a provided Android application package (APK), navigate its internal directory structure, and locate a hidden flag file.

**Result:**
The flag was successfully discovered hidden deep within the resource directory of the APK. Despite the presence of a recursive "rabbit hole" involving nested ZIP files (`0.zip`), the flag was found in a static location: `picoCTF{ax8mC0RU6ve_NX85l4ax8mCl_703dd9ef}`.

**Method:**
The investigation utilized APK Decompression, Directory Traversal, and efficient CLI-based file discovery using the `find` command to bypass intentional anti-forensic distractions.

---

## 2. Evidence Identification

This section provides details regarding the initial evidence file.

- **Filename:** `mobpsycho.apk`
- **Size:** `4 MB`
- **SHA-256:** `04af9e10808316c2335608808fe0f490622a681c789f08ba1fce50b32d70fba8`

**Initial Check:**
Verifying file type using signature headers (Magic Bytes).

```bash
$ file mobpsycho.apk  
mobpsycho.apk: Zip archive data, made by v3.0 UNIX, extract using at least v1.0, last modified Mar 12 2024 00:06:36, uncompressed size 0, method=store
```

---

## 3. Investigation Steps

### Step 1: Initial Extraction

Since an APK is essentially a ZIP archive, the investigation began by extracting its contents to a working directory.

**Command:**
```bash
$ binwalk -e mobpsycho.apk
```

### Step 2: Identifying the Recursive "Rabbit Hole"

Initial manual inspection revealed a file named `0.zip`. Upon extracting `0.zip`, another `0.zip` was found inside, suggesting a recursive structure designed to waste time and mislead manual extraction efforts (similar to a Matryoshka doll).

### Step 3: Efficient File Discovery

To bypass the manual traversal of the nested archives, I utilized the `find` command to scan the entire extracted directory structure for any files matching the name "flag".

**Command:**
```bash
$ find . -name "*.txt"
./res/color/flag.txt
./_0.zip.extracted/res/color/flag.txt
./_0.zip.extracted/_0.zip.extracted/res/color/flag.txt
```

**Observation:** The file `flag.txt` was located in `./res/color/`. This is an unusual location for a `.txt` file, as the `res/color` directory in Android typically contains XML color definitions.

### Step 4: Flag Retrieval

I read the contents of the identified `flag.txt` file located in the primary extraction directory.

**Command:**
```bash
$ cat ./res/color/flag.txt
7069636f4354467b6178386d433052553676655f4e5838356c346178386d436c5f37303364643965667d
```

**Decoding Hex to ASCII:** The content was encoded in Hexadecimal. I decoded it directly via the terminal:
```bash
$ echo "7069636f4354467b6178386d433052553676655f4e5838356c346178386d436c5f37303364643965667d" | xxd -r -p
picoCTF{ax8mC0RU6ve_NX85l4ax8mCl_703dd9ef}
```

---

## 4. Conclusion

Mob psycho is a practical exercise in avoiding "rabbit holes" by using efficient tooling. While the challenge attempted to lure the investigator into a recursive extraction loop (Step 2), the use of the `find` utility allowed for immediate identification of the target artifact. It also highlights the importance of checking standard application directories (`res/`) for non-standard file types.