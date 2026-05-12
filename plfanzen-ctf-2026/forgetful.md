# [forgetful]

* **CTF Name:** plfanzenctf 2026
* **Category:** Cryptography
* **Hint:** i keep forgettign my mdouli
* **Challenge Author:** emxl
* **Writeup Author:** Nakata Christian (n4ct)
* **Date:** May 9, 2026

---

## Challenge Description

![forgetful Description](img/forgetful.png)

## 1. Executive Summary

**Objective:**
To decrypt the ciphertext of an RSA-encrypted flag where the author carelessly leaked a massive multiple of the Euler's Totient function ($\phi$) and reused the vulnerable modulus to generate a new one.

**Result:**
The challenge featured a classic textbook RSA vulnerability often referred to as "Known Key Leakage" or the "Equivalence of Factoring and Computing $d$". By exploiting the leaked variable $f$, I was able to implement a probabilistic root-finding algorithm to factor the first modulus ($n_1$) into its prime components ($p$ and $q$). After trivially extracting the third prime ($r$) from the second modulus ($n_2$), I recalculated the valid private key and decrypted the flag. 

**Method:**
The approach involved analyzing the relationship between the public exponent $e$, private exponent $d$, and the leaked variable $f$. Recognizing that $f$ was a mathematical multiple of $\phi(n_1)$, I used a custom Python script to factor $n_1$. I then isolated $r$ by dividing $n_2$ by $n_1$, reconstructed the full $\phi(n_2)$, and successfully inverted $e$ to find the final decryption key.

---

## 2. Evidence Identification

Target files provided by the organizers:

- **Filename:** `chall.py` (The challenge source code detailing the flawed RSA implementation)
- **Filename:** `output.txt` (The generated parameters containing $n_1$, $n_2$, $e$, $f$, and the ciphertext $y$)

---

## 3. Investigation Steps

### Step 1: Initial Thought & Reading the Source

Diving into `chall.py`, the setup looked like a standard RSA encryption script at first glance. The author generates two 1024-bit primes, $p$ and $q$, and calculates the first modulus $n_1$. They also calculate the private key $d$ based on $e = 65537$. 

But then, the script does something incredibly weird and noisy:

```python
d = pow(e, -1, φ)
f = (e * d - 1) * randint(1<<2047, 1<<2048)
print(f'{f = }')
```
After doing this, the author "forgets" what they were doing, generates a third prime $r$, and creates a new modulus $n_2 = n_1 \times r$. They encrypt the flag using this new $n_2$ and give us the ciphertext $y$. We are handed $n_1$, $n_2$, $e$, $f$, and $y$ in `output.txt`. 

### Step 2: Unmasking the Variable 'f'

Let's talk math. In textbook RSA, the fundamental relationship between the public exponent $e$ and the private exponent $d$ is defined over the Euler's Totient function of the modulus, $\phi(n)$. 

The core rule is:
$$e \cdot d \equiv 1 \pmod{\phi(n)}$$

This congruence strictly means that $(e \cdot d - 1)$ is an exact multiple of $\phi(n)$. In other words, there exists some integer $k$ such that $e \cdot d - 1 = k \cdot \phi(n)$. 

Now, look at how $f$ is constructed in the challenge:
$$f = (e \cdot d - 1) \times \text{randint}(1\ll2047, 1\ll2048)$$

Even though the author tried to obfuscate $(e \cdot d - 1)$ by multiplying it by a giant random number, it doesn't change the mathematical fact: **$f$ is still a multiple of $\phi(n_1)$**. In cryptography, leaking any multiple of the totient is a fatal flaw because it gives attackers a direct pathway to factor the modulus. 

### Step 3: The Probabilistic Factoring Oracle

When analyzing the variable $f$, the most naive approach that comes to mind is attempting to divide $f$ to isolate the exact $\phi(n_1)$. However, noticing the massive 2048-bit random multiplier (`randint(1<<2047, 1<<2048)`), I immediately deduced that exact extraction was a mathematical dead-end intended to waste time. Because of this, I bypassed direct extraction entirely. I chose to use the Probabilistic Factoring Algorithm because it dynamically accepts any multiple of $\phi(n_1)$ as an oracle, rendering the author's random multiplier completely useless.

Knowing that $f = k \cdot \phi(n_1)$, we can use a well-known probabilistic algorithm to factor $n_1$. The logic relies on the properties of the multiplicative group modulo $n_1$. 

By Euler's Theorem, for any base $a$ coprime to $n_1$:
$$a^{\phi(n_1)} \equiv 1 \pmod{n_1}$$

Since $f$ is a multiple of $\phi(n_1)$, it is also true that:
$$a^f \equiv 1 \pmod{n_1}$$

The algorithm works by repeatedly taking square roots of $a^f \pmod{n_1}$. We express $f$ as $f = t \cdot 2^s$ (where $t$ is odd). We pick a random base $a$, compute $x = a^t \pmod{n_1}$, and repeatedly square it. We are looking for a non-trivial square root of 1 (a number $x$ where $x \neq 1$ and $x \neq n_1 - 1$, but $x^2 \equiv 1 \pmod{n_1}$). Once we find this non-trivial root, we can instantly find one of the prime factors by calculating the Greatest Common Divisor (GCD):
$$p = \text{gcd}(x - 1, n_1)$$

This algorithm is extremely fast. I didn't need to guess the random multiplier generated by the `randint`; the math just bypasses it entirely.

### Step 4: Connecting the Moduli

Once my script factored $n_1$ and spit out $p$ and $q$, the rest of the challenge completely fell apart. 

The author generated the second modulus by simply multiplying the first one by a new prime: 
$$n_2 = n_1 \times r$$

Since both $n_1$ and $n_2$ are given in `output.txt`, extracting $r$ is hilariously trivial. No crypto-magic needed here, just elementary school division:
$$r = \frac{n_2}{n_1}$$

### Step 5: Crafting the Final Exploit

With $p$, $q$, and $r$ in hand, I had complete control over the second modulus $n_2$. To decrypt the flag, I needed the new private key $d_2$. 

First, calculate the totient for $n_2$:
$$\phi(n_2) = (p - 1) \cdot (q - 1) \cdot (r - 1)$$

Then, calculate the modular inverse of $e$ over $\phi(n_2)$ to get the actual private key:
$$d_2 \equiv e^{-1} \pmod{\phi(n_2)}$$

Finally, apply the textbook RSA decryption routine on the ciphertext $y$:
$$m = y^{d_2} \pmod{n_2}$$

I wrote a Python script utilizing `pycryptodome` to handle the large integers and execute the probabilistic factorization. After running it, the script successfully extracted $p$, $q$, and $r$, calculated $d_2$, and printed out the decoded bytes, giving me the flag.

**Solver Script:**
```python
import random
from math import gcd
from Crypto.Util.number import long_to_bytes, inverse

# data from output.txt
n1 = 26163135579688365685749815087329013334321121413643522908978368498735100170979534541718203679850082229787759782839681447559164002210869244500540973862856530598392079268634690330070660954034487592074822325850001910182733807095603564736824910742913113289353912516772790184315838420981130270105651186663870881112836678617131337228434051865326335706482708472706460968524237228926484467949566760384706104911056831538533624528670958485196083590036887610756195981479779202661715287328581372726755736493677063580937937266428951007545922455280143685478422497559640922154682744408643083289846851666246679455798110179318405230931
e = 65537
f = 16619390725406635003568704852041911383955112212003240311342104383864759018695752174792104916686338541054342162609171143958134395731427150364372793173747880920137583990341341227291324539508796021865961464369193544132215022658230178860234791766090107941114287607741074843606904794703901411480225844724713596907693681841046073301889715371806982838530018343173875170873522014193380732851547012574855474908668296483104554386695539355932942245744809166324853267643767579216887208285303085135015815536424052951160199582501759864869389195414975668274178099398177595497814766952786710419583062743876116182639815677393654265216006656000329955779142657774012939903613439634900756309488788122180358247113778689757033990808260318315953460320952689775164494488647339215735270522827001658979078965173654286080229344600296846537691065606393856754774657799846581490089559198081343375609135990178877583801388625349032186444905843627094118220522630500025852277112348471906984265139377439682886342233965872410799647143624708691650589737696646061463804793253780815810379511117350924120083782790018656800072336505688406241117202425315513946334946991380012284298375994956942535844596390726997538376786444638010597206874426880844883185479294521633421276121268768

n2 = 3744676117380018641668565892400060597598102470869192632857690015295815332161644283341780564613457727737562575645824862653471082863831534974662000525091534997986639499609449665365105050920311980582790572642499182946943026269663375062221835741115900079031838565458474495719991625318219870536519462982162951828191511514447259543635866241177847950837537712532728716975126901558406841638815830827656710855510973350720103540120744403947297634321526646725912126780073606947982441103861991837449443740084526521291253031492077715755095432408404163246177412993252662886723266628703833691002677999001876718711604867226639547529543827309052093869197820219041816125907880168206543866865164216068062134474378825555094557812068745099180548317070882943384931781265097214746098507801167905339988776032032233040684414513107134913863424395154608233362935114768752610665839261294654641442581859119417973864057668647702371544195390852813023274711
y = 1192454268596034783703987997857184539013560456905463534487934990789408259132529888179478327838308152408943511172223310911818318055745959076310610194100238815440973302194697484135449956281295204464442680433043033759430472212878255906073617635580740550219377442291318685319833582696685232012541093524313783191058062111027418420793730056721723709479566394061449799608119051227936939761422225674533439968552715317418348088821375961321742539426835616694011309468598514877264149427576676110165168173944300681607038995442234802353307996182447235054172477369472489440539191331218712223299530245178428464525243995786877882355119878260523642758027365324100610326845431800025723076748075327424051479302838364321169409793214255253892577570009288096441537063618930433989891046882222086182614969142633023121163421902185799866071021152639815742960060495904963119622025949778733803721613489040116957109749734422528642444316292207295272860462

r = n2 // n1
assert n1 * r == n2, "r division failed"
print(f"r secured")

def factor_n_with_phi_multiple(n, k_phi):
    t = k_phi
    s = 0
    while t % 2 == 0:
        s += 1
        t //= 2
    
    while True:
        a = random.randint(2, n - 2)
        x = pow(a, t, n)
        if x == 1 or x == n - 1:
            continue
            
        for _ in range(s - 1):
            x_new = pow(x, 2, n)
            if x_new == 1:
                p = gcd(x - 1, n)
                return p, n // p
            if x_new == n - 1:
                break
            x = x_new
        else:
            x_new = pow(x, 2, n)
            if x_new == 1:
                p = gcd(x - 1, n)
                return p, n // p

print("Factoring n1..")
p, q = factor_n_with_phi_multiple(n1, f)
assert p * q == n1, "Factorization failed"
print(f"p and q secured")

phi_2 = (p - 1) * (q - 1) * (r - 1)

d = inverse(e, phi_2)
m = pow(y, d, n2)

flag = long_to_bytes(m)
print("\nFlag:")
print(flag.decode(errors='ignore'))
```

**Output:**
```bash
─$ python3 a.py
r secured
Factoring n1..
p and q secured

Flag:
plfanzen{i_f0rg0r_t0_g3n3r4t3_4_n3w_p_bca22d14a9}
```

---

## 4. Conclusion

This challenge is a brilliant playground for understanding the true fragility of RSA when mathematical parameters are handled carelessly. It proves the fundamental cryptographic theorem: computing the private key $d$ and factoring the modulus $n$ are computationally equivalent problems. 

The author tried to hide the $\phi(n_1)$ leak behind a massive random integer, but in the realm of modular arithmetic and group theory, a multiple of $\phi$ is still a multiple of $\phi$. It’s like trying to hide a glowing beacon by putting a transparent box over it. A fun, straight to the point crypto challenge that perfectly tests core knowledge without relying on tedious guessing!