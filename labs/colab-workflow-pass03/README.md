# colab-workflow-pass03

Successor of labs/colab-workflow-pass02 for disposable N7NN books. The fact store is investigation.json at schema colab-exchange-investigation/2. Pass02 is unchanged and still reads schema /1. This module does not migrate those books.

New commands:

```
python -B colab_workflow.py seal-return-local --book ABS --page NNNN.name --pass 05.NN --return-file ABS --declared-transport TEXT
python -B colab_workflow.py open-pass --book ABS --page NNNN.name --pass 05.MM
```

seal-return-local stores the supplied file bytes as artifacts/<pass>/return.md and 05.NN.return.md. open-pass adds an empty later slot only from one recorded request-next review whose package and page-local return are intact. Show prints the transition list and writes nothing. Attach still runs the pinned v2 producer verify.

A partial.json or .write.lock page stays refused. This tool does not clean it up, prepare a package, call a model, reserve a capture, or write the live work book.
