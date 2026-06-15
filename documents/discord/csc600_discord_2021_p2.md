## [COURSE: CSC 600] [SOURCE: Discord] [DATE: Spring 2021]

---
**Thread** [2021-02-27]
> **Biubiubiu**: yes, it seems like we need to [pass the array as a pointer], and I've been stuck in this pointer/reference thingy for two days
  → **Biubiubiu**: like if we pass in the array as a pointer, whatever is done in the method may not affect the actual array, but if we pass by reference it might
  → **Danish.CS()**: Yea that's sort of confusing for me too since it's been a while coding in C++ But if you pass the array as pointer, then you could work with the elements
  → **Danish.CS()**: But the thing is if we see his email, he said the function declaration should look like void reduce(int a[], int&n) — so it looks like we should pass the size n as reference
  → **Biubiubiu**: well we're passing the size as reference so it can be changed easily, but I think void reduce(int a[], int &n) means pass the array as a pointer
  → **Biubiubiu**: since there's no way to make an entire copy of the array
  → **Danish.CS()**: that's true since we don't have the option to return the new array with void
  → **Biubiubiu**: what I've learnt about resizing array is to make a temp array to store the new elements -> delete the orig arr (pointer) -> re-point the orig arr pointer to the new arr pointer
  → **Danish.CS()**: that's exactly how I was going to do it — copy elements to new array and delete the original one. Then display the correct sized array
  → **Danish.CS()**: that's the thing, he probably wants us to modify the original array in the reduce function
  → **Biubiubiu**: we could try to pass the array in as reference, or pointer to pointer
  → **Biubiubiu**: but I'm not sure if that is allowed
---

---
**Thread** [2021-02-27]
> **dlau**: By default, arrays in C++ are passed in as a pointer by value
  → **dlau**: You're going to need to create a temp array to hold your reduced array then reassign each element in your original array with the value in the temp reduced array
---

---
**Thread** [2021-02-28]
> **Naweeda**: I defined N to 50000, and K to 1000
  → **Naweeda**: I also did the sec() function what he gave us but when I emailed him, he said it is wrong
  → **Naweeda**: I am very confused about this sec() function
  → **dlau**: This is wrong? That's what I got from the pdf as well. I'll email him as well
  → **Biubiubiu**: I don't think the error should be printed
  → **Biubiubiu**: my K is 50,000 and N is 100,000 (for what he meant by 'significantly bigger' than the example, but this is a bad idea) — I ended up using 200-300 seconds in release mode and 500-600 seconds in debug mode
  → **dlau**: You're right. I fixed the error logs
---

---
**Thread** [2021-03-01]
> **punjibi**: anyone using this code from the Class Reader to find the three largest diff values but are not getting the correct results?
  → **punjibi**: I get that the hw value a=(9,1,1,6,7,1,2,3,3,5,6,6,6,6,7,9) gives 9, 9, 7 but I was expecting 9, 6, 7. I might just be overlooking something?
  → **dlau**: Check your last else if — I think you have it reversed
  → **dlau**: Try `else if (array[i] > first) third = array[i];`
  → **Mabas**: I added an additional check to make sure the digit wasn't already in the top 3
  → **Mabas**: So for example: `else if (array[i] > third && array[i] != first && array[i] != second) third = array[i]`
---

---
**Thread** [2021-03-01]
> **Danish.CS()**: Is anyone using xcode for doing this hw? If so, did you build a new scheme for release mode? How would we change the default debug to release mode?
  → **dlau**: Not sure about xcode, but you need to somehow configure your c++ compile command
  → **dlau**: I just used `g++ -O3`
  → **Danish.CS()**: Are we supposed to make everything inline to improve performance?
---

---
**Thread** [2021-03-01]
> **dlau**: I set my n to 1000000 and k to 100000. It's taking forever to run...
  → **dlau**: Oh shit my computer is overheating
  → **Miggy**: I've spent more time wrestling with WSL than I have programming
  → **Miggy**: Should have just done this project on my macbook
---

---
**Thread** [2021-03-01]
> **punjibi**: Wait, we are only doing times for #4 right?
  → **dlau**: Yes — I didn't see anything about timing execution for each problem
  → **Miggy**: if the grader marks us down for not doing time for 1 and 3 we will group email to complain lol
  → **dlau**: What were your answers for why recursion is faster than iterative for release mode?
---

---
**Thread** [2021-03-01]
> **Ayatollah Epstein**: yo anyone got the pdf book for 600? just curious
  → **dlau**: Yes. Prof. Jozo has one! If you ask nicely, he might just give it to you
  → **dlau**: I tried looking for one myself. I didn't find anything, so I just ended up buying the reader
---

---
**Thread** [2021-03-03]
> **Danish.CS()**: Do we have to submit the exam or is it automatically saved?
  → **ramy1951**: it automatically gets saved but you have to hit the submit button at the end to make it look submitted
  → **rinaykumar**: Do we have to join the zoom meeting or just take the exam?
  → **ramy1951**: No zoom — all questions are over email
  → **LuongDang**: i thought end-time is 12:25 but apparently there also is a time limit
  → **ramy1951**: it auto saves but doesn't submit for you
  → **Danish.CS()**: i mean it ended in 70 minutes, even our class time is 75
  → **Naweeda**: I wasn't able to click submit — it ran out of time
  → **Danish.CS()**: it auto saved your answers so don't worry
  → **rinaykumar**: Same, but it says submitted if you click on the test again
---

---
**Thread** [2021-03-03]
> **Danish.CS()**: I'm glad problem 4 was the easiest one lol
  → **Danish.CS()**: i mean problem 5* — the reduced array. If you know your pointers, it wasn't hard
  → **Biubiubiu**: Yeah but I got stuck in problem 3 for a really long time — until the last second literally
  → **Miggy**: The if-else one was kinda weird — seemed a little too easy
  → **LuongDang**: ifthenifelse is recursive
  → **dlau**: I did it with short circuiting
  → **LuongDang**: slide 92 in page 23 of reader — answer for if-else thing, solution is in Ruby but same thing
  → **Biubiubiu**: I'm scared if the if-else is wrong — 25% of the grade is gone
  → **Biubiubiu**: Yeah it should be nested if, not if-else
  → **Biubiubiu**: This exam is 28% of overall grade
  → **Miggy**: I'm sure students who aren't on discord and just went off Chegg are crying — I know from prior students a lot of those answers on Chegg are incorrect
  → **Biubiubiu**: I was actually being super honest — just use class material and reader
  → **Miggy**: That if-else was def the most unforeseen question
---

---
**Thread** [2021-03-03]
> **LuongDang**: you can write in any language on the exam yeah?
  → **Danish.CS()**: he said C, but it should be similar in C++ and Java
  → **LuongDang**: need to declare the language of course
---

---
**Thread** [2021-03-03]
> **LuongDang**: I hear it's curved
  → **Danish.CS()**: just pray no one gets more than 90, otherwise he won't shift the curve like it should be lol
  → **rinaykumar**: There's always that 1 guy that gets 100...
---

---
**Thread** [2021-03-03]
> **Mabas**: section 2 exam seems a lot more complicated than what we had in section 1 — ours was literally like "take these if/else statements and replace them with while-loops"
  → **Biubiubiu**: we were given the graph from reader pp.39 — the one without the solution. It has a pseudo code but it looks simple with tricks in it
---

---
**Thread** [2021-03-04]
> **Deleted User**: My code for the nested if-else exam question:
`if( C1 ) { B1; if( C2 ) { B2; ... if( Cn ) { Bn } else { D } } else { D } } else { D }`
  → **Deleted User**: Questions #1: 25 points, #2: 25 points, #3: 25 points, #4: 25 points
---

---
**Thread** [2021-03-04]
> **Deleted User**: If someone needs help getting SWI Prolog on Mac DM me. I am happy to help with setup.
  → **Danish.CS()**: help me!
  → **Abraham**: https://swish.swi-prolog.org (online Prolog environment — no install needed)
---

---
**Thread** [2021-03-07]
> **Deleted User**: Anyone have an idea when Midterm #2 is going to be? After Spring Break or before?
  → **rinaykumar**: Not sure on the date, but I heard he does the second midterm soon after the first. So we'll have less time to learn/prepare
  → **ramy1951**: If I remember correctly he said that we only have 3 weeks worth of material for midterm 2
---

---
**Thread** [2021-03-10]
> **Deleted User**: Professor Jozo scheduled Midterm #2 on Wednesday after Spring Break — but that Wednesday is a holiday. Someone should remind him.
  → **Miggy**: he said midterm 2 March 31st? Yikessss — right after spring break too
  → **Deleted User**: Professor told Midterm #1 grades will be posted by March 14th, 2021
---

---
**Thread** [2021-03-11]
> **Biubiubiu**: professor himself is super hard-working — I remember last semester he published a paper during Thanksgiving week
  → **dlau**: You were in his class last year?
  → **dlau**: I bet. He seems very passionate about his work
  → **Biubiubiu**: Yeah I took 676 — he's pretty supportive
---

---
**Thread** [2021-03-12]
> **dlau**: Anyone know when the next HW assignment is coming out? I hope he doesn't assign the hw and exam on the same week like last time
  → **Itzwaleed14**: When will he grade our hws? I didn't get anything yet
  → **dlau**: I already got my grades for HW — still waiting for the midterms
---

---
**Thread** [2021-03-14]
> **Mabas**: I got my grade for midterm 1 — you guys might be graded too
  → **Kuro**: got mine as well — it ain't looking too pretty
  → **Deleted User**: 66.48/100.00 — around C/C+/C-?
  → **dlau**: I got a lot lower than you — I didn't even get any feedback
  → **Deleted User**: I think Professor also did not open it for review — at least there should be a review of what we did wrong
  → **Deleted User**: Review = Not permitted
---
