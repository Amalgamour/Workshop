# Brands 

## Purpose

- Brands resolve a very important aspect of working with an LLM Because meaning of a word can change from person to person.  Relying on averages isn't a good idea. 
- example: the word ham what does it actually mean?  is that ham the lunch meat?  Is it an acronym?  Happy Artic Men?   Is is a nickname?  When a user explains their meaning of a word it needs to be recorded and added to the dictionary. 
- the brand works like this.  (word).bbb so when a dictionary search happens.  It can connect to the write page 
- bbb runs 001-998.  000 and 999 are sentinels, reserved and unused.  Most words carry a handful of meanings.

## Example
10.10.11.user  Page 1014.food, 1026.relationships, 1145.groups 
word - ham, hammie, Ham, Hammie, HAM

ham.001 ham, user favourite food, usually a sandwhich, ref. 10.10.11.1014.01.ham 

ham.002 Ham, Hammie, hammie: User friend from work  Ref. 10.10.11.1026.01.ham

ham.003 HAM: A FB group the user is active it.  Short for Happy Artic Men.  Ref. 10.10.11.1145.01.ham

## Formatting

- should match seqAddr.md.  The reference word is a card key, not a tail (tails are reserved words).  It is attached to 01.cardtitle for the section that is being referenced: `10.10.11.1014.01.ham`.
- A 3 digit group after the card key is the brand: `ham.002`.

## Card Brand

- The Card will be titles ham 
- type: brand
- brand: the brand number, linking back to the dictionary (ham.001)
- forms: the words it covers, case matters (Ham, Hammie, hammie)
- means: what the user means by it
- it contains the top 5 key words found in the sentence. 
- How often each of those appear when its meaning.
- example ham the lunch meat, shows up sandwhich 100%, lunch 95%, hungry 75%, eat 50%, meal 43% 
- Meters are written only by the compute.  They are not drafted.
- Success: the emit runs and the user carries on.
- Failure: negative words, the user stops the process, or restatement (the user repeats and over-explains because the first attempt failed).  On a failure the compute updates the brand cards linked to that piece.

## dictionary
- the dictionary points to all brand cards as address dd.ss.bb.pppp.01.(cardtitle)
- It is only an index.  It lives on page 0012 face 03, counted: 03.00 is the menu, 03.NN are sections.
- Each entry can mark a default brand.
- One fixed layout of sections from the kernel out, never re-split.  Each letter gets 1-5 sections by how many words start with it.  Full table in claude/decisions.md C8.6.
- Each book keeps its own dictionary.  The kernel gives a small base dictionary to inherit.

## Resolving a word
1. The sentence matches one brand's meters: use it.
2. No match: the brand last used in this session.
3. None used yet: the entry's default.
4. No default or no brand: the LLM's ordinary meaning.
- Every assumption is stated back so the user can correct it.
- When the user shows a new meaning, the compute pushes the model to ask for it.  The model hands it to the compute, which adds the brand card and dictionary entry.  The user confirming the meaning is the review.

## Open
- Does a failure count only against a brand that was assumed?
- Where does a new brand card go when no page for it exists?
