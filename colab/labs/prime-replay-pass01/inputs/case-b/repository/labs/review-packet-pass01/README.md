# review-packet-pass01

Mechanical packet assembler for one named return. It records custody, exact sources, and artifact-byte checks.

```text
python -B labs/review-packet-pass01/review_packet.py assemble --request REQUEST.json
```

Exit 0 means the packet directory is complete. Exit 2 means the request was refused, or the directory is partial and was kept. A complete packet can still record reserved, missing, incomplete, or refused custody.

A verified receipt is custody, not acceptance. Return claims remain claims even when a hash matches.
