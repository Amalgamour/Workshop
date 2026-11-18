# Failure and recovery — workflow pass04

date: 2026-11-01
who: Grok-2
state: written before labs/colab-workflow-pass04

This plan replaces the pass03 statement that a crash after truncation of investigation.json is outside the tool. Pass04 does not truncate that file or seal.json in place. It does not add a repair command. Pass03 FAILURE.md stays as the record of the previous plan.

## Sequence

commit does these steps in order.

1. Compute the candidate investigation bytes and the publication id in memory. Read the current root pair. Predecessor none, or retained-prior with checkpoint id equal to the current investigation sha256.
2. Refuse resume refused when partial.json, attempt.json, or .write.lock already exists.
3. If publications/<publication id>.json or publications/<publication id>.published already exists, refuse publication collision with wrote false. No lock and no checkpoint are created.
4. Create .write.lock with the bytes 1 and a newline.
5. For retained-prior, exclusive-create checkpoints/<checkpoint id>/investigation.json, seal.json, and identity.json. Read them back. A collision refuses checkpoint collision with wrote false.
6. Exclusive-create publications/<publication id>.json and attempt.json.
7. Write extras with the existing byte writer. A new return artifact is in this step.
8. Exclusive-create each projection under staging/<publication id>/projections/ and os.replace it onto the page projection path.
9. Exclusive-create staging/<publication id>/investigation.json and seal.json, read them back, then os.replace investigation.json and afterwards seal.json onto the page root.
10. Read the root pair back. Exclusive-create publications/<publication id>.published.
11. Remove attempt.json and partial.json only after that published file exists and the root pair matches the candidate.
12. The finally step removes .write.lock when it is present and is not a reparse.

A Refuse from a check propagates and does not write partial.json. Any other exception writes partial.json and raises Refuse interrupted write with wrote true. The lock is still removed in finally. The checkpoint, publication record, attempt.json, and staged files are not removed.

write of a new staging or checkpoint file calls WRITE_HOOK before os.open. os.replace calls REPLACE_HOOK before the replace. A hook or an os.write error therefore happens against the staged file, or before the replace, and does not open the existing authority file with O_TRUNC.

## Injected boundaries

Tests inject these on new disposable books. They are not power-loss trials.

- Partial os.write of the staged investigation.json, then OSError, on a page that already has a sealed pair. The root pair stays byte-identical. The checkpoint matches that pair.
- The same partial write during the first open. Predecessor none. No checkpoint directory.
- OSError from REPLACE_HOOK before the investigation.json replace. The root pair stays byte-identical.
- OSError from REPLACE_HOOK before the seal.json replace and after the investigation replace. The root investigation is the candidate, the root seal is the prior seal, and the checkpoint is the prior pair.
- Partial os.write of a staged projection. The live projection and the root pair stay byte-identical.
- WRITE_HOOK raising before the staged record is opened. The root pair stays byte-identical.
- An interrupted seal of a second pass after 05.01 already has a package, a page-local return, and a review. Those 05.01 artifact bytes stay hash-identical.

A failed command returns refused, not complete. The checkpoint's transition list, when the checkpoint finished, does not contain the failed action. show then reports partial true. The next command returns resume refused and writes nothing.

## Checkpoint collision and replay

If checkpoints/<current seal id>/ already exists, the next commit refuses checkpoint collision, wrote false, leaves the planted bytes, and does not write partial.json. An identical seal-return replay returns repeat, wrote false, and adds no publication and no checkpoint. A later successful commit retains the then-current pair under its own seal id. An unrelated checkpoint directory is not consulted. Planting checkpoints/ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff/ does not change show.

## Recovery

Stop. Do not delete partial.json, attempt.json, or a checkpoint to obtain a success result.

When the three blockers are absent and the root seal matches, the root pair is current. Checkpoints are not authority.

When a blocker is present, read attempt.json. Recover only checkpoints/<retained_checkpoint>/. Verify the identity digest, the investigation hash, and the seal field. Copying that pair aside is the inspection. Putting it back on the page is a later Prime decision. This tool will not copy it back and will not delete the blocker.

If predecessor is none, there is no prior sealed pair to restore.

A torn page-root projection is rebuilt, if Prime chooses, from the retained record and the artifact return bytes. The tool does not perform that rewrite.

No race-freedom and no power-loss guarantee is claimed. AR-01 stays held. Hard-link probes are not used.
