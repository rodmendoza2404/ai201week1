# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

This project covers student-generated knowledge about FIU Computer Science courses and professors. Official FIU resources ,course catalogs, department pages, syllabi,describe what a course covers, but they do not tell students which professors are actually helpful, which courses have crushing workloads, whether exams are curved, or which combinations of classes are survivable in one semester.

That knowledge exists, but it is scattered across Reddit threads and Rate My Professors reviews with no way to search across all of it at once. This system collects those student voices into a single RAG pipeline so a student can ask a plain-language question and get a grounded, cited answer drawn from real peer experiences.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Reddit thread about FIU Computer Science major experience | documents/fiu_cs_major_experience.txt | https://www.reddit.com/r/FIU/comments/1f5j4vt/how_is_computer_science/ |
| 2 | Reddit thread asking which FIU CS professors are good | documents/fiu_cs_professors_good.txt | https://www.reddit.com/r/FIU/comments/1g7kep6/what_cs_professors_are_actually_good/ |
| 3 | Reddit thread about hardest FIU CS classes | documents/fiu_hardest_cs_classes.txt | https://www.reddit.com/r/FIU/comments/j55ivh/computer_science_majors_hardest_classes/ |
| 4 | Reddit thread about taking CDA 3102, COP 3530, and COP 4338 together | documents/fiu_three_courses_workload.txt | https://www.reddit.com/r/FIU/comments/126o8sv/are_these_3_courses_doable_in_one_semester/ |
| 5 | Reddit thread about picking FIU CS professors | documents/fiu_help_picking_cs_professors.txt | https://www.reddit.com/r/FIU/comments/jry3og/help_picking_cs_professors/ |
| 6 | Rate My Professors reviews for Antonio Hernandez | documents/antonio_hernandez_reviews.txt | https://www.ratemyprofessors.com/professor/2370429 |
| 7 | Rate My Professors reviews for Antonio Bajuelos | documents/antonio_bajuelos_reviews.txt | https://www.ratemyprofessors.com/professor/2007165 |
| 8 | Rate My Professors reviews for Mark Weiss | documents/mark_weiss_reviews.txt | https://www.ratemyprofessors.com/professor/129106 |
| 9 | Rate My Professors reviews for Eric Ackerman | documents/eric_ackerman_reviews.txt | https://www.ratemyprofessors.com/professor/3004879 |
| 10 | Rate My Professors reviews for Niemah Osman | documents/niemah_osman_reviews.txt | https://www.ratemyprofessors.com/professor/3027499 |


---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 400 characters

**Overlap:** 80 characters

**Why these choices fit your documents:** 
My documents are short-form opinion text . Reddit comments (2-6 sentences) and Rate My Professors reviews (3-8 sentences).  A 400-character chunk captures roughly one complete review or one substantive comment without merging unrelated opinions together into a single embedding. Smaller chunks (e.g., 150 characters) would fragment individual sentences and cause the embedding to carry too little meaning to match well against queries. Larger chunks (e.g., 800+ characters) would merge multiple reviews covering different aspects like granding, treaching style,exam format, into one embedding, diluting retrieval precision when a query asks about only one of those aspects. The 80-character overlap ensures that if a key opinion spans a chunk boundary, at least one of the two adjacent chunks contains enough context to be retrieved.
 
**Final chunk count:** 86 chunks across 10 documents

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2 via sentence-transformers

**Production tradeoff reflection:**

all-MiniLM-L6-v2 is fast, free, and runs entirely locally with no API key or rate limits — ideal for a class project. In a production deployment I would weigh the following tradeoffs when choosing a different model:

Accuracy vs. cost: OpenAI's text-embedding-3-small delivers meaningfully higher retrieval accuracy for a small per-token fee. For a high-traffic student advising tool, the quality improvement would likely justify the cost.
Multilingual support: FIU has a large Spanish-speaking student population. If reviews were written in Spanish, paraphrase-multilingual-MiniLM-L12-v2 would handle cross-language queries; the current model would fail silently on non-English content.
Context length: all-MiniLM-L6-v2 is optimized for short passages up to ~256 tokens, which fits professor reviews well. If documents were long PDFs (syllabi, handbooks), a model with a longer context window like text-embedding-3-large would preserve more meaning per embedding.
Latency: Local models eliminate API round trips, which matters for a real-time interface. If switching to an API-based model, response time for embedding at query time adds ~100–300ms per request.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
The prompt sent to the LLM explicitly restricts it to the retrieved context only:

You are a helpful assistant for FIU Computer Science students.
Answer the question using ONLY the information in the documents below.
If the documents do not contain enough information to answer, say exactly:
"I don't have enough information on that topic in my documents."
Always end your answer by listing which sources you used.

**How source attribution is surfaced in the response:**
Source attribution is handled in two ways. First, the prompt instructs the LLM to list which source documents it drew from at the end of its response. Second, the query.py retrieval function programmatically extracts and deduplicates source filenames from the metadata of the top-5 retrieved chunks and returns them separately as a sources list. The Gradio UI displays this list in a dedicated "Sources used" panel alongside the answer, so attribution is visible even if the LLM omits it from its own response text.
---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do students say about Mark Weiss's exams? | Exams are difficult; half MC, half code; no syntax deductions; drops highest/lowest grade; fair grader | Exams are difficult but fair; half MC, half code; no syntax deductions; drops highest and lowest program and quiz grade | Relevant | Accurate |
| 2 | Is taking CDA 3102, COP 3530, and COP 4338 in the same semester a bad idea? | Reddit consensus is that the combination is very heavy and not recommended | The documents suggest it may be challenging, especially while working part-time, but hedged rather than giving a clear recommendation against it | Partially relevant | Partially accurate |
| 3 | What are the hardest CS classes at FIU according to students? | CDA 3102, COP 3530, and COP 4338 are commonly cited | "I don't have enough information on that topic in my documents" — despite the correct source being retrieved | Partially relevant | Inaccurate |
| 4 | What do students say about Antonio Hernandez as a professor? | Good lecturer, math-heavy, homework spread out, exams based on slides, positive overall | Good professor, teaches data structures well, math-heavy lectures, homework spread out, quizzes based on slides, very positive | Relevant | Accurate |
| 5 | Which CS professors at FIU do students recommend most? | Specific professors named in Reddit threads with reasons | Named Kianoosh, Gregory Murad Reis, Sergio Pisano, and Hernandez with specific reasons from documents | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** "What are the hardest CS classes at FIU according to students?"

**What the system returned:** "I don't have enough information on that topic in my documents." — even though `fiu_hardest_cs_classes.txt` and `fiu_cs_major_experience.txt` were both retrieved in the top 5 chunks.

**Root cause (tied to a specific pipeline stage):** This is a chunking and retrieval interaction failure. The file `fiu_hardest_cs_classes.txt` was retrieved, but the specific chunks pulled from it did not contain the direct list of hard courses — they contained surrounding context (comments about course difficulty in general, or about workload) rather than the core sentences naming CDA 3102, COP 3530, and COP 4338 as the hardest courses. Those key sentences were split across chunk boundaries, and neither resulting chunk contained enough of the original claim to satisfy the LLM's grounding threshold. Because the prompt instructs the LLM to say "I don't have enough information" when the documents don't contain a clear answer, the model correctly followed its instruction — but the root failure was that the relevant chunk content was fragmented by the fixed-character chunker rather than split at natural sentence or paragraph boundaries.

**What you would change to fix it:** Switch from fixed-character chunking to sentence-aware chunking using a library like `nltk.sent_tokenize` or LangChain's `RecursiveCharacterTextSplitter`. This would keep complete sentences together within a chunk, preventing a critical fact like "the hardest courses are CDA 3102 and COP 3530" from being split mid-sentence across two chunks where neither half is retrievable on its own.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
Writing the chunking strategy section before touching any code forced a concrete decision about chunk size before I saw how the data actually looked. Setting 400 characters and 80 overlap in planning.md meant that when I implemented `chunk.py`, I wasn't guessing — I had a reasoned choice already made. It also gave me a baseline to evaluate against: when I printed the 5 sample chunks and they looked coherent, I could confirm the spec was right rather than adjusting arbitrarily.
 

**One way your implementation diverged from the spec, and why:**

The spec described the anticipated challenge of Rate My Professors noise — very short reviews like "Great professor! 10/10" embedding poorly. In implementation, I added a `len(chunk) > 50` filter in `chunk.py` to drop fragments under 50 characters. The spec mentioned this as a possibility but named 100 characters as the threshold to consider. After seeing the actual chunk output, 50 characters turned out to be the right cutoff — it removed true fragments (broken overlap tails) without discarding legitimately short but substantive reviews.
 
---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*  My Documents section (10 source files, all .txt, mix of Reddit threads and Rate My Professors reviews) and my Chunking Strategy section (400-character chunks, 80-character overlap, reasoning about short-form opinion text).
- *What it produced:* A working `ingest.py` that loads all .txt files from the documents/ folder, strips source header lines (SOURCE:, PROFESSOR/TOPIC:, ---), and returns a list of `{text, source}` dicts. Also produced `chunk.py` with the fixed-character sliding window implementation and a 50-character minimum filter.
- *What I changed or overrode:* The generated `clean()` function originally removed any line starting with a capital letter followed by a colon, which was too aggressive — it was stripping course codes like "COP3530:" from review headers. I narrowed the filter to only strip the specific header labels I had defined (SOURCE:, PROFESSOR/TOPIC:) rather than applying a broad pattern.

**Instance 2**

- *What I gave Claude:* My Retrieval Approach section (all-MiniLM-L6-v2, top-k=5, ChromaDB), the architecture diagram showing the five pipeline stages, and the grounding requirement (answer only from retrieved context, cite sources, return "I don't have enough information" when context is insufficient).
- *What it produced:* Working `embed.py` that embeds all chunks and stores them in a persistent ChromaDB collection with source and chunk_index metadata. A `query.py` with `retrieve()` and `ask()` functions and a Groq API call using `llama-3.3-70b-versatile`. A Gradio `app.py` with the two-panel layout.
- *What I changed or overrode:* The generated prompt template initially instructed the model to "prefer" information from the documents, which is too weak — in testing it caused the model to blend retrieved content with general LLM knowledge about CS courses. I changed the instruction to "answer using ONLY the information in the documents below" and added the explicit fallback phrase for out-of-scope queries. This tightened grounding significantly and produced the correct refusal response on out-of-scope test queries.
