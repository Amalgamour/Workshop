# Local return intake

Write the exact response to evidence/pass05.01/submission.md and the working notes
to recipient-notes.md first. Run from D:/Git/lib-build:

```text
python -B labs/colab-support-pass02/colab_support.py intake --output "D:/librarian/colab-outgoing/0702-desk-state-review-0501/prepared" --config "D:/librarian/colab-outgoing/0702-desk-state-review-0501/config.json" --book "D:/Git/lib-build/00.kernel/00.00.10.work" --member 0168.desk-state-colab-0501 --return-file "D:/Git/lib-build/00.kernel/00.00.10.work/0702.desk-state-review/evidence/pass05.01/submission.md" --source-root "D:/Git/lib-build" --artifact "00.kernel/00.00.10.work/0702.desk-state-review/evidence/pass05.01/recipient-notes.md|00.kernel/00.00.10.work/0702.desk-state-review/evidence/pass05.01/recipient-notes.md" --json
python -B labs/return-capture-pass01/return_capture.py verify --book "D:/Git/lib-build/00.kernel/00.00.10.work" --member 0168.desk-state-colab-0501
```

Do not edit the package or invent an approval. Keep partial work and report any
refusal. No fallback capture allocation or Git writes. Prime reviews the result.
