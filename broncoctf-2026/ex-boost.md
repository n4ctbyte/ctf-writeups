# [EX-BOOST]

* **CTF Name:** Bronco CTF 2026
* **Category:** Forensics
* **Difficulty:** 2 Stars
* **Challenge Author:** blunderous_wonders
* **Writeup Author:** Nakata Christian (n4ct) - TCP1P
* **Date:** July 12, 2026

---

## Challenge Description

![EX-BOOST Description](img/ex-boost.png)

---

## 1. Solve Steps

### Step 1: Initial Analysis

We're given 3 images: `Tiger.png`, `Snake.png`, and `Crane.png`.

![Tiger](img/ex-boost-tiger.png)

![Snake](img/ex-boost-snake.png)

![Crane](img/ex-boost-crane.png)

The challenge description stated `I much prefer the RGB trifecta`, so I thought maybe the flag is hiding in the bit planes. So I used `Aperi Solve` to see the bit planes.

### Step 2: Aperi Solve and the Flag

By uploading the images to Aperi Solve, we can extract the flag part by part.

**Tiger.png (Flag Part 1):**

![Flag 1](img/ex-boost-flag1.png)

`F33L`

**Snake.png (Flag Part 2):**

![Flag 2](img/ex-boost-flag2.png)

`TH3`

**Crane.png (Flag Part 3):**

![Flag 3](img/ex-boost-flag3.png)

`H34T`

Flag: `bronco{F33LTH3H34T}`