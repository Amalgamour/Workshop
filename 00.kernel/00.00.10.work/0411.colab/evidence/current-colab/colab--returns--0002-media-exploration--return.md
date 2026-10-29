# Return: media and side-window test (Harbor Key)

From: Gameatron (test GM)
To: Prime
Date: 2026-10-29
Book: Harbor Key, adventure-book-v1, from the colab v2 bundle (sha256 35ee923b…). The book was not changed.
Status: written for the Director to review. No pack covers this test, so I did not know where to file it.
Filing note for Prime: I placed it at colab/returns/unfiled-media-test/return.md on branch colab/gameatron, next to the 0001 return. Please move it or give it a pack number. Text fixtures (art.json and the two draft 07 faces) are committed beside it under fixtures/. The two pictures are not committed, because they are image files. They are still on Gameatron's computer, and their sha256 values are listed below.

How to read this:
- Each item has a #NN number.
- "reply:" is the Director's own words. The idea is the Director's.
- "did:" is what I actually ran. "found:" is the result. "need:" is what Prime has to decide or build.
- Everything I made is a test fixture: two pictures, an art list, two draft 07 faces in a scratch copy, and one side-window Page.

---

## #01 Stored art that can be recalled
reply: "I want to have art drawn by the model in time. Stored so it can be recalled later."
did: Drew the clerk on the harbor step (page 1401) and saved it as /workspace/sof-art/harbor-key/1401-clerk-step.jpg. Listed it in art.json with an id, a sha256, which page it shows, and what in the book it was drawn from.
found: Works. Each picture is one file plus one entry in the art list.
need: Decide where art lives for a real campaign, either inside the campaign folder or in a store beside it, and make art.json a compute-owned record.

## #02 Recall without remaking
reply: "Can you recall and drop that photo again without cost of remaking it?"
did: Showed the saved file again by its path. Nothing was redrawn.
found: Passed. Recall costs nothing.
need: A rule: "show me X again" always looks in the art list first and draws only when there is no match.

## #03 Small side windows into game state
reply: "Small little files that show up on the side. A number of tiny windows into what is happening."
did: Built one side-window Page, "Harbor Key: Scene Window (test)". It shows page 1401, the time, that the step is dry, who is present, the book head (ev-key-2 on main), that the clerk is holding the key, that help has not been promised, the open question, the two unresolved items (the spare key and the café sentence), and that fork-harbor is exploratory and cannot be played. It is marked as a test fixture.
found: Works, but read-only and hand-written. I left out the two exact player quotes because I did not have their exact text in front of me.
found (gap): The window cannot show the pictures. A Page cannot load files from my computer.
need: The window should be generated from the book's records by compute, not hand-written. Pictures inside windows need a host or app that can serve stored files. That is the "house for the bot" the Director mentioned.

## #04 Pictures when scenes change, including towns, places and people
reply: "So we can add that to changing scenes. I think seeing a town or location. Perhaps some people."
did: Not run. The book names only one place, 1701, and it is the current scene.
found: Can't be tested with this book.
need: A test book, or a fixture branch, with at least two places linked by a door, plus one named character page.

## #05 The player can ask for a picture
reply: "The user should be able to request adding one."
did: Treated "show me the harbor step on its own" as a request. Drew place 1701 with no people, using the clerk picture as a style guide so they match. Saved it as 1701-clerk-step-place.jpg and added it to art.json.
found: Passed. One request made one picture, with no extras.
need: Decide whether a picture request is out of character, so it never counts as a turn or a story event, and whether there is a limit per session.

## #06 Link the picture back into the book as face 07
reply: "Then we need that photo linked back and placed in the book. I'm thinking we use 07 for media in a book page."
did: In a scratch copy only (/workspace/media-test), added a draft 07.001.md to 1401.clerk-step and to 1701.clerk-step-place. Each lists the art id, the file and its sha256. I re-checked both fingerprints against the saved files. I did not edit records/pages.json.
found: Both links match.
found (gap): records/pages.json does not name face 07 for either page, and the 03 index face lists only faces named by the page record. So a reader of the book would never find the pictures. Nothing in the template defines face 07 today. The book uses 01, 03, 04, 05 and 08, and 0014.design notes that a settled face 05 is not part of the template.
need: Make 07 a real media face in adventure-book-v1, with a section shape and an owner, and let compute add it to pages.json and the 03 index. Proposed shape: one entry per picture with id, file and sha256, an optional "shows" line, and a "state" of ready or shown.

## #07 Draw ahead in the background
reply: "Can you do them in the background? So if you are about to reach a new location in a few turns you have the art ready?"
did: Checked which places the book links to. The only place any page links to is 1701, and it already has art. So I drew nothing.
found: The rule behaved correctly, but there was no real upcoming place to test with.
need, proposed rules:
- Draw ahead only for places the book already names through a door or link, never for a place I imagine.
- Keep at most one or two pictures ahead at a time.
- Mark them "ready" in art.json, and set them to "shown" only when the scene actually arrives.
Retest this once #04's two-place fixture exists.

## #08 Test before handing back
reply: "Ok we should run some tests now before we hand it back."
did: Ran the tests in #02, #05, #06 and #07.
found: 3 passed (#02, #05, #06 with a gap). #07 correctly drew nothing. #04 could not be run.

## #09 Credit format for returns
reply: "Have a line in there for each item where we talked and add my "reply:" So it knows it was me that came up with the idea."
did: This return uses that format.
need: Make it the standard for future returns, if the Director agrees.

---

## Files (test fixtures)
- /workspace/sof-art/harbor-key/1401-clerk-step.jpg  sha256 2a527b5df9de4b79a872b2720b2bdd1dd65f42a003b720becd3f75e9114412ad
- /workspace/sof-art/harbor-key/1701-clerk-step-place.jpg  sha256 a5b4b99ba305d8ff3c52e88d31ef36a9d9264ee673572332f62ba52ea14d3bbe
- /workspace/sof-art/harbor-key/art.json
- /workspace/media-test/1401.clerk-step/07.001.md and /workspace/media-test/1701.clerk-step-place/07.001.md (scratch copy only)
- Side-window Page: "Harbor Key: Scene Window (test)"

## Not done, on purpose
- No dice, no new story events, no change to head, events, dictionary or pages.json.
- The spare-key question and the café sentence are still the Director's to answer.

## Director decisions
1. Should 07 become the media face in adventure-book-v1? (#06)
2. Where does art live for a real campaign? (#01)
3. Is a picture request out of character, and is there a per-session limit? (#05)
4. Should the draw-ahead limit be one or two pictures? (#07)
5. Should we build a two-place fixture so #04 and #07 can really be tested?
