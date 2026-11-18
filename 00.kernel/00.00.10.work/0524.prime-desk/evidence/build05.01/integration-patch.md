# Integration proposal — not applied

`app/librarian.py` was not edited. Its pack pin remains `939484f152c9227482e857f9ce88eaf40649f433a57d6c9d213a07bde16baee5`, 10463 bytes. No shared facade, no `00.live` rewrite, and no successor module import.

The development entry already has `prime-status`, `prime-review`, `prime-guard`, and `prime-check-next`. Those stay as they are. A Prime desk view should not be folded into them. `prime-status` calls pinned intake. The review commands call the review door. This view is a separate read of one explicit request.

If a later reviewed pass adds a door, the smallest change is a new command that only forwards arguments:

```text
prime-desk view --request ABS [--json]
prime-desk packet --request ABS --work-id ID [--json]
```

That door would subprocess `labs/prime-desk-pass01/prime_desk.py` and return its exit code. It would not build the request, crawl the book, call `validate_context`, call Git, or import `labs/prime-cycle-pass03`, `labs/review-loop-pass02`, or `labs/review-construction-pass02`.

Do not apply that change from this file. Review-loop integration remains the pending operation row already emitted by the tool.
