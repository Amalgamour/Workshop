# Sequence Address

## What it is

- new design for a file type
- a page is a file that contains multiple faces instead of being 2d with one face we have multi faces
- Each face contains a different bit of information

## Design

### Axis design
- digit axis min 2 numbers
- dots count as hiearchy highest left lowest right
- Chosen sequence 2.2.2.4.2
    - 1st axis is DD for desk highest controling environment
    - 2nd axis is SS for shelve a themed work space 
    - 3rd axis is the BB for Book a localized environment
    - 4th is the page axis PPPP giving a large space for the work that can exist within the book environment
    - 5th axis is the faces as 2 digits 

### Title Design
- Then comes the Title. you have reached the end of the seqaddr after a dot that has any other formatting then strictly digits. Title can be any length but it is prefered to be one word or hyphenated word.
    - Position decides: a word after DD, SS, BB or PPPP is a title. A word after a face is a card key. Tail words are reserved and are never titles or card keys.
    - Title characters: lowercase letters, digits, hyphens, starting with a letter. No dots.
    - A title is a label stored in the stamp. A title written in an address is checked against it.
    - Pages 1000 and up must have a title. Page 0000 has none.
    - examples 
    - DD.title after dot doesn't == next axis so it's a desk title
    - DD.SS.title = shelf title
    - DD.SS.BB.title = Book title
    - DD.00.BB.title shelf == 00 meaning it's a desk book
    - DD.SS.BB.PPPP.title Page title long form
    - PPPP.title short for page must reference parents for full title. 

### Faces design
- Faces exist without titles as they are a face and not a whole. 
- Face 00 is the page's identity. It holds the page stamp, so the stamp is not repeated on each face.
- A page needs face 00 and at least one of faces 01-06 or 08. Draft faces count. If the last face is retired the page is retired.
- Faces can have counters attached to them as two digits after the face 
- Face address example PPPP.FF short
- Face address example with book BB.PPPP.FF med
- Face address example DD.SS.BB.PPPP.FF full found by its inherited from book shelf and desk
- Face can have a counter after it's FF.NN a climbing number for faces that contain a version of a face.  Example 0001.05.01 is a page 0001 Face 05 and 01 is the first counter. 
- Seated face exists only as FF no tail or counter. 
- Seated face only legal formate DD.SS.BB.PPPP.FF That is the seated address. 
- Counter face DD.SS.BB.PPPP.FF.NN goes from 01-98. 
- FF.00 is the board of a counted face: every counter and its tail. A face is counted only if FF.00 exists. A counted face is never seated.
- FF.99 is the counter continuation, required only once FF.98 exists.
- Faces 05 and 06 are always counted.

### Tails design

- Contains tails as well so a counter face can be PPPP.FF.NN.tail
- Current tails with counter
    - `FF.NN.draft` the pack being written
    - `FF.NN.pack` ready to run
    - `FF.NN.open` Being run by a worker
    - `FF.NN.return` what was done
    - `FF.NN.review` the review
    - bare `05.MM` closed
- Current tails without counter
    - `FF.draft` Draft of a face not seated so not to be used as active.
    - `FF.retired` A previously seated face turned into retired before it can be removed. 

## Face format

- Must have a stamp the as the header explaining the context and what face.  The stamp lives once on face 00.
- Contents a viewable list of the sections
- Cards: Are like kamban cards. These contain a title that is referencable for finding and retriving the exact piece of information. With details as the body. 
- A card is a ## heading. Its key is the heading in title form. Field lines (name: value) come under the heading, then the body.
- Every card has a card type (rule, schema, menu, why, task, note, link, brand, index), defined in the kernel. Each face has a default type.
- Cards can be difference by face, Knowing each face design is important and must be retrivable and useable in an AGENTS.md Refrence always points to addresses for ease of finding. Cards titles are to be matched across faces.  


## Faces

- Face 01 - law or agents understanding of the meaning of the page.  Can contain model effiecient card sections. 
- Face 02 - schema where templates live, this is where a model or compute can find the exact process.
    - Cards are linked across faces by title name
    - A Card of Face 01 that requires schema, formatting, design, templates live on Face 02
    - 
- Face 03 - Operate Designed for the compute. Where the compute is giving the operations for executing a card if needed.  Primarily only found in the kernel or a desk book.  Possible in a book environment in the reserved fields (pages 0001-0099).  
    - Primarily contains the cards contents list with the card title. face 03 card menu not found on any other face, for menu must refence Face 03
    - States where authority comes from 

- Face 04 User face designed for the user to see the why of the page.  Formatted for a user to read for inspection. Most pages created by a user will only have a face 04 and maybe a menu of the sections. So it can be long form.  The cards of face 01 and 02 must have a representation on face 04.  With them becomes sections of the face 04.  Face 04 is a full version, not a mirror: source, why:, then a full explanation.
    - Cards from face 01 and 02 must include a why piece along with a full readable explaintion of the card on face 01 and 02.
    - Hard check: the 04 card exists with a why: and a body. Findings: the 04 body copies the 01 body, or the 01 card's keywords are missing.
    - When a user is working there ideas when working on a page are recorded into face 04. That doesn't require to be representate by face 01 or face 02 

- Face 05 Tasks Designed as a working place for working agents. build into passes. 
    - different formatting contains a counter 05.NN 


- Face 06 Notes - a location for where a model what needs to leave information can drop it.  Uses the counter one notes per session. 
    - example 06.01 - notes by claude 
        - includes which model created the notes.
        - What it references to
        - When it was used why the note exists. 

- Face 07 reserved not active

- Face 08 map where all the links for a page goes. What dependances does this page have?  
    - xlinks between the authority of the page, 
    - What does this page depend on? 
    - What is actally needed to find this page and use it by the user, the model and the compute. 


## Sentinels
- The sentinels exist in every axis of the design. Its a full sequence of 0 and of 9.  Since our min axis is 2 a Seq00 would be '00' Seq99 is '99' 
    - Example of sentinal for a 4 digit axis is seq00 would be '0000' and seq99 would be '9999'
    - Two sentinels exist for every axis.  Those addresses with a seq00 or seq99 are special locations and cannot be normal pages. 
    - Only two sentinel locations can exist for any axis it's the alpha and omega for the axis
    - Page 0000 must exist for a book to be a legal space
    - Page 9999 must exist if the book is refenencing a sequence of a continuation of a book.
        - example 10.11.21.tile is a book address For that book to be legal it must have a DD.SS.BB.0000 No title allowed. 
    - A desk must also have it's sentinal as DD.00
        - if a DD.99 exists it means it's linking to a child desk under its authority and that child desk must have it's .00 linking back two it's parent desk. 
        - most desks will just point to the kernel as their parent or a branch of kernel focused on a different type of workr.  
    - A shelf must also have a .00 as DD.SS.00 
        - if it has a child it must include .99seq on it's parent.

## Reserved

- We have reserved spacing for any axis with intigers 1-9 expressed as it's full axis 2 digit is 00-09, 00 sentinal 01-09 reserved  
    - First open desk address is 10 through 98
    - First open selve same as desk
    - First open book same as desk
    - First open page starts at page 1001 (1000 is the head of the first user band)
    - Page 0001-0009 are special reserved pages
    - Page 0010-0019 reserved for Content, dictionary, Concordance other important pages that must exist
    - page 0020-0049 localized behavour may exist or inherite from parent or directly from kernel repos
    - Page 0050 - 0099 Structural pages likely only exist in kernel or repo templates 
    - 0100-0999 reserved for workflow.

## Decided since

Full rules in `claude/seqAddr.md`, reasons in `claude/decisions.md`.

- Short form: the 4-digit page is the anchor. Missing ancestors come from the active book. No page means a container address from the desk. A leading dot (.04) is the active page.
- Models always write the full address and state it back when a user wrote short form.
- Finding: book, shelf, desk, kernel. If nothing is found it is elevated to the user.
- 00 means the owner of the level above, itself. Every container is identified by its page 0000: 10.00.00.0000 is desk 10.
- 99 means look for the next location. It can list many targets. Every target links back.
- Kernel is desk 00. Desks 01-09 are kernel branches. 10-98 are user environments. One namespace per repository.
- Bands: the second digit of a page is the band. Every band is 100 pages, PP00 head to PP99 continuation. A full band continues through PP99, never grows in place.
- Tails: pages and faces take draft and retired. Counters take draft, pack, open, return, review. Containers take their state from page 0000.
- Page types: system, general, code, workflow, band, pointer. Defined in the kernel.
- Dictionary and brands: see brands.001.md.
- A book is one append-only file held by the compute: see claude/format.md.
