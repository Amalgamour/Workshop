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
    - examples 
    - DD.title after dot doesn't == next axis so it's a desk title
    - DD.SS.title = shelf title
    - DD.SS.BB.title = Book title
    - DD.00.BB.title shelf == 00 meaning it's a desk book
    - DD.SS.BB.PPPP.title Page title long form
    - PPPP.title short for page must reference parents for full title. 

### Faces design
- Faces exist without titles as they are a face and not a whole. 
- Faces can have counters attached to them as two digits after the face 
- Face address example PPPP.FF short
- Face address example with book BB.PPPP.FF med
- Face address example DD.SS.BB.PPPP.FF full found by its inherited from book shelf and desk
- Face can have a counter after it's FF.NN a climbing number for faces that contain a version of a face.  Example 0001.05.01 is a page 0001 Face 05 and 01 is the first piece. 
- Seated face exists only as 05 no tail or counter. 
- Seated face only legal formate DD.SS.BB.PPPP.FF That is the seated address. 
- Counter face DD.SS.BB.PPPP.FF.NN goes from 01-98. 

## Face format

- Must have a stamp the as the header explaining the context and what face.  
- Contents a viewable list of the sections
- Cards: Are like kamban cards. These contain a title that is referencable for finding and retriving the exact piece of information. With details as the body. 
- Cards can be difference by face, Knowing each face design is important and must be retrivable and useable in an AGENTS.md Refrence always points to addresses for ease of finding. Cards titles are to be matched across faces.  


## Faces

- Face 01 - law or agents understanding of the meaning of the page.  Can contain model effiecient card sections. 
- Face 02 - schema where templates live, this is where a model or compute can find the exact process.
    - Cards are linked across faces by title name
    - A Card of Face 01 that requires schema, formatting, design, templates live on Face 02
    - 
- Face 03 - Operate Designed for the compute. Where the compute is giving the operations for executing a card if needed.  Primarily only found in the kernel or a desk book.  Possible in a book environment in the reserved fields.  
    - Primarily contains the cards contents list with the card title. face 03 card menu not found on any other face, for menu must refence Face 03
    - States where authority comes from 

- Face 04 User face designed for the user to see the why of the page.  Formatted for a user to read for inspection. Most pages created by a user will only have a face 04 and maybe a menu of the sections. So it can be long form.  The cards of face 01 and 02 must have a representation on face 04.  With them becomes sections of the face 04.  
    - Cards from face 01 and 02 must include a while piece along with a full readable explaintion of the card on face 01 and 02.
    - When a user is working there ideas when working on a page are recorded into face 04. That doesn't require to be representate by face 01 or face 02 

Face 05 Tasks Designed as a working place for working agents. build into passes. 
    - different formatting contains a counter 05.NN 
    - Contains tails as well so a counter face can be PPPP.FF.NN.tail
    - Current tails
- `05.MM.draft` the pack being written
- `05.MM.pack` ready to run
- `05.MM.open` Being run by a worker
- `05.MM.return` what was done
- `05.MM.review` the review
- bare `05.MM` closed

Face 06 Notes - a location for where a model what needs to leave information can drop it.  