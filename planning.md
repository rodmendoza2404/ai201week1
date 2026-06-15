# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

My domain is student-generated advice about FIU Computer Science courses and professors. This knowledge is valuable because official FIU course catalogs and department pages explain course descriptions, credits, and prerequisites, but they do not explain what students actually experience in the class.

Students usually want to know things like which professors are helpful, which courses have heavy workloads, whether exams are difficult, whether assignments are manageable, and what advice previous students would give before registering. This information is hard to find because it is scattered across Reddit threads, Rate My Professors reviews, and informal student conversations instead of being organized in one searchable place.

The goal of this project is to build a RAG system that lets a student ask plain-language questions about FIU CS classes and professors and receive grounded answers based only on the collected student-generated sources.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
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

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**400 characters  

**Overlap:**80 characters

**Reasoning:** My documents are short-form opinion text — Reddit comments (2–6 sentences) and professor reviews (3–8 sentences). A 400-character chunk captures roughly one complete review or one substantive comment without merging unrelated opinions. Smaller chunks (e.g., 150 characters) would fragment single sentences and lose context. Larger chunks (e.g., 800+) would merge multiple reviews about different aspects (grading, teaching style, exams) into one embedding, diluting retrieval precision. The 80-character overlap ensures that if a key opinion spans a chunk boundary, at least one of the two chunks contains enough context to be retrieved.


---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2

**Top-k:** 5

**Production tradeoff reflection:** all-MiniLM-L6-v2 is fast, free, and runs locally — ideal for a class project. In production I would weigh: (1) OpenAI's text-embedding-3-small for higher accuracy at low cost if budget exists; (2) a multilingual model like paraphrase-multilingual-MiniLM-L12-v2 if students write reviews in Spanish; (3) a longer-context model if documents were dense PDFs rather than short reviews; (4) latency — local models eliminate API round trips, which matters for a real-time query interface.


---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do students say about Mark Weiss's exams? | Reviews mention that Weiss's exams are difficult and require understanding of data structures; some mention curving. |
| 2 | Is taking CDA 3102, COP 3530, and COP 4338 in the same semester a bad idea? | Reddit consensus is that the combination is very heavy and not recommended; students advise spreading them out. |
| 3 | What are the hardest CS classes at FIU according to students? | Commonly cited: CDA 3102 (Computer Organization), COP 3530 (Data Structures), and COP 4338 (Systems Programming). |
| 4 | What do students say about Antonio Hernandez as a professor? | Reviews mention he is a good lecturer but exams are challenging; students recommend attending every class. |
| 5 | Which CS professors at FIU do students recommend most? | Reddit threads point to specific professors with high engagement; Rate My Professors confirms with high ratings. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. **Chunk boundary splits:** A professor review that starts with "His exams are…" and continues with "…curved but fair" might be split across two chunks, with neither chunk containing the full picture. The 80-character overlap mitigates this but doesn't eliminate it.

2. **Rate My Professors noise:** Some reviews are very short ("Great professor! 10/10") with no substantive detail. These will embed poorly and may be retrieved for the wrong queries. I may need to filter out reviews under 100 characters.


---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

I will give Claude my Documents section and Chunking Strategy section and ask it to implement `ingest.py` (loads all .txt files from documents/, cleans whitespace and source headers, returns a list of {text, source} dicts) and `chunk.py` (splits each document into 400-char chunks with 80-char overlap, preserves source metadata).

**Milestone 4 — Embedding and retrieval:**

I will give Claude my Retrieval Approach section and architecture diagram and ask it to implement `embed.py` (loads chunks from chunk.py, embeds with all-MiniLM-L6-v2, stores in ChromaDB with source and chunk_index metadata) and a `retrieve()` function in `query.py` that accepts a query string and returns top-5 chunks with source info.

**Milestone 5 — Generation and interface:**

I will give Claude the grounding requirement (answer only from retrieved context, cite sources) and ask it to implement the `ask()` function in `query.py` (builds prompt with retrieved chunks, calls Groq API, returns answer + source list) and `app.py` (Gradio UI wiring).