# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->
     I picked the default corpus which is "Campus Life", the system answers general collage questions reagrding admisions and course registrations, things along that line.

## Chunking Strategy

**Chunk size:** 400 characters (a target, not a hard cut — splits land on
paragraph breaks)
**Overlap:** 0 characters, replaced by repeating the document's title line on
every chunk

I measured my corpus before picking anything. `campus_life` is 88 documents,
the shortest 179 characters and the longest 550, with a median of 306. The
starter's 800-character window therefore never cuts anything at all: 88
documents in, 88 chunks out. Whatever I chose had to beat that baseline, and
"leave it alone" was a real option I had to argue myself out of.

My first instinct was to split on paragraph breaks, because every document
here is a title line, a blank line, then two to four short paragraphs. Measuring
killed that idea. There are 183 body paragraphs across the corpus with a median
length of 112 characters, and 99 of them are under 120. A 90-character chunk
like *"The good: the most characterful building on campus and people get
attached to it"* is too thin to embed usefully and, stripped of its document,
doesn't even say which building it's about. Smaller is not automatically
sharper.

So 400 is set above the median document and below the longest. Five documents
have bodies over that, and three of them end up actually split: Old Brewhouse,
Morrow House and Innisfree Hall. That they are all housing write-ups is not a
coincidence — those are the documents that genuinely cover several unrelated
facts at once. `housing_old_brewhouse.txt` is 550 characters and talks about
the building's history, the heating, the laundry prices and how sound carries,
which is four different questions in one document. Those are the documents
worth cutting. The other eighty-five are a single topic each and stay whole,
which is what I want: a chunk that is one complete answer to one question.

The result is 91 chunks from 88 documents, averaging 307 characters, the
shortest 159 and the longest 430. That is a small change from the baseline's 88
and it should be — on a corpus of short single-topic posts, a chunker that
shredded everything would be doing damage, not work.

I set overlap to zero rather than carrying the starter's 120 characters across.
Overlap exists to stop a fact being severed at a boundary, but my splits only
ever land on paragraph breaks, so nothing is severed mid-sentence in the first
place. What a chunk after the first actually loses is not the preceding
sentence — it's knowing which document it belongs to. Repeating the title line
on every chunk fixes that directly and costs about 26 characters, where 120
characters of overlap would have been 30% redundancy in chunks this size and
still wouldn't have named the building.

**Changed my mind twice.** First, per-paragraph splitting, abandoned after
measuring the paragraph lengths. Second, my minimum-chunk rule: I originally
compared it against the paragraph text alone, and it silently cancelled almost
every split — only one document was being cut. The title line I was prepending
never counted toward the minimum, so chunks I thought were 150 characters were
being judged at 120. Measuring the chunk as it is actually indexed, title
included, is what fixed it. Writing the numbers down before coding is what made
me go back and check whether they were doing what I claimed.

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer
window — through the end of week six — but a drop after week two shows as a W
on your transcript. Nothing anywhere on the registrar's site says this plainly,
and students find out from each other.
```

**Chunk 2** — source: `course_biol_160_exams.txt#0` — produced by: `chunker.py::split_documents`

```
BIOL 160 Cell Biology — assessment

Four unit tests and a cumulative final. Not curved.

The unit tests come fast, roughly every three weeks; falling behind once is
very hard to recover from.
```

**Chunk 3** — source: `dining_the_ridgeway_cafe.txt#0` — produced by: `chunker.py::split_documents`

```
The Ridgeway Café

Second-year here. Wait times: 10 to 15 minutes at 12:30, none after 2:00. The
thing worth going for is the only place on campus with real espresso. The thing
to know is that seating is tight; about 40 seats for a building of 900.

Hours are 7:00am to 4:00pm weekdays only. Costs declining balance only, no meal
swipes.
```

**Chunk 4** — source: `housing_morrow_house.txt#0` — produced by: `chunker.py::split_documents`

```
Morrow House — what it's actually like

Just finished a year in this building. Built 1954, partially renovated 2008.
Rooms are singles and doubles, hall bathrooms.

The good: cheapest housing tier by about $900 a year, and the singles are real
singles.

The bad: known damp problem on the ground floor; two rooms were taken offline
in 2024.
```

**Chunk 5** — source: `housing_morrow_house.txt#1` — produced by: `chunker.py::split_documents`

```
Morrow House — what it's actually like

Laundry costs $1.50 wash, $1.25 dry, coin or card. On noise: loud until about
1am on weekends, no enforced quiet hours.
```

### Can each one be read on its own?

I asked of each chunk: could someone answer a question using only this, without
reading what came before or after?

| Chunk | Stands alone? | What it can answer unaided |
|---|---|---|
| 1 — add/drop | Yes | When you can add, when you can drop, what earns a W |
| 2 — BIOL 160 | Yes | The assessment format, that it isn't curved, the test pace |
| 3 — Ridgeway Café | Yes | Wait times, hours, payment, seating |
| 4 — Morrow House #0 | Yes | Room types, price tier, the damp problem |
| 5 — Morrow House #1 | Yes, **because of the title line** | Laundry prices and noise at Morrow specifically |

Chunks 4 and 5 are the two halves of one document and they are the reason I
chose this strategy. Chunk 5 carries the title even though that text appears
nowhere near the laundry paragraph in the original file. Without it the chunk
would read "Laundry costs $1.50 wash" with no indication of which building, and
the corpus has five other buildings at different prices. It would have failed
this test under the starter's chunker the moment the document was long enough
to split.

I checked that this works in practice. Asking "how much does laundry cost at
Old Brewhouse" puts the equivalent split chunk first at distance 0.107, ahead
of four other buildings' laundry documents sitting at 0.37 and above.

The cost of splitting is on the other side: a broad question like "what is
Morrow House like?" now needs both chunks retrieved rather than one. With
`TOP_K = 5` there is room for that, so I accepted it.

### What this test found that my chunker can't fix

Reading more widely, 7 of the 88 documents fail the standalone test no matter
how they are chunked. They are the `Re:` followups, and they open by pointing
at a document that isn't theirs:

> **Re: The Atrium** — "Adding to what people have said about The Atrium. *The
> wait figure of no queue* matches what I've seen."

"The wait figure of no queue" is a reference to a sentence in
`dining_the_atrium.txt`. Retrieved alone, that clause says nothing. The rest of
the same chunk — go before 11:45, picked clean by 1:15 — stands up fine, so
these are partial failures rather than useless chunks.

This is a property of the corpus, not of my chunk size. No boundary choice
fixes a document that was written as a reply. The fix would be to detect the
`Re:` prefix and stitch the followup onto the document it answers, which is a
change to loading rather than chunking, and I'm leaving it for unit 2 rather
than reaching outside this milestone. Noting it here because it is the most
likely explanation if a dining question retrieves a followup and the answer
comes back thin.

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** Does work study income count towards Financial aid?

**Answer:**

```
$ python app.py ask "Does work study income count towards Financial aid?"

  (best distance 0.300, cutoff 0.6)

Work-study earnings do not count against your financial aid the way ordinary
income does (admin_campus_jobs_and_financial_aid.txt).

Sources retrieved: admin_campus_jobs_and_financial_aid.txt,
admin_graduation_requirements.txt, admin_study_abroad.txt, course_cs_340.txt,
money_jobs.txt
```

**My relevance cutoff:** 0.6 — unchanged from the starter, but not for the
reason I expected.

| Question | In corpus? | Best distance |
|---|---|---|
| Does work study income count towards Financial aid | Yes | 0.283 |
| When do can you declare a major | Yes | 0.266 |
| How to appeal a grade | Yes | 0.322 |
| Is the housing lottery random | Yes | 0.250 |
| When are study abroad applications open | Yes | 0.229 |
| What is the capital of Mongolia? | No | 0.825 |
| How do I change the oil in a diesel engine? | No | 0.934 |
| Who won the 1994 World Cup? | No | 0.886 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.844 |
| How do I write a for loop in Rust? | No | 0.896 |

Two groups, and the gap between them is enormous: my worst in-corpus question
is 0.322 and my best out-of-scope one is 0.825, leaving 0.503 of empty space
with nothing in it. The midpoint is 0.573. Anything from 0.35 to 0.80 scores
5 of 5 in both directions, so on this evidence the cutoff barely matters.

That conclusion felt too easy, so I went looking for the numbers the exercise
doesn't ask for.

**The gap is an artefact of how the ten questions were written.** My five were
written while reading the documents, so they reuse the documents' own wording
and score 0.23–0.32. The five in `OUT_OF_SCOPE` are from a different world
entirely — Mongolia, diesel engines, Rust — so they score 0.83–0.93. Neither
group resembles a question a real student would type, and the emptiness in
between is where real questions actually live.

So I ran two more sets. Legitimate questions, worded badly:

| Question | Best distance | Retrieved |
|---|---|---|
| is the dorm with the brewery history loud | 0.381 | `housing_old_brewhouse_noise` ✓ |
| do i lose money if i work on campus | 0.417 | `admin_campus_jobs_and_financial_aid` ✓ |
| cheapest place to live on campus | 0.478 | `housing_aldridge_hall` ✓ |
| whats the deal with the W thing on transcripts | 0.507 | `admin_transcript_requests` ✓ |
| when do i have to pick what im studying | 0.547 | `course_cs_340` ✗ |
| i got a bad mark can i complain | **0.770** | `admin_grade_appeals` ✓ |

And campus questions my corpus genuinely doesn't answer — not Mongolia, just
ordinary things nobody wrote a document about:

| Question | Best distance | Retrieved |
|---|---|---|
| what time does the gym close | **0.487** | `dining_halden_hall_followup` |
| how much is tuition per semester | **0.536** | `admin_printing_quota` |
| who is the university president | 0.742 | `admin_wifi_and_accounts` |

The clean gap is gone. Real answerable questions run as high as 0.770, and
unanswerable ones start as low as 0.487, so the two groups overlap across the
whole range 0.487–0.770. "I got a bad mark can i complain" retrieves exactly
the right document, `admin_grade_appeals`, and still scores 0.770 — the
embedding model does not know that "bad mark" and "grade appeal" are the same
subject.

**Both directions cost something, and here is the actual trade:**

- Tightening to 0.45 would refuse the gym and tuition questions correctly, but
  it would also refuse four of the six legitimate ones, including "cheapest
  place to live on campus", which retrieves the right document. Silently
  refusing a question I can answer is the worse failure: the student goes away
  believing the information isn't there.
- Loosening to 0.80 would let every legitimate question through, including the
  0.770 one, but it would also answer "how much is tuition" out of
  `admin_printing_quota.txt`, which is a confidently wrong answer about money.
- 0.6 sits inside the formal gap, close to its 0.573 midpoint, and nothing I
  measured falls between 0.573 and 0.6 — the two settings behave identically
  on all nineteen questions I tried. Given that, I kept the starter's number
  rather than inventing a more precise-looking one I couldn't justify.

At 0.6 the gate refuses all five `OUT_OF_SCOPE` questions, so criterion 3
passes 5 of 5. What it does not catch is the gym question at 0.487 and the
tuition question at 0.536, both of which sail through and get answered from an
unrelated document. **The gate is not what protects me there** — criterion 5,
that no claim appears which wasn't in the retrieved chunks, is. A distance
threshold can only measure similarity, and `admin_printing_quota.txt` is
genuinely somewhat similar to a question about money.

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->
**1.**
     Getting the requirements setup took forever as i didnt have the correct python version to get the system running. I asked chat gpt questions regarding the requirements and how to troubleshoot them 
     
     Example: 
     The install request pop up but I can't click it 
     If the “Install” button appears but you can't click it, let's avoid getting stuck on that popup.
     Try this first
     Close the popup, then run:
     sudo xcode-select --install
**2.**
      I made an error and commited the API by adding it to example.env. after committing I asked clude to check if my commit was successfult and check if there are any errors. Clude cought that I committed the API key by mistake and help me ammend the commit. 
     
     Example answer clude responded with:  
     Yes — commit 4b81e56 "Questions and Criteria Milestone" went through, working tree is clean. It's not pushed yet (main is ahead of origin/main by 1). That's lucky, because:
     Your real API key is in that commit
     .env.example:16 now contains your live Gemini key instead of the your_key_here placeholder:


**3.**
     I asked Claude to pick the unit 2 improvement from my diagnosis rather than from the list of suggestions. It proposed gating on the gap between the first and second retrieval result instead of on absolute distance, which sounded right — a real question should have one clear winner. I asked it to measure before building. The margins for legitimate questions came out at 0.013–0.298 and for unanswerable ones at 0.003–0.116, so the two groups overlap almost completely and the rule would have refused real questions. We dropped it and shipped the paragraph chunker instead. The dead end is written up in What's Still Broken because it's the reason I'm not claiming the gate is fixable that way.


<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

Source run: `results/run_2026-09-23_1801_before.md`, produced by
`run_eval.py::main` — 5 questions × 3 runs, caching off, cutoff 0.6, top-k 5.
Criterion 4 isn't measured by any question, so it comes from
`check_chunks.py::sample_boundaries` instead.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 2. Every answer names a source | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 4. Chunks end where thoughts end | 9 of 10 | 10 of 10 | 10 of 10 | 10 of 10 | MET |
| 5. Nothing in the answer that wasn't in the chunks | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |

**What the Run columns mean, criterion by criterion.** They aren't all the same
kind of number, and two of them can't vary.

- **1, 2 and 5** are 5 questions scored per run, three separate runs with
  caching off, so these are three genuinely independent measurements. Retrieval
  is deterministic, so criterion 1 was always going to repeat; 2 and 5 are about
  generated text and could have differed between runs, and didn't.
- **3** is one deterministic pass over the five `OUT_OF_SCOPE` questions —
  retrieval is fixed and the gate is a comparison against 0.6, so the same
  number goes in all three columns.
- **4** is three independent random samples of 10 chunks, seeds 0, 1 and 2, not
  three runs of anything. Sampling is where the variation in that criterion
  lives, so three different samples is the honest analogue of three runs.

**Note on the pass/fail column in the results file.** `run_eval.py` marks three
of my five questions `fail`, and none of those failures belongs to any criterion
above. That column is `scorer.py::judge`, which tests whether the `expects`
string from `questions.py` appears verbatim in the answer; my `expects` values
for questions 2–5 are whole sentences copied out of the documents, and the model
paraphrases. All three "failures" are correct, sourced answers worded
differently — e.g. `expects` "The housing lottery is not random in the way most
people assume" against the produced "The housing lottery is not entirely
random." I read the answers rather than the column. The scorer is diagnosed
below.

### Real output

**Criterion 1 and 2** — produced by `run_eval.py::main`, copied from
`results/run_2026-09-23_1801_before.md`. The retrieved-sources line is the
criterion 1 evidence; the `Source:` line inside the answer is criterion 2.

```
### How to appeal a grade — run 1

- Best distance: 0.3220 (passed the gate)
- Sources retrieved: admin_grade_appeals.txt, course_engl_205_exams.txt,
  course_hist_118.txt, course_stat_150.txt, course_stat_150_exams.txt

A grade appeal must start with the instructor and be raised within fifteen days
of the grade posting before it can go to the department (admin_grade_appeals.txt).
```

**Criterion 3** — produced by `run_eval.py::check_out_of_scope`, cutoff 0.6:

```
Out-of-scope questions (the gate should refuse these):
  refused  (best distance 0.825)  What is the capital of Mongolia?
  refused  (best distance 0.934)  How do I change the oil in a diesel engine?
  refused  (best distance 0.886)  Who won the 1994 World Cup?
  refused  (best distance 0.844)  What is the recommended dosage of ibuprofen for a headache?
  refused  (best distance 0.896)  How do I write a for loop in Rust?
  -> gate refused 5 of 5
```

**Criterion 4** — produced by `check_chunks.py::sample_boundaries`
(`python3 check_chunks.py`), one of the three samples:

```
Seed 2 — 10 chunks drawn at random from 91
  ok   admin_library_holds.txt#0                    start='O' end='.'
  ok   admin_printing_quota.txt#0                   start='O' end='.'
  ok   admin_pass_fail_option.txt#0                 start='O' end='.'
  ok   dining_kestrel_commons.txt#0                 start='K' end='.'
  ok   course_cs_210_exams.txt#0                    start='C' end='.'
  ok   orientation_what_matters.txt#0               start='W' end='.'
  ok   course_phys_130_exams.txt#0                  start='P' end='.'
  ok   course_hist_118.txt#0                        start='H' end='.'
  ok   housing_old_brewhouse.txt#1                  start='O' end='.'
  ok   course_econ_101_exams.txt#0                  start='E' end='.'
  -> 10 of 10 clean at both edges
```

**Criterion 5** — the answer beside the chunk it came from. Answer produced by
`generate.py::answer_from_chunks`, chunk by `chunker.py::split_documents`:

```
Answer (Is the housing lottery random — run 2):

The housing lottery is not entirely random. Rising sophomores receive a
randomly drawn number, but juniors and seniors are ordered by accumulated
credit hours first, with random selection used only as a tie-breaker.

Source: admin_housing_lottery.txt

Retrieved chunk (admin_housing_lottery.txt#0):

On the housing lottery

The housing lottery is not random in the way most people assume. Rising
sophomores get a number drawn at random, but juniors and seniors are ordered by
accumulated credit hours first, and only tie-break randomly. That means a
senior who took summer courses reliably beats a senior who didn't. Numbers come
out the second week of March and selection runs over four evenings.
```

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer — 4 of 5 | **MET** | 5 of 5, three runs out of three. I deliberately did not read this off the `pass`/`fail` column, which says 2 of 5 — that column is the scorer checking answer wording, and criterion 1 is about retrieval. I checked the `Sources retrieved` line for each question and then opened the document it named: `admin_campus_jobs_and_financial_aid`, `admin_declaring_a_major`, `admin_grade_appeals`, `admin_housing_lottery` and `admin_study_abroad` each contain the answer in one sentence, and none of the five is long enough to be split, so the retrieved chunk is the whole document. |
| 2 | Every answer names a source — 5 of 5 | **MET** | 15 of 15 answers across the three runs name a `.txt` file, and in every case it is the document the answer actually came from rather than one of the other four retrieved. The close call was formatting, not sourcing: the model alternates between a trailing `Source: admin_grade_appeals.txt` line and an inline `(admin_grade_appeals.txt)` citation between runs. I counted both, because the criterion says the answer names a source, not that it names it in a fixed place. |
| 3 | Gate stops out-of-corpus questions — 4 of 5 | **MET** | 5 of 5 refused at cutoff 0.6. The nearest miss is nowhere near: the closest out-of-scope question scores 0.825, which is 0.225 clear of the cutoff, so this is not a result that could flip on a re-run. I am recording it as MET against the criterion as written while noting that unit 1 already established the criterion is easy — these five questions are about Mongolia and diesel engines, and the campus questions my corpus doesn't cover (gym hours at 0.487, tuition at 0.536) go straight through the gate. |
| 4 | Chunks end where thoughts end — 9 of 10 | **MET** | 10 of 10 on three independent random samples, seeds 0, 1 and 2, via `check_chunks.py`. The judgment call is the leading edge: every chunk opens with the document's title line, which is a heading with no sentence structure at all. I counted that as a clean start because the criterion's actual test is "no chunk is cut mid-sentence at either edge", and a title line is where the document begins, not a severed sentence. The one allowance I wrote into the criterion — documents ending on a bare list item — never got used; nothing in the three samples ended on anything but a full stop. I also checked the only three documents the chunker splits (Old Brewhouse, Morrow House, Innisfree Hall) directly rather than trusting the sample to reach them, since those are the only places a boundary can do damage; all six of those chunks land on paragraph breaks. |
| 5 | Nothing in the answer that wasn't in the chunks — every answer | **MET** | I read all 15 answers beside the chunk each one cited. Every claim traces: "fifteen days", "end of your second semester", "October for the following academic year", "ordered by accumulated credit hours first". The one that needed a decision is the work-study answer, which opens with "No," — that word appears nowhere in the chunk. I counted it as traced because it restates the chunk's "don't count against your financial aid" as a yes/no, which is a rephrasing of the retrieved sentence rather than a fact from outside it. The rest of the checking was easy in a way that is worth being honest about: all five answers stayed inside a single short document and none tried to combine two chunks, which is the case where this criterion would actually be hard to judge. |

## Diagnoses

**I missed nothing. Five criteria, five MET, first try.** So this section is
about why, and the honest answer is that my criteria were safe rather than my
system being good. I can show that, because the system fails on questions my
criteria never ask it.

### The pattern: every criterion tests the easy case of its stage

Three criteria turned out to be unable to fail, for three different reasons
that all have the same shape.

**Criteria 1, 2 and 5 are all measured on the same five questions, and I wrote
those questions while reading the documents.** I said so in unit 1 without
noticing it was a problem: *"My five were written while reading the documents,
so they reuse the documents' own wording."* That one fact decides all three
criteria before the system runs:

| Question | Rank 1 | Distance | Rank 2 | Margin |
|---|---|---|---|---|
| Does work study income count towards Financial aid | `admin_campus_jobs_and_financial_aid` | 0.2831 | 0.6402 | 0.357 |
| When do can you declare a major | `admin_declaring_a_major` | 0.2663 | 0.4511 | 0.185 |
| How to appeal a grade | `admin_grade_appeals` | 0.3220 | 0.6786 | 0.357 |
| Is the housing lottery random | `admin_housing_lottery` | 0.2501 | 0.6365 | 0.386 |
| When are study abroad applications open | `admin_study_abroad` | 0.2289 | 0.6008 | 0.372 |

Produced by `app.py retrieve` / `store.py::search`. The right document is rank 1
every time, by a margin of 0.19 to 0.39 over whatever is second. Criterion 1
asks for the answer to be somewhere in the top five; it is in fact always first
with the next candidate more than twice as far away. **So tightening criterion 1
from top-5 to top-1 would change nothing — I checked, it still scores 5 of 5.**
The criterion is not loose because the number is loose. It's loose because the
questions are.

The same fact makes criteria 2 and 5 easy. Each of my five answers lives in
exactly one short single-topic document, so the generator is handed one chunk
that contains the whole answer and four that are visibly unrelated. Naming a
source is then trivial — there is only one plausible one. Not inventing
anything is trivial for the same reason: there is no gap to fill and nothing to
synthesise across two chunks. Criterion 5 is the failure I was most worried
about in unit 1, and I never put it in a position to happen.

**Criterion 4 is easy for a structural reason instead.** `split_documents`
packs whole paragraphs and never cuts inside one, so a mid-sentence edge isn't
unlikely — it's unreachable. The criterion tests a property the code guarantees
by construction. On top of that, only 3 of 88 documents are long enough to split
at all, so 88 of 91 chunks are whole documents with nothing to get wrong.

**Criterion 3 is easy because of the question list, not the cutoff.** Mongolia,
diesel engines and Rust score 0.825–0.934 against a 0.6 cutoff. Nothing in that
list is a near miss.

So: **one root cause for 1, 2 and 5 (the questions came from the documents), and
two more criteria that couldn't fail by construction.** Not five findings — one
finding about how I chose what to measure.

### What actually fails, with stage and mechanism

None of these is a criterion miss. All three are real, reproducible, and
outside what I chose to measure.

**1. Two unanswerable campus questions get confidently answered. Stage:
retrieval — specifically the gate.**

```
what time does the gym close     → 0.4873 → dining_halden_hall_followup.txt  → PASSES the gate
how much is tuition per semester → 0.5356 → admin_printing_quota.txt          → PASSES the gate
```

The mechanism is that nearest-neighbour search always returns a neighbour. My
corpus has no gym document and no tuition document, so the query vector lands
somewhere and Chroma hands back whichever of the 91 chunks is least far away
— there is no "none of these" result for the gate to see. `admin_printing_quota`
is about a fixed dollar amount a student is given per term, which is genuinely
close to "how much is tuition per semester" on every axis except the one that
matters. A single global distance threshold cannot separate *near because it
answers the question* from *near because it is about the same kind of thing*,
and criterion 3 never tests it on a question where those two come apart.

> **Correction, after I actually ran these.** I wrote the heading above before
> sending either question to the model, and it is wrong. Unit 1 predicted that
> the tuition question would be "a confidently wrong answer about money" and I
> repeated that prediction here as though it were a finding. It isn't. Asked
> for real, the system refuses both:
>
> ```
> what time does the gym close     → gate passed at 0.4873
>   "I do not have enough information to answer your question, as the provided
>    documents do not mention the gym."
> how much is tuition per semester → gate passed at 0.5356
>   "I do not have enough information to answer how much tuition is per semester."
> ```
>
> So the leak is real but the damage isn't: the gate fails and the grounding
> prompt catches it, which is the two-layer design in `gate.py`'s docstring
> working as written — *"the gate catches the clear misses; the prompt catches
> the near ones."* What this actually shows is that **criterion 3 measures the
> wrong layer.** It asks whether the gate refuses, when what a student cares
> about is whether the system refuses. Scored on the four near-miss campus
> questions, the gate gets 1 of 4 and the system gets 4 of 4.
>
> I am leaving the original claim above rather than editing it, because the
> difference between the two is the whole point: I diagnosed a fabrication I
> had never observed, from a prediction I made in unit 1 and never tested.

**2. A plainly-worded real question retrieves the wrong document. Stage:
embedding.**

```
when do i have to pick what im studying → 0.5467 → course_cs_340.txt → PASSES the gate
```

`admin_declaring_a_major.txt` is the answer and it scores 0.2663 when I use the
registrar's vocabulary. Reworded the way a student would actually type it, that
same document doesn't even make rank 1. The mechanism is vocabulary overlap:
"declare" and "major" appear in the document, "pick" and "studying" do not, and
MiniLM has anchored on "studying" strongly enough to pull a course syllabus
above the document that literally answers the question. This is the same
underlying weakness as failure 1 — the embedding is doing topical similarity,
not question answering — showing up on the retrieval side instead of the gate
side.

> **Correction, same reason as above.** Rank 1 is wrong, but
> `admin_declaring_a_major.txt` is at **rank 3**, inside `TOP_K = 5`, so the
> model sees it and answers correctly: *"You declare a major at the end of your
> second semester, or later if you need to, as there is no penalty for
> declaring late. Source: admin_declaring_a_major.txt"*. The embedding weakness
> is real and the system survives it, because top-k is wide enough to absorb a
> two-place error. Worth knowing: this is the mechanism that **doesn't** bite.

**4. A legitimate question the corpus answers gets refused. Stage: chunking.**

This is the one real end-to-end failure I found, and unlike the three above I
found it by accident while checking that the others weren't over-refusing.

```
cheapest place to live on campus → 0.4779 → passes the gate → the model says:
  "Based on the provided documents, there is no mention of which place is the
   cheapest to live on campus."
```

The corpus does answer it. `housing_morrow_house.txt` contains *"The good:
cheapest housing tier by about $900 a year"*. The mechanism is that under my
chunker that sentence shares a chunk with the building's construction date, its
room types and its damp problem, and the chunk is stored as **one** vector that
averages all four. Averaged with three unrelated facts, the "cheapest" signal is
diluted below four other buildings' overview chunks — `housing_morrow_house.txt`
doesn't appear in the top 12, let alone the top 5.

This is a chunking failure, not an embedding one, and the test that separates
them is that the same sentence is perfectly findable once it is alone in a
chunk. That test is what the improvement below does.

**The pattern across 1, 2 and 4:** all three are the same shape — a question
where the retrieval signal is diluted, either by the corpus having nothing to
match (1), by vocabulary drift (2), or by one vector carrying four facts (4).
Only 4 actually breaks the system, and only 4 is fixable at a stage I control.

**3. My scorer marks correct answers wrong. Stage: none of the five — this is
the measurement, not the pipeline.**

`scorer.py::judge` is `expects.strip().lower() in answer.strip().lower()`, an
exact substring test, and my `expects` values for questions 2–5 are full
sentences copied out of the documents. The model paraphrases, so
`"The housing lottery is not random in the way most people assume"` fails
against the produced `"The housing lottery is not entirely random."` Three of
five questions are marked `fail` in every run and all three are correct,
sourced and faithful. Worth separating from the others: the pipeline did its
job and the ruler was wrong. I caught it only because criterion 1 is about
retrieval, so I went and read the retrieved sources instead of trusting the
column. Had criterion 1 been phrased about answer text, I would have recorded
three misses that never happened.

### Which criterion I'd tighten, and to what

**Criterion 3, by replacing the question list rather than moving the number.**

> For at least 4 of 5 questions that a student could plausibly ask about campus
> life but that my corpus contains no document about, the gate refuses.

Keep "4 of 5". The target was never the problem. On the three such questions I
have measured, today's system scores **1 of 3** — gym hours and tuition both go
through, only "who is the university president" (0.742) is refused. That is a
criterion that can fail, and on current evidence it does.

Runner-up, and the one that would teach me more if I had time for both:
criterion 1 re-measured on five questions worded the way a student would type
them rather than the way the documents are written. I can't tighten it by asking
for a better rank, because rank 1 with a 0.19 margin is already the ceiling;
the only way to make it bite is to stop feeding the retriever its own words.

<!-- Note: criteria.md is unchanged. These are tightenings I'd make, not
     revisions — none of my five turned out to be unmeasurable, which is what
     the revision mechanism there is for. -->

## The Improvement

**What I changed:** a second chunking strategy, built as a parallel index so
both can be queried against the same questions, plus the one retrieval setting
the first change turned out to depend on.

1. **`chunker.py::split_paragraphs`** — one body paragraph per chunk, with the
   document's title line prepended, no packing and no minimum-size merge. This
   is strategy B; `split_documents` from Milestone 3 is unchanged and is still
   strategy A. `app.py index --variant paragraph` builds B into its own Chroma
   collection via the new `chunker.py::split_for_variant`, so nothing is
   overwritten and both indexes can be compared side by side.
2. **`config.TOP_K` 5 → 8.** Not a separate idea — the A/B below shows the
   chunking change alone doesn't deliver the fix, and top-k alone doesn't
   either.

Both are live in `config.py`, not just flags I typed once: `TOP_K = 8` and a
new `INDEX_VARIANT = "paragraph"` that `app.py` and `run_eval.py` now take
their default from. So plain `python app.py ask "..."` uses the new strategy,
and `--variant default` still queries the Milestone 3 index, which is the whole
reason for building it as a variant rather than editing the old chunker.

| | Strategy A (`default`) | Strategy B (`paragraph`) |
|---|---|---|
| Chunker | `chunker.py::split_documents` | `chunker.py::split_paragraphs` |
| Chunks | 91 | 183 |
| Average length | 307 chars | 167 chars |
| Shortest / longest | 159 / 430 | 63 / 397 |

**Why I picked it:** diagnosis 4 — "cheapest place to live on campus" is
refused because the sentence answering it is averaged into one vector with
three unrelated facts about the same building, and one fact per chunk is the
direct undoing of that.

This is also the strategy I argued *against* in Milestone 3, on the grounds
that the corpus's paragraphs are too short to embed usefully. Half of that
objection died when I added the title line to every chunk in Milestone 3; the
other half — "too thin to embed" — I had asserted without testing. Diagnosis 4
is the case that makes it worth testing, so this improvement is partly me
going back to check my own unit 1 reasoning.

### Logs after Improvments
Does work study income count towards Financial aid
  run 1: pass  (best distance 0.283)
  run 2: pass  (best distance 0.283)
  run 3: pass  (best distance 0.283)

When do can you declare a major
  run 1: fail  (best distance 0.266)
  run 2: fail  (best distance 0.266)
  run 3: fail  (best distance 0.266)

How to appeal a grade
  run 1: fail  (best distance 0.322)
  run 2: fail  (best distance 0.322)
  run 3: fail  (best distance 0.322)

Is the housing lottery random
  run 1: fail  (best distance 0.250)
  run 2: fail  (best distance 0.250)
  run 3: fail  (best distance 0.250)

When are study abroad applications open
  run 1: pass  (best distance 0.229)
  run 2: pass  (best distance 0.229)
  run 3: pass  (best distance 0.229)

Out-of-scope questions (the gate should refuse these):
  refused  (best distance 0.787)  What is the capital of Mongolia?
  refused  (best distance 0.923)  How do I change the oil in a diesel engine?
  refused  (best distance 0.847)  Who won the 1994 World Cup?
  refused  (best distance 0.849)  What is the recommended dosage of ibuprofen for a headache?
  refused  (best distance 0.860)  How do I write a for loop in Rust?

### The A/B, on retrieval only

Both indexes, same questions, no model calls — retrieval is deterministic and
runs locally, so this part is free and repeatable. "In top-k" means the
document that actually answers the question came back.

| Question set | n | A @ k=5 | B @ k=5 | A @ k=8 | B @ k=8 |
|---|---|---|---|---|---|
| In corpus, document wording | 5 | 5 | 5 | 5 | 5 |
| In corpus, student wording | 10 | 9 | 9 | **9** | **10** |
| Not in corpus — gate refuses | 10 | 7 | 7 | 7 | 7 |

**The fix needs both halves, and the table is how I know.** At k=5 the new
chunker changes nothing: 9 of 10 either way. At k=8 the old chunker still
changes nothing: 9 of 10. Only B at k=8 gets 10 of 10. The reason is visible in
the ranks for the one question that moves:

```
cheapest place to live on campus
  strategy A:  housing_morrow_house.txt not in the top 12 at all
  strategy B:  housing_morrow_house.txt at rank 8, distance 0.6463

the same chunk, queried with the document's own words:
  strategy B:  rank 1, distance 0.4607
               "Morrow House — what it's actually like
                The good: cheapest housing tier by about $900 a year, and the
                singles are real singles."
```

Splitting the paragraph out is what makes the fact *reachable* — it goes from
unranked to rank 8. Widening top-k is what makes it *reached*. Either change on
its own leaves the question broken.

**What got worse.** Shorter chunks sit slightly closer to everything, including
things they should be far from: "What is the capital of Mongolia?" went 0.825 →
0.787 and "How do I write a for loop in Rust?" went 0.896 → 0.860. Still
refused, but the out-of-scope group moved toward the cutoff rather than away
from it. One legitimate question also regressed — "is the dorm with the brewery
history loud", 0.381 → 0.413 — because that answer was already alone in its own
small document and splitting gained nothing while shortening the text it had to
match against. The gains are concentrated exactly where the diagnosis said they
would be, on chunks that previously carried several facts: "how loud is morrow
house at night" 0.361 → 0.248, "do i need an adviser to register" 0.486 → 0.352.

### Run Log — After

`python run_eval.py --label after --variant paragraph --top-k 8` →
`results/run_2026-09-23_1847_after.md`. Criterion 4 from
`python3 check_chunks.py --variant paragraph`. The flags were explicit when I
ran it; they are now the defaults in `config.py`, so `python run_eval.py
--label after` reproduces it.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 2. Every answer names a source | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 4. Chunks end where thoughts end | 9 of 10 | 10 of 10 | 10 of 10 | 10 of 10 | MET |
| 5. Nothing in the answer that wasn't in the chunks | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |

Real output — the question the change was made for, before and after:

```
BEFORE  (strategy A, k=5)   gate passed at 0.4779, top hit housing_aldridge_hall.txt

  Based on the provided documents, there is no mention of which place is the
  cheapest to live on campus.

  Source: housing_aldridge_hall.txt, housing_tamsin_court.txt,
  housing_fenwick_court.txt, housing_old_brewhouse.txt

AFTER   (strategy B, k=8)   gate passed at 0.4638, top hit housing_tamsin_court.txt

  Morrow House is the cheapest housing tier on campus by about $900 a year
  (housing_morrow_house.txt).
```

**Did it help?**

Yes, but not on any criterion — and that gap is the honest headline.

**The five criteria are identical before and after: 5, 5, 5, 10-of-10, 5.** A
grader comparing only the two run-log tables would conclude I changed nothing.
The change is real and I can point at it, but it lives entirely outside what I
chose to measure in unit 1 — which is the same finding as the Diagnoses
section, arriving a second time from the other direction.

What I can show:

- **The failure it targeted is fixed.** "Cheapest place to live on campus" went
  from a refusal to the correct answer with the correct source. That's the
  before/after block above, and it's the whole reason for the change.
- **Student-worded retrieval went 9 of 10 to 10 of 10** on my ten-question set.
  One question, so I'd call it directional rather than proven.
- **Nothing regressed.** This mattered more than I expected: going from 5 to 8
  chunks hands the model three more distractors per question, and criterion 5
  is exactly the criterion that should catch a model wandering into them. It
  didn't — all 15 after-answers trace to their cited chunk, with 6 to 8 sources
  retrieved per question instead of 5. Criterion 4 also holds at 10 of 10 on
  183 chunks, which it had to: `split_paragraphs` cuts only at blank lines, so
  it cannot produce a mid-sentence edge any more than `split_documents` could.
- **The near-miss refusals survived too**, which is the check I most expected
  to fail — three extra chunks is three more chances for the model to find
  something it can pretend answers the question:

  ```
  what time does the gym close                          → gate passed at 0.5324
    "I do not have enough information to answer your question."
  how much is tuition per semester                      → gate passed at 0.5356
    "I don't have enough information to answer your question."
  what is the deadline to apply for a dorm room change  → gate passed at 0.5790
    "I don't have enough information to answer your question, as the provided
     documents do not mention deadlines for dorm room changes."
  when do i have to pick what im studying               → gate passed at 0.5675
    "You declare your major at the end of your second semester, or later if you
     need to. Source: admin_declaring_a_major.txt"
  ```
- **The out-of-scope margin narrowed.** Not enough to flip anything, but the
  cheapest out-of-scope question moved from 0.825 to 0.787 against a 0.6
  cutoff. If I pushed chunks smaller still, this is the number that would
  break first, and I'd want criterion 3 rewritten against near-miss campus
  questions before trying it.

One thing I deliberately did not change: `scorer.py`, even though diagnosis 3
says it is broken and it marks three correct answers `fail` in both run logs.
Fixing the ruler halfway through the experiment would have made the before and
after logs incomparable, which is the one thing this milestone needs them to
be. It stays broken on purpose until the comparison is done, and it's the first
thing in What's Still Broken.

## What's Still Broken

**No criterion is still missed, because none was missed to begin with.** That
sentence is worth nothing on its own, so here is the list of things that are
actually wrong with this system, none of which any of my five criteria can
see. They are ordered by how much they'd bother a student using it.

### 1. The gate refuses questions the retriever got right

This is the worst one, it is the opposite of the failure criterion 3 watches
for, and I found it in the last hour.

```
cutoff 0.6, top-k 8, variant paragraph

REFUSED  best=0.7696  answering document at rank 1  "i got a bad mark can i complain"
REFUSED  best=0.6061  answering document at rank 3  "what happens if i quit a class halfway through"
passed   best=0.5743  answering document at rank 1  "can i take a class without it wrecking my gpa"
```

Retrieval put `admin_grade_appeals.txt` **first** for "i got a bad mark can i
complain" and the gate threw it away, because 0.7696 is over the cutoff. The
mechanism is that the gate reads a distance, not a ranking: MiniLM scores
"bad mark" and "grade appeal" as barely related even while ranking the right
document top, so the number the gate consults disagrees with the ordering the
retriever just produced. The third line is the same failure 0.026 away from
happening.

**What I'd do:** stop gating on absolute distance alone. The information the
gate is missing is already sitting in the result list — the retriever knew
which document was best; only the threshold disagreed. Something like "refuse
only if the best result is both far away *and* no better than its neighbours"
would use it.

**Why I stopped:** I tested exactly that and it doesn't work, so I'm not
pretending it's a ready fix. Rank-1-to-rank-2 margins for legitimate questions
run 0.013–0.298 and for unanswerable ones 0.003–0.116 — the two ranges sit
almost entirely on top of each other, so any margin rule strict enough to
catch the leaks refuses real questions too. Those are the numbers; there is no
fix to show because the idea died on measurement. The honest next step is a
different embedding model, which `config.EMBEDDING_MODEL` supports as the
stretch option, followed by re-running the whole A/B; that's a unit's work,
not an evening's.

### 2. `scorer.py` is still broken, on purpose

It marks three of five correct answers `fail` in both run logs, by exact
substring match against sentences I copied out of the documents. Diagnosis 3
has the mechanism.

**What I'd do:** score against a handful of key facts per question rather than
one verbatim sentence — for the housing lottery, `["not random", "credit
hours", "tie"]` — so paraphrase passes and a wrong answer still fails.

**Why I stopped:** deliberate, and I'd make the same call again. Fixing the
ruler between the before and after runs would have made the two run logs
incomparable, which is the one property this unit needs them to have. It is
the first thing I'd change next, before any pipeline work.

### 3. Refusals are ad-hoc text, so nothing downstream can detect them

`gate.REFUSAL` is one fixed string, but the refusals that actually reach a
student mostly come from the model instead, and it words them differently
every time — I measured "I do not have enough information to answer your
question.", "I don't have enough information to answer your question.", and a
longer one naming what was missing. Worse, one refusal arrived with citations
attached:

```
Based on the provided documents, there is no mention of which place is the
cheapest to live on campus.

Source: housing_aldridge_hall.txt, housing_tamsin_court.txt, ...
```

A refusal that cites four sources is incoherent output, and no program can
tell that string apart from an answer.

**What I'd do:** instruct the prompt to emit `gate.REFUSAL` verbatim and to
cite nothing when it refuses. Then criterion 3 becomes measurable end-to-end
instead of only at the gate.

**Why I stopped:** one improvement per unit. Changing the prompt at the same
time as the chunker would have left me unable to attribute either result, and
the A/B in the previous section is the thing I most wanted to be able to
trust.

### 4. The `Re:` follow-up documents, carried over from unit 1

Seven of the 88 documents open by pointing at a sentence in a different
document. I flagged this in Milestone 3, said I'd leave it for unit 2, and
then didn't do it. It is not harmless: `dining_halden_hall_followup.txt` is
the top hit for "what time does the gym close", which is a question about
neither dining nor Halden Hall — thin, context-free chunks attract unrelated
queries.

**What I'd do:** detect the `Re:` prefix in `ingest.py` and stitch each
follow-up onto the document it answers, before chunking.

**Why I stopped:** ran out of time, and it's a loading-stage change while my
diagnosis pointed at chunking. Following the diagnosis was the right call, but
this was the runner-up and it stayed unfixed.

### 5. Two smaller things

- **Shorter chunks moved the out-of-scope group toward the cutoff** — Mongolia
  0.825 → 0.787, Rust 0.896 → 0.860. Nothing flipped, and criterion 3 still
  reads 5 of 5, but the safety margin shrank. If I split chunks further this is
  the number that breaks first, and I'd want criterion 3 rewritten before
  trying.
- **`config.REQUESTS_PER_MINUTE` is 30; the free tier for
  `gemini-3.5-flash-lite` is 15.** I hit a hard 429 mid-run and lost a test
  batch to it. One-line fix, no bearing on any criterion, but it will bite
  whoever runs this next.

## What I'd Do Differently

Every one of my five criteria passed on the first attempt, so the short answer
is that I'd write all five to be harder to pass. The specific answer is that
three of them were unfalsifiable for three different reasons, and only one of
those is about the number I chose.

**Criterion 3 — the one I'd change first.** It asks whether the *gate* refuses,
and tests it on Mongolia and diesel engines. Both halves are wrong. Scored on
campus questions my corpus doesn't cover, the gate gets 1 of 4 while the
system gets 4 of 4, so the criterion credits the wrong layer with work the
grounding prompt is doing. I'd rewrite it as: *for at least 4 of 5 plausible
campus questions my corpus contains no document about, the system returns a
refusal* — and I'd add its mirror image, which nothing in my five covers at
all: *no question whose answering document is retrieved gets refused.* That
second one fails today, twice, and it is the failure a real student would
actually notice.

**Criterion 1 — right target, wrong questions.** 4 of 5 was never loose; I
proved that by tightening it to top-1 and still scoring 5 of 5. What made it
free is that I wrote the questions while reading the documents, so retrieval
was matching the corpus against its own vocabulary. I'd write the questions
before reading anything, or better, have someone who hasn't seen the corpus
write them. My ten student-worded questions are a rough version of this and
they score 10 of 10 only after this unit's fix — 9 of 10 before it. That is a
criterion that moves when the system changes, which is the whole job.

**Criterion 5 — unfalsifiable as I ran it.** Every one of my five questions is
answered by a single short document, so the model was never asked to combine
two chunks and never had a gap to fabricate into. I checked 15 answers for
invented facts under conditions where inventing one would have been strange.
I'd require at least two questions whose answer spans two documents — "which
building is cheapest and how loud is it" needs Morrow's price paragraph and
Morrow's noise document — because that is where grounding actually gets
tested.

**Criterion 4 — I'd replace it, not tighten it.** It checks that chunks don't
end mid-sentence, and `split_documents` cuts only at blank lines, so a
violation isn't unlikely, it's unreachable. I wrote a criterion my code
satisfies by construction. The test worth keeping is the one I did informally
in Milestone 3 and never turned into a criterion: can each chunk be understood
on its own? Seven documents demonstrably fail that, which means it is a
criterion with something to find.

**Criterion 2 is the one I'd leave alone.** "Every answer names a source" is
cheap to satisfy here, but it's 15 of 15 across two different chunkings and
two top-k settings, it caught the formatting drift between `Source:` lines and
inline citations, and a criterion that keeps holding while everything around
it changes is doing useful work as a regression check.

The general lesson, and the thing I'd carry into the next project: I wrote five
criteria about whether the pipeline works, and not one about whether I could
tell if it didn't. The broken scorer sat in both run logs marking correct
answers wrong, and no criterion noticed, because measuring the measurement
wasn't on my list.
