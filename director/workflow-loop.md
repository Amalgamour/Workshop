# workflow

This space is to explain how a loop should work.  How to loop through the work. 


## band design 

- uses the bands concept from seqaddr.md in the hundreds bands
- bands N(digit) stands for the hundreds location in the page.  So N4 means it can exist in any thousands band as the N400-N499. N5 = N500-N599
- Working bands 
1. N1NN not in use 
2. N2NN not in use 
3. N3NN modules build with explaintion.  
    1. Face 01 explains what the module is here. 
    2. Face 02 holds the actually written files sto
4. N4NN = Dev.band This is where work is designed questions asked and answers 
primarily used by the Person to talk to the Model. 
    1. Face 04 mostly, with Face 05.NN to match
5. N5NN = jobs.band where 05.NN is written for a builder.  See bands and tails in seqaddr.md 
6. N6NN = not in use 
7. N7NN Colab.band where labs linked to the page is found

## bound bands
- bands are bound into a group N4 is the dev space links to N5 for the packs and returns to live from work.  The builder reports what is build in N3
- The face 05 is the linking piece.  Example N4 if in the admin thousands of 0 means it would be 0400-0499. Work starts at 0401 as 0400 is the door.  
- the last two digits of the page is linked to the N5,N4,N3,N7 
    - Example if we design a timer it's design lives at 0401.timer it's build packs live at 0501.timer  The build lives at 0301.timer and any labs live at 0701.timer.  They must link.

## work packs
- packs are made up on a file that contains an agents.md style build list for a model.  Tickets/tasks live in face 05.  as a counted face example 05.01 is the first place a pack can be written. 
- within this file exists a series of instructions
1. Who made the pack, who authorized it, what is the expected outcome. 
2. Overview what is the task we are trying to achieve, matches the N4 01 and 04. 
3. #NN starting at 01 is the cards each piece of work. 

Example:
#01 >build the lead command
placed: 2026-10-22
reason: From 0107.workflow/05.09 #05.
recommend: In jobs.py, add a command that takes Did, Blocked, and Need and writes them as three lines before the first #NN on a 05.NN.return.md. It refuses a file that is not a return. Stamp the change. Keep an older jobs.py copy.
path: 10.workshop/10.10.work/10.10.10.lib/code/jobs.py
scale: 2
Ask: >build Add the lead command.

4. add as many of these as needed.  Until the 05.NN.pack is ready for a worker to use. 
## Process

- N4 starts the process what is the work.  
    - Sets MVP for this page
    - What are the goals we want to achieve
    - What are we trying to prove?
    - Writen in 04 with a agents.md style 01 to go with it. 
- N5 Where packs and returns go. It's how Axiom 6 lineage works
    - Write as face 05.NN uses tails draft, pack, open, return, 
        - 05.01.draft where a piece of work is stored from the 
    - Builder reads the pack sets its tail to open so it's known to being worked on  Comepletes each #NN in the pack makes a copy calling it 05.NN.return addes what it did, asks questions applies requestions permission and or soultions to what blocks it. 
    - Adds it's notes and overflow and unprompted with why's at the end after the cards #NN.  
- Lead model takes the 05.NN.return appies it's understanding back to N4 as a matching 06.NN Updates or corrects the 01 and 04 if needed. If the MVP isn't completed it runs another pass.  
- Each pass should require more gravity to complete.  1-3 passes normal.  4-6 abnormal should pause and request assistance to solve. 
