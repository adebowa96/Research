# HFCS paper and APHA poster: revision notes

Files:
- `HFCS_Paper_Revised.docx` / `.pdf`: revised research paper
- `HFCS_APHA_Poster_Revised.pptx` / `.pdf`: revised poster

Your submitted abstract is copied word for word on the poster and in the paper. None of the study numbers changed:
454,324 identified → 447,607 eligible → 29,503 with HFCS (6.6%) / 418,104 without (93.4%).
All of these check out arithmetically (29,503 + 418,104 = 447,607; 29,503 / 447,607 = 6.59%; about 1 in 15.2).

## You still need to do these

1. **Author names.** The poster title still says "Name of Student(s)". Your co-author's comment asks "where are our names". The paper's title page has a yellow placeholder too.
2. **Reference 2 (market report).** It says it was published December 1, 2025 but accessed August 30, 2025, which is impossible. Put in the real access date (highlighted yellow).
3. **Reference 18 (Dietary Guidelines 2025–2030).** Add your access date (highlighted yellow).
4. **Confirm the 6,717 exclusions.** This is 454,324 − 447,607. If you know how many were New Zealand products and how many were "Drug", report the two numbers separately.
5. **Optional validation.** See the search-strategy issue below. Re-running the search as an exact phrase (`"high fructose corn syrup"`), or hand-checking a random sample of about 100 HFCS-positive records, would show how accurate the 29,503 count is.
6. Remove the yellow highlights once these are done.

## Accuracy fixes in the paper

- **Search method was described incorrectly.** The paper called `"High" AND "Fructose" AND "Corn" AND "Syrup"` an "exact phrase" search that "ensured only products directly listing HFCS" were found. It is not an exact-phrase search. It matches any ingredient list that contains all four words anywhere. For example, a list with "corn syrup, fructose, high oleic oil" would match. The Methods now describe the query accurately, and the Limitations explain that it may over-count (words not next to each other) or under-count (HFCS listed as "HFCS", "glucose-fructose syrup" or "isoglucose").
- **Contradictory eligibility wording.** The paper said the market-country filter "was set to the United States, while New Zealand was excluded". It now says New Zealand-market and "Drug" products were excluded, and the exclusion count (n = 6,717) is reported in Results.
- **Citations that did not support the claim:**
  - The regional market shares (38/27/23/12%) cited ref 11. Ref 11 is a JAMA Network Open commentary on metabolic syndrome, not a market source. They now cite ref 2 only.
  - The Asia-Pacific growth claim cited ref 10 (Rippe 2010, a clinical review). It now cites ref 2.
  - The sentence saying high-fructose sweeteners are "key drivers" of obesity cited refs 5 and 10, both of which conclude that HFCS and sucrose have similar effects. It is reworded to match what those sources say.
- **Truncated sentence fixed.** "The main source of risk is excess added." now reads "… excess added sugar intake overall." I also added the one difference the Li 2022 meta-analysis did find (higher CRP with HFCS).
- **Duplicated sentence removed** from the strengths paragraph.
- **Dietary Guidelines updated.** The 2025–2030 Dietary Guidelines came out on January 7, 2026. They say no amount of added sugars is recommended and set a limit of 10 g of added sugars per meal. They are now cited next to the 2020–2025 guideline. The poster's "less than 10% of calories" line was out of date and has been replaced.
- **Added limitation:** GBFPD counts individual items (package sizes and product codes) and may include products no longer sold.

## References (checked against published records)

- Ref 3 was a Medium blog post. It is replaced with White JS, *Am J Clin Nutr* 2008;88(6):1716S-1721S, a peer-reviewed source for the HFCS-42/HFCS-55 facts.
- Ref 12 (Fukagawa) was in Harvard style with the wrong year. Corrected to AMA style: 2022;115(3):619-624.
- Ref 19 (Steele): first author corrected to "Martínez Steele E".
- Ref 1 now lists all six authors, as AMA style requires for six or fewer.
- Removed the `?utm_source=chatgpt.com` tracking tails from every URL.
- References were renumbered after the new Dietary Guidelines reference (18) was added.
- Verified that these exist as cited: Wang 2022, Li 2022, Aoyagi 2025, Lancaster 2020 (e2010224), Larrick 2022, Nguyen 2023, Fukagawa 2022, White 2008.

## Formatting and language in the paper

- Added a title page and the abstract, followed by keywords.
- The Discussion and Conclusion paragraphs were styled as "Heading 4". They are now normal body text.
- British spellings changed to American ("grammes", "labelling", "emphasise", "standardised", "behaviour").
- Fixed "its a relevant", "these finding", "U.S food" and informal contractions.
- Added subheadings to Methods and Discussion. The references are in AMA 11th-edition style with hanging indents, and pages are numbered.

## Poster: co-author comments (Roberts)

| Comment | What was done |
|---|---|
| "make the words larger nobody can read these" | Body text raised from 18–20 pt to 28 pt (Introduction, Methods), 36 pt (Future Work) and 40 pt (Results). The Abstract stays word for word at 20 pt. |
| "where are our names" | **Still needed from you**, see item 1 above |
| "remove the references … enlarge the other text" | References panel removed and the space given to larger text |
| "remove this image, it's the same as the one beside it" | Donut chart removed. The bar chart is now centered and larger. |

## Other poster fixes

- Deleted leftover template items hidden behind the figures, including the "MG1655 ∆qseC … CFU" bacteria text, an empty "MG1655 µ on 0.02% Lactose" chart, stray letters (A, B, s, 7, 4) and an axis strip numbered 1–14.
- The flowchart no longer has the footnote "*Derived…; not reported directly in the paper"; the paper now reports the 6,717.
- Methods now match the paper: correct search description and exclusions stated clearly.
- The Results bullet for "418,104 products" had lost its bullet point; restored.
- Added a conclusion bullet about term-based search accuracy.
- Section headers renamed from template wording ("Abstract and/or Background", etc.).
- Body text in the rewritten panels is now Arial. The theme font (Calisto MT) could not be checked for fit here.

The co-author's comments are still in the .pptx. Resolve them in PowerPoint once you are happy with the changes.
