# [Bundle 99]

* **CTF Name:** Bronco CTF 2026
* **Category:** Forensics
* **Difficulty:** 3 Stars
* **Challenge Author:** yoshie878
* **Writeup Author:** Nakata Christian (n4ct) - TCP1P
* **Date:** July 11, 2026

---

## Challenge Description

![Bundle 99 Description](img/bundle-99.png)

---

## 1. Solve Steps

### Step 1: Clue Analysis

We're given a zip file named `Bundle_99`. Unzipping it, we can see several files and folders.

### Step 2: Retrieve the Flag

Since the flag format is `bronco{...}`, I decided to scan all files and subdirectories recursively using `strings` and `exiftool`.

First, I tried checking raw human-readable text inside the binaries using `strings`:
```bash
find . -type f -exec strings {} + | grep -i 'bronco'
```

**Result:** Empty. The standard `strings` command didn't catch anything.

Next, I moved to checking the metadata of all files using `exiftool`:
```bash
find . -type f -print0 | xargs -0 exiftool | grep -i 'bronco'
```

**Result:** And yes, `exiftool` successfully found the flag inside an XML structure.

Flag: `bronco{1m4n4rt15ttru5t}`