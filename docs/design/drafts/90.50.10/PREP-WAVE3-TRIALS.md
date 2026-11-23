# Wave 3 trials and the move off 0405

Nov 23, Cursor-C (Pack). Held. Not published.

The plan (12.3) says one lab pass writes one page's trial, so two passes can be open
when the files differ. 0701 pass 05.02 is the 0404 trial. 0701 pass 05.03 is the 0415 trial.
Page grant stays tests/ from the original init. Each pass may touch only its own lab file.

05.02 pack hash: 0fe67d63e293f6102674cf21a06ba8a9c6be07c310e499ff07bc9ca74783023c
may touch: tests/lab_0404.rs
05.03 pack hash: 674d965e08dbb013e4ce8e1e05a3e6d70c74c6a11b80ff4580d8e94b037838dd
may touch: tests/lab_0415.rs
Builder: Grok-1. Start a823ee28. Template 4. Kit branch returns.

0407 and 0408 may-touch lines were checked and left as they are.
11.7 page tests: tests/page_0407.rs and tests/page_0408.rs.
13.5 lab trials: tests/lab_0407.rs and tests/lab_0408.rs, named on face 01.
The lab files stay off those pages. The plan says a trial file belongs to the lab, never to the work page.

0416 replaces the dropped 0405 scratch pack.
0416 pack hash: 820addfaeea5de4bad2df510d8331d9205d71e3a30d6e9966f2f2c9de00d9907
grant: tests/wf.rs, tests/page_0416.rs
