# [Operation Oni]

* **CTF Name:** picoCTF 2022
* **Category:** Forensics, disk
* **Difficulty:** Medium
* **Hint:** None
**Challenge Author:** LT 'SYREAL' JONES
* **Writeup Author:** Nakata Christian (n4ctbyte)
* **Date:** January 7, 2026
* **Source:** [Link to Challenge](https://play.picoctf.org/practice/challenge/284?category=4&difficulty=2&page=2)

---

## Challenge Description

![Operation Oni Description](img/operation-oni.png)

## 1. Executive Summary

**Objective:**
To conduct a forensic examination on a provided disk image (`disk.img`), locate valid SSH credentials hidden within the file system, and use them to gain unauthorized access to a remote target server.

**Result:**
The investigation initially uncovered server host keys which proved to be false leads. A deeper analysis of the root user's home directory revealed a valid Ed25519 private key (`id_ed25519`). After reconstructing the key headers and correcting file permissions, I successfully authenticated via SSH and retrieved the flag: `picoCTF{k3y_5l3u7h_af277f77}`.

**Method:**
The investigation employed Disk Forensics (FTK Imager/Mounting), File System Traversal, SSH Key Analysis, and Linux Permission Management.

---

## 2. Evidence Identification

This section provides details regarding the initial evidence file.

- **Filename:** `disk.img`
- **Size:** `230 MB`
- **SHA-256:** `b528d5a0e61278b5520a995b518a213ee20f61d18c6be68825a516fabd2162fc`

**Initial Check:**
Verifying file type using signature headers (Magic Bytes).

```bash
$ file disk.img
disk.img: DOS/MBR boot sector; partition 1 : ID=0x83, active, start-CHS (0x0,32,33), end-CHS (0xc,223,19), startsector 2048, 204800 sectors; partition 2 : ID=0x83, start-CHS (0xc,223,20), end-CHS (0x1d,81,52), startsector 206848, 264192 sectors
```

---

## 3. Investigation Steps

### Step 1: Disk Forensics & Structure Analysis

The investigation began by mounting the `disk.img` image (using `FTK Imager` or mount loopback). The disk contained two main Linux partitions. I focused my search on the second partition (`Partition 2`), which appeared to contain the root file system.

### Step 2: The "Host Key" Red Herring

My initial search pattern targeted the standard SSH configuration directory: `/etc/ssh/`. I located a file named `ssh_host_rsa_key` containing a private key block.

**Observation:**
```plaintext
/etc/ssh/ssh_host_rsa_key
/etc/ssh/ssh_host_ed25519_key
```
Attempting to use these keys resulted in failure. 

**Analysis:** These are Host Keys, used by the server to identify itself to clients, not User Keys used for authentication. This was a deliberate distractor placed in a common location.

### Step 3: Locating the True Credential

Redirecting the search to user home directories, I examined `/root/` (the home directory of the superuser). Inside `/root/.ssh/`, I discovered a specific key pair:
- `id_ed25519` (Private Key)
- `id_ed25519.pub` (Public Key)

**Path:** `Partition 2 > root > .ssh > id_ed25519`

### Step 4: Key Reconstruction and Permission Hardening

The raw content extracted from the image was a raw base64 block without standard OpenSSH headers. To make it usable, I had to reconstruct the PEM format:

```plaintext
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACBgrXe4bKNhOzkCLWOmk4zDMimW9RVZngX51Y8h3BmKLAAAAJgxpYKDMaWC
... [REDACTED] ...
KZb1FVmeBfnVjyHcGYosAAAADnJvb3RAbG9jYWxob3N0AQIDBAUGBw==
-----END OPENSSH PRIVATE KEY-----
```

I saved this to a file named `oni_key`. Before initiating the connection, I had to secure the key file. SSH clients reject private keys with open permissions (0644 or 0777).

```bash
$ chmod 600 oni_key
```

### Step 5: Unauthorized Access and Exfiltration

With the sanitized key, I initiated a connection to the challenge instance. Although the key was found in the `/root/` directory, the challenge instructions specified the user `ctf-player`.

```bash
$ ssh -i oni_key -p 55820 ctf-player@saturn.picoctf.net
```

**Result:** The connection was established successfully.

```bash
ctf-player@challenge:~$ ls
flag.txt
ctf-player@challenge:~$ cat flag.txt
picoCTF{k3y_5l3u7h_af277f77}
```

---

## 4. Conclusion

Operation Oni serves as a practical lesson in distinguishing between SSH Host Keys and User Keys.

1. **Forensic Artifacts:** The presence of keys in `/etc/ssh/` is standard for server config but irrelevant for client authentication.

2. **Privilege Level:** In forensic scenarios, checking the root user's artifacts (`/root/`) is often as critical as checking standard user directories.

3. **Operational Security:** The challenge reinforced the importance of correct file permissions (`chmod 600`) for sensitive credentials, without which the extracted data is unusable.