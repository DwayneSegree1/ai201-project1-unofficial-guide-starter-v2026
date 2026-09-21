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

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
