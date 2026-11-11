# Workshop

## Business Requirements

- Make the choices on hardware, software and design
- A persistant retrivable database storing Why's
- A why is the reason to do something, where a finished spec is a recipe and recipes can rot
- Intelligence bleeds so reliablity is important 
persistant storage system Give options
- must be checkable by a person 

## Technical Details
- Always build code cleanly, modular, and with proper architecture and seperation of concerns. 
- Fractal: Smallest to largest should be consistant. Always look at the source before making a different choice.
- Why: failure to record your decision is a recipes can rot. When we have the why rebuild is possible. 
- Record: Intelligence that doesn't take notes and review them is processes not recovered.  






## Fractal Design

- Our axioms is the design we start from What ideas need to be asked during work.
- view Axioms.md
- Axioms is the shape, seqaddr is the geometry


## Sequence Addressing

- view seqAddr.md to understand it's design
- Is the new form of a filetype we are going to be creating
- It's a multi faced file that can be stored in a database
- We need a reader to be able to view the difference faces and how it all links together. 

## Compute & Database

- **Compute:** The deterministic engine between the model, user, and storage. Handles addressing, retrieval, validation, permissions, and writes.
- **Database:** Persistent, retrievable storage of information, decisions, reasons, relationships, and history. Preserve the why, not just the finished result.
- **Design:** Books contain pages, pages contain faces, faces contain cards. Use SeqAddr to locate and connect them. Inherit governing rules rather than duplicating them.
- **Authority:** People authorize, models reason and propose, compute validates and executes. Models do not directly modify canonical records.
- **Integrity:** Preserve lineage and prior states. Changes must be traceable, recoverable, and resistant to incomplete writes or conflicting updates.
- **Retrieval:** Find information by address, title, card, or recorded connection. Return only the context needed, with its source and governing rules.
- **Technology:** Evaluate storage and compute options against reliability, speed, portability, and human inspection. Record why each choice was made.
- **Validation:** Build small, testable components. Verify each layer independently before composing larger systems.
## Kernel

- view kernel-design

## UI

Use NextJS to design the interface, clean and smooth design. 