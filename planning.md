# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

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

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

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

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
