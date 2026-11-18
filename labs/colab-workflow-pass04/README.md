# colab-workflow-pass04

Successor of labs/colab-workflow-pass03 for disposable N7NN books. The fact store is investigation.json at schema colab-exchange-investigation/2. Before a later commit replaces that file and seal.json, pass04 copies the verifying pair to checkpoints/<seal sha256>/. Those two authority files are published with os.replace from exclusive staging files. Pass03 is unchanged and still truncates them in place. This module does not migrate those books and does not recover a partial page.

Show prints the transition list and writes nothing. Attach still runs the pinned v2 producer verify. A partial.json or attempt.json page stays refused. This tool does not clean it up, prepare a package, call a model, reserve a capture, or write the live work book.
