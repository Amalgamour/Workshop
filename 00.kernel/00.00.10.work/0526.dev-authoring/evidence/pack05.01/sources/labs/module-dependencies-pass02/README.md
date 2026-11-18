# module-dependencies-pass02

Successor of labs/module-dependencies-pass01/depdecl.py for 0525.app-dependencies/05.02.

Same commands. module-declaration/1 and module-declaration-set/1 keep the predecessor rules. module-declaration/2 adds an observed-file basis and a digest-only pin. The predecessor file is not edited.

Contract: 00.kernel/00.00.10.work/0525.app-dependencies/evidence/build05.02/CONTRACT.md

The app records are in labs/app-dependencies-pass02. Use:

    python -B labs/module-dependencies-pass02/depdecl.py validate --set ABS

This reader does not import named modules and does not fetch Git. Exit 0 is an answer about declarations.
