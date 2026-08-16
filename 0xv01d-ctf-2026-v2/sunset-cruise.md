# [Sunset Cruise]

* **CTF Name:** 0xV01D CTF 2026 v2
* **Category:** OSINT
* **Difficulty:** 415 points
* **Writeup Author:** Nakata Christian (n4ct) - TCP1P
* **Date:** August 16, 2026

---

## Challenge Description

![Sunset Cruise Description](img/sunset-cruise.png)

---

## 1. Solve Steps

### Step 1: Clue Analysis

We're given an image taken from a boat, showing a waterfront building along the coast.

![Sunset Cruise Clue Image](img/sunset-cruise-cruise.jpeg)

### Step 2: Identifying the Building

To identify the building, I cropped it from the image and searched it on Google Images. The results identified the building as `Edip Efendi Yalısı`, located on the Asian shore of the Bosphorus in Istanbul, Turkey.

![Sunset Cruise Google Images Result](img/sunset-cruise-google-image.png)

Here is the verified location on Google Maps:

![Sunset Cruise Google Maps](img/sunset-cruise-google-maps.png)

### Step 3: The 3 Words

To obtain the 3 words for `Edip Efendi Yalısı`, I used a website called `what3words.com` and got the words: `cosmetic.suppers.agenda`.

![Sunset Cruise 3 Words](img/sunset-cruise-3-words.png)

Flag: `0xV01D{Turkey_Istanbul_cosmetic.suppers.agenda}`