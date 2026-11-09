# Brands

Aligned from `../brands.md` with decisions C3.3 and C8. The rules live in `decisions.md`; this page explains how they fit together.

## Purpose

A word can mean different things to different people. Relying on a model's average meaning is not good enough. "Ham" might be lunch meat, a friend's nickname, or Happy Arctic Men. When a user explains their meaning of a word, it is recorded, so models look it up instead of guessing.

## Parts

| Part | Where | Holds |
|---|---|---|
| **Brand** | `word.NNN` | one meaning of a word; `001-998` (`000` and `999` reserved) |
| **Brand card** | face 01 of the page that explains the meaning | forms, meaning, meters |
| **Dictionary** | page `0012`, face 03 | an index from each word to its brand cards, nothing more |

## Example

Book `10.10.11.user`, pages `1014.food`, `1026.relationships`, `1145.groups`.

Dictionary entry, in section `29` (ha-hh):

```
## ham
type: index
default: ham.003
ham.001: 10.10.11.1014.01.ham
ham.002: 10.10.11.1026.01.ham
ham.003: 10.10.11.1145.01.ham
```

Brand card on `10.10.11.1014.01`:

```
## ham
type: brand
brand: ham.001
forms: ham
means: user's favourite food, usually a sandwich
meters: sandwich 100%, lunch 95%, hungry 75%, eat 50%, meal 43%
```

The other two cards: `ham.002` (forms `Ham, Hammie, hammie`; a friend from work) and `ham.003` (form `HAM`; a Facebook group, Happy Arctic Men).

## Addressing

A word after a face is a card key: `10.10.11.1014.01.ham`. A 3-digit group after it is a brand: `...0012.03.ham.002`. Tail words are reserved, so card keys never collide with them. [C8.2]

## Forms and case

Forms are case-sensitive: `ham`, `Ham` and `HAM` can be different brands. A word is placed in a dictionary section by its lowercase form.

## Meters

The top 5 words that appear with this meaning, and how often each appears when this meaning is used. Only the compute writes meters (C8.7):
- Every resolution is recorded: word, brand chosen, sentence words, outcome.
- **Success:** the output runs and the user carries on.
- **Failure:** negative words, the user stopping the process, or **restatement** (the user repeating and over-explaining because the first attempt failed).
- On a failure, the compute updates the brand cards linked to that resolution.

Meters are readable on the card but never edited by hand, and are exempt from drafting.

## Resolving a word

1. The sentence matches one brand's meters clearly: use it.
2. No clear match: the brand last used in this session.
3. None used yet: the dictionary entry's `default`.
4. No default, or no brand: the LLM's ordinary meaning.

Every assumption is stated back ("ham, taken as ham.001, the sandwich").

## Learning a new meaning

When the user shows a meaning the dictionary lacks, the compute pushes the model to ask for it. The model hands the answer to the compute, which creates the brand card and the dictionary entry through drafting (`drafting.md`). The user confirming the meaning is the review.

## Local first

Each book keeps its own dictionary. The kernel provides a small base dictionary that books inherit. Referencing other books' dictionaries (source books) is a later design.

## Dictionary layout

One fixed layout from the kernel out, never re-split. Each letter has 1-5 sections by its share of English words.

| Range | Use |
|---|---|
| `03.00` | menu |
| `03.01-03.09` | reserved: digits and symbols |
| `03.10-03.61` | letters (A `10-12`, B `13-15`, C `16-19`, D `20-22`, E `23-24`, F `25-26`, G `27-28`, H `29-30`, I `31-32`, J `33`, K `34`, L `35-36`, M `37-39`, N `40`, O `41`, P `42-45`, Q `46`, R `47-48`, S `49-53`, T `54-55`, U-Z `56-61`) |
| `03.62-03.98` | reserved |
| `03.99` | continuation |

The full split within each letter is in `decisions.md` C8.6. The within-letter boundaries are estimates, to be checked against a real word list before freezing.

## Open

- C8.7: does a failure count only against an assumed brand?
- C8.10: where a new brand card goes when no page for it exists.
