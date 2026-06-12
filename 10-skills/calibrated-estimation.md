---
title: "Calibrated Estimation and Probability Language in Intelligence"
type: skill
tags: [calibration, estimation, probability, uncertainty, WEP, Sherman-Kent, ODNI, superforecasting, intelligence-analysis]
llms: [claude-sonnet]
status: active
last_updated: 2026-05-17
---

# Calibrated Estimation and Probability Language

## Purpose

Systematic communication of uncertainty in analytical products using standardised, calibrated probability language. Prevents the two most common estimation failures: false precision (claiming more certainty than is warranted) and epistemic cowardice (using vague language to avoid accountability for analytical positions).

**Use when:**
- Writing any intelligence assessment or threat report that makes a probabilistic claim
- Assigning confidence levels to analytical conclusions
- Reviewing a draft intelligence product for uncertainty language
- Evaluating how well an AI system or analyst is calibrated
- Academic work: explicit confidence expression in empirical claims

**Feeds into:** [[10-skills/structured-analytical-techniques]], [[10-skills/humint-source-evaluation]], [[10-skills/indications-warning-analysis]]

---

## LLM Role in Calibrated Products

**LLMs cannot perform genuine calibration.** When an LLM outputs "Confidence: High" or "75% likelihood," it is predicting the next token in a sequence that resembles an intelligence report. It is not executing a Bayesian update, it has no reference class, and it cannot track whether its past 70% claims materialised 70% of the time. The output is false precision with the vocabulary of rigorous analysis.

**Division of labour — enforce this without exception:**

| Task | Who does it |
|------|------------|
| Extract evidence from source material | LLM |
| Enumerate hypotheses and list supporting/counter evidence per hypothesis | LLM |
| Identify information gaps and unanswered collection requirements | LLM |
| Flag logical inconsistencies or contradictions between sources | LLM |
| Apply structural criteria (e.g., extraction method classification) | LLM |
| Assign probability language (WEP phrases, ODNI percentages) | **Analyst only** |
| Assign confidence levels (High / Moderate / Low) | **Analyst only** |
| Update probability estimates as new information arrives | **Analyst only** |

**Rule:** If an LLM output field contains a WEP phrase, an ODNI probability bracket, or a High/Moderate/Low confidence label where the underlying reasoning involves analytical judgment (attribution, intent, likelihood of action), treat it as a placeholder and replace it with your own assessment before the product is finalised or ingested.

---

## Why Calibration Matters

An analyst is **calibrated** if, when they say something has a 70% probability, it actually happens roughly 70% of the time across many such statements. Calibration is not accuracy in any single case — it is consistency between expressed confidence and actual frequency of being right.

**Uncalibrated patterns:**

| Pattern | Description | Problem |
|---------|-------------|---------|
| **Overconfidence** | 90% confidence claims that come true 60% of the time | Decision-makers allocate resources to high-confidence threats that fail; credibility erodes |
| **Underconfidence** | 50% confidence claims that come true 80% of the time | Urgent threats are treated as uncertain; responses are delayed or inadequate |
| **Epistemic cowardice** | "It is possible that..." / "We cannot rule out..." | Provides no decision-relevant information; protects the analyst while failing the consumer |
| **Precision inflation** | "73% probability" when evidence supports only "roughly 3-in-4" | False precision misleads; the decimal implies measurement that does not exist |

---

## Sherman Kent's Words of Estimative Probability (WEP)

The foundational framework from CIA, developed by Sherman Kent in the 1960s. Maps verbal probability expressions to approximate numeric ranges.

| Phrase | Approximate probability range |
|--------|------------------------------|
| Certain | ~99% |
| Almost certainly / highly likely | 93% ± 6% |
| Probably / likely | 75% ± 12% |
| Roughly even chance / about as likely as not | 50% ± 10% |
| Unlikely / probably not | 30% ± 10% |
| Almost certainly not / highly unlikely | 7% ± 5% |
| Impossible | ~1% |

**Critical problem identified by Kent:** Different readers assign dramatically different probability values to the same verbal phrase. "Possible" to one analyst means 20%; to another it means 60%. The WEP chart standardises this but only if all parties agree to use it.

**Usage rule:** When using WEP phrases, include the numeric equivalent in parentheses on first use in a product: "The group is likely (~75%) to conduct a follow-on attack within 30 days."

---

## ODNI Probability Language Standards

The Office of the Director of National Intelligence updated the IC-wide standard:

| Language | Probability |
|----------|-------------|
| Almost certainly | >95% |
| Very likely | 80–95% |
| Likely | 55–80% |
| Roughly even chance | 45–55% |
| Unlikely | 20–45% |
| Very unlikely | 5–20% |
| Remote | <5% |

**Best practice:** When writing products for intelligence or LE audiences, use ODNI standard phrasing plus numeric range. When writing academic work, use numeric probability ranges directly.

---

## Confidence vs. Probability

These are distinct dimensions that are frequently conflated:

| Dimension | What it measures |
|-----------|----------------|
| **Probability** | How likely is the event? (about the world) |
| **Confidence** | How well-founded is the probability estimate? (about the analysis) |

A statement like "We assess with high confidence that the probability is roughly even" means: we believe the evidence is solid (high confidence), but the evidence genuinely supports a 50/50 assessment.

**Standard three-tier confidence notation:**

| Level | Definition |
|-------|-----------|
| **High confidence** | Judgement based on high-quality information and/or a sound analytical framework; few significant analytic uncertainties |
| **Moderate confidence** | Judgement based on credible information that is not conclusive; multiple interpretations are possible |
| **Low confidence** | Judgement based on fragmentary or questionable information; significant analytic uncertainties |

**Format in products:** "[Probability phrase (numeric %)] — [Confidence: High/Moderate/Low]"
Example: "The actor is likely (~70%) to deploy ransomware against the target within the quarter — Confidence: Moderate (limited corroborating telemetry; single source)"

---

## Reference Class Forecasting

Developed by Daniel Kahneman and Amos Tversky; formalised by Philip Tetlock (Superforecasting). Addresses the **inside view / outside view** problem.

**Inside view:** Estimate probability by thinking about the specific case — its unique features, the narrative around it, how it feels.

**Outside view (reference class):** Estimate probability by finding a reference class of similar past events and using the base rate.

**Problem:** The inside view is almost always more salient and more wrong. Human minds anchor on specific narrative features and inflate or deflate probability based on emotional vividness, not statistical frequency.

**Procedure:**
1. Identify the reference class: "situations that are like this one in the relevant ways"
2. Determine the base rate: how often did the event occur in the reference class?
3. Adjust the base rate based on specific features of this case that are genuinely informative
4. Do not adjust more than the evidence warrants — specific features are usually less informative than they seem

**Example:**
- Specific case: assessing probability that a new ransomware group achieves 50+ victims in first 12 months
- Reference class: ransomware groups that emerged in the past 5 years with similar tooling and initial campaign characteristics
- Base rate: ~30% of such groups achieved this scale in 12 months
- Adjustment factors: this group has access to an active affiliate network (+) and is operating in a sector where law enforcement attention is currently low (+); start from 30%, adjust up to ~45%

---

## Superforecasting Techniques (Tetlock)

Philip Tetlock's research identified the traits and techniques of "superforecasters" — individuals who maintain excellent calibration over time.

**Core practices:**

| Practice | Description |
|----------|------------|
| **Start with a base rate** | Always begin outside view before adjusting for specific features |
| **State probability numerically** | Forces specificity; prevents epistemic cowardice |
| **Update regularly** | Revisit estimates as new information arrives; track the update direction |
| **Track your record** | Keep a scoring log; calibration can only be improved by measuring it |
| **Break problems into components** | Estimate sub-questions separately, then aggregate (Fermi decomposition) |
| **Assign probability to your estimate being wrong** | Not "what is the probability of X?" but "what is the probability that my estimate of X is wrong by more than N%?" |

**Fermi decomposition for intelligence estimates:**

Break a single uncertain estimate into smaller, more tractable sub-questions. Each sub-answer is easier to estimate independently; the product or combination is more reliable than a single holistic judgment.

Example: "What is the probability of a major state-sponsored cyberattack against European critical infrastructure in the next 6 months?"

Decomposed:
- What is the base rate of such attacks per year over the past 5 years? (2 confirmed, range 0–3)
- Is the current geopolitical environment above or below baseline for motivation? (above: +20%)
- Is capability of known threat actors currently elevated? (stable)
- Is the defensive posture of European infrastructure currently weaker or stronger? (slightly weaker: +10%)
- Combined: ~55% probability over 6 months — Confidence: Low (small historical sample, high geopolitical volatility)

---

## Expressing Uncertainty in Academic Writing

Academic contexts require different calibration conventions than intelligence products:

| Academic phrase | Probability it should convey |
|----------------|------------------------------|
| "It is certain that" / "It is clear that" | Reserve for logically necessary claims only |
| "The evidence strongly suggests" | ~75–85% confidence in the empirical claim |
| "The evidence suggests" | ~55–75% |
| "There is some evidence for" | ~40–55% — genuinely uncertain |
| "It is possible that" | Do not use — provides no information |
| "It cannot be ruled out that" | Do not use unless you have a reason to mention a remote possibility |

**Avoid:** Qualitative uncertainty language that provides no update to the reader ("It is worth noting that...", "One could argue that...", "It might be the case that..."). These are hedges masquerading as analysis.

---

## Calibration in CTI Products

For threat intelligence specifically:

| Claim type | Calibration requirement |
|-----------|------------------------|
| **IOC attribution** | Explicitly state confidence in actor attribution separately from confidence in the IOC itself |
| **Campaign linkage** | How strong is the evidence linking this campaign to prior activity? Specify the linking features and their strength |
| **Intent assessment** | "This actor will..." claims require explicit acknowledgment that intent is inferred from capability and history; highest uncertainty category |
| **Timeline estimate** | "Within X days/weeks/months" — explicitly state the basis; timeline estimates degrade fast |

**Output template for CTI confidence statement:**
```
Assessment: [one-sentence claim]
Probability: [WEP phrase] (~X%)
Confidence: [High / Moderate / Low]
Basis: [key evidence and sources]
Key uncertainty: [what most changes this estimate if wrong?]
Expires: [when should this estimate be revisited?]
```

---

## Quick Reference — ODNI Probability Language

```
Almost certainly  >95%
Very likely       80–95%
Likely            55–80%
Roughly even      45–55%
Unlikely          20–45%
Very unlikely     5–20%
Remote            <5%

Format: [phrase] (~X%) — Confidence: [H/M/L] — [basis]
```
