## [COURSE: CSC 230] [SOURCE: Discord] [DATE: Spring 2023]

---
**Thread** 2023-04-19
> **lunatic.2002:** Hey can someone please explain big O notation and functions? I understand that fx needs to be less than c g(x) but when I graph some of these on Desmos, some of the functions end up being greater than fx even tho it was less than cgx for a bit.
  → **Zach:** O-notation is a way of signifying the relative amount of time an algorithm takes to complete given the worst-case scenario. An algorithm that will consistently complete in the same amount of time, regardless of the input, would be considered O(1). An algorithm where the number of steps is relative to the number of entries, *n*, would have a worst-case scenario O(n). This means that in the worst possible outcome, it will take some number of steps multiplied by the number of entries *n* to complete.
  → **Zach:** Example of O(1): a function like fizzbuzz that checks a single value and prints — always the same number of steps regardless of input.
  → **Zach:** O(n): a function that loops through an array once (e.g., printing every element) — the number of steps scales linearly with n.
  → **Zach:** O(n^2): a nested loop over an array — for every value of n, you run through n steps again, so n x n = n^2.
  → **Zach:** Important: we do not consider constants. O(2n^2) simplifies to O(n^2). O((n^2)/2) -> O(n^2). O(n^2 + n) -> O(n^2). O(n^3 + n^2) -> O(n^3). Also: O(10000) -> O(1), O(100000n) -> O(n).
---

---
**Thread** 2024-09-07
> **Kunj Shah:** Any Prof. Jacobson student here??
  → **Charley CycoNerd:** I'm in his class.
---

---
**Thread** 2025-05-06
> **Charley CycoNerd:** For CSC 230, if you are comfortable working in Python, I strongly recommend taking Jonathan Jacobson. He will go above and beyond to make himself available overtime for ensuring you learn the topics. It's a hands-on class, and you will have projects to work on. These projects will have to be done in Python on Google Colab.
  → **leavism:** URGH YES 100/10 stars for Jacobson
---
