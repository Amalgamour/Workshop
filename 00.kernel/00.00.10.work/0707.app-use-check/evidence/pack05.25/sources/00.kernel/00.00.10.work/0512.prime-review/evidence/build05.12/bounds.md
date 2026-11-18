# Bounds - referenced source versus document

JSON input documents stay at MAX_DOC 262144. load_input and strict_json and read_regular use that cap. A JSON input of 262145 bytes refuses `input: input exceeds 262144 bytes`.

Inline text stays at MAX_TEXT 12000. A source record above that refuses `text limit`. A null record stays null. This successor does not invent a record for a large file.

Source count stays 64, and only for the sources list. Every other list stays at 24. A 65th source refuses with the count, the limit 64, and the keep-every-source sentence. Holds of 25 and answers of 25 still refuse at their own list limit.

Referenced-source size is 16777216 bytes. It applies to source content_bytes, source transport_bytes, and the chunked bound-file hash. It is not an inline budget and it is not a prompt-context budget. Values 262144, 262145, 276423, and 16777216 bind from a compact JSON record. 16777217 bytes refuses with the actual length, the supported limit, and the keep-the-file sentence. A prefix hash is not verification.

No content-normalization read of a bound file was added. Same-hash still requires equal lengths. A present record still has to match its content hash and length.
