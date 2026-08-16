# [Acrostic]

* **CTF Name:** 0xV01D CTF 2026 v2
* **Category:** Misc
* **Difficulty:** 250 points
* **Writeup Author:** Nakata Christian (n4ct) - TCP1P
* **Date:** August 15, 2026

---

## Challenge Description

```
This challenge allows only 1 flag attempt. Submit only when you are sure.
A mysterious message was intercepted from the network. Something is hidden in plain sight.
Read carefully — the first letter of each line reveals the secret.
Flag format : 0xV0ID{......}
```

---

## 1. Solve Steps

### Step 1: Clue Analysis

We're given a long poem-like text.

```
Forgotten echoes drift through the network at midnight.
Invisibly, packets cross the wire unseen.
Routing tables shift and reshape the data paths.
Silence fills the void between each transmission.
Time stamps record every byte that passes.
Signals propagate at the speed of light.
Topology defines how nodes find each other.
Encryption wraps the payload in darkness.
Persistence is the key to every challenge. 
```

This one is easy. From the challenge's description `Read carefully — the first letter of each line reveals the secret.`, we know that we have to pay attention to the first letter of each line which spell out `FIRSTSTEP`. Well, even the challenge's title already gave it away. Acrostic is a poem or piece of writing in which specific letters in each line, most commonly the first letter, if read downward will spell out a hidden word.

Flag: `0xV0ID{FIRSTSTEP}`