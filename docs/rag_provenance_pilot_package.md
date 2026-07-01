# RAG Provenance Paid Pilot Package

## Pilot name

**AI Source Provenance and Trust Readiness Scan**

## Product line

Recommended product name: **Resilient Provenance**

## Buyer profile

Best-fit initial buyers:

1. municipalities or regional agencies preparing AI search over documents, GIS layers, permits, public works records, infrastructure records, or emergency-management files;
2. infrastructure consultants that manage fragmented client data and need source lineage before using AI workflows;
3. legal, compliance, or investigation teams that need chain-of-custody evidence for AI-assisted document review;
4. foundations, grant programs, and scholarship operations that need auditable evidence trails for decisions, reports, and records;
5. regulated operators preparing internal RAG systems for sensitive knowledge bases.

## Pain statement

Organizations are moving files, PDFs, GIS layers, spreadsheets, code/configs, and datasets into AI retrieval systems faster than they are building provenance controls. This creates risk because teams may not be able to prove:

- which source files entered the AI pipeline;
- whether cited answer chunks came from approved source material;
- whether a source file was stale, archived, draft, unsigned, or unknown;
- whether GIS or infrastructure layers were reviewable before AI use;
- whether an AI answer can be traced back to a known source version.

## Pilot objective

Deliver a bounded source-provenance scan and answer-verification package that tells the buyer:

> Which source assets are traceable enough to enter an AI retrieval pipeline, and which answer citations can be verified against approved manifest records?

## Scope

### Included

- file-level source inventory;
- SHA-256 fingerprint manifest;
- deterministic chunk hashes for readable text assets;
- conservative source classification;
- review flags for unknown, stale, archived, draft, GIS candidate, and file-hash-only assets;
- RAG answer citation verification against manifest assets and chunks;
- buyer-readable scan report;
- buyer-readable answer verification report;
- remediation backlog.

### Optional add-ons

- GIS layer profile and missing-sector scan;
- Google Drive metadata adapter;
- GitHub repository source adapter;
- signature-ready manifest design;
- recurring monthly scan report;
- foundation/grant-program evidence-register adaptation.

## Deliverables

| Deliverable | Description |
|---|---|
| Source provenance manifest | Machine-readable JSON source and chunk fingerprint register |
| RAG provenance report | Human-readable source inventory and review-flag report |
| Answer verification report | Proof that answer citations do or do not map to manifest-approved assets/chunks |
| Risk and remediation backlog | Prioritized fixes before RAG deployment or expansion |
| Claim-boundary statement | Clear limitation language that avoids unsupported security claims |

## Acceptance criteria

The pilot is complete when:

1. a defined source directory, repo, export, or document set has been scanned;
2. a JSON manifest has been produced;
3. a human-readable provenance report has been produced;
4. at least one sample RAG answer citation object has been verified;
5. all rejected citations include explicit reasons;
6. all unknown/stale/draft/archive/GIS candidate flags are listed for review;
7. the buyer receives a remediation backlog.

## Pricing posture

Use pricing as planning language until buyer discovery is complete.

Recommended pilot tiers:

| Tier | Buyer fit | Scope | Planning price posture |
|---|---|---|---|
| Starter | foundation, small org, small municipal office | one repo/folder, one report, one answer-verification sample | low four figures |
| Professional | municipality, consultant, regulated team | multiple source folders, provenance report, verification report, remediation backlog | mid four to low five figures |
| Infrastructure/GIS | municipal, public works, emergency management, infrastructure consultant | GIS/doc/data scan, missing-sector profile, provenance report, remediation backlog | low to mid five figures |
| Retainer | recurring governance | monthly scans and evidence reports | recurring monthly fee |

## Limitation language

This pilot provides provenance evidence, source traceability, and citation verification. It does not certify the truth of source content, the correctness of an AI answer, regulatory compliance, privacy compliance, cybersecurity sufficiency, or model safety.

## Follow-on expansion

A completed pilot can expand into:

1. recurring source-trust monitoring;
2. GIS/infrastructure data readiness scoring;
3. RAG deployment preflight checks;
4. signed manifest chain-of-custody;
5. cross-repo evidence-register engine;
6. foundation evidence operations for scholarship, grants, and public-interest reporting.

## Sales narrative

**Resilient Provenance** gives organizations a practical trust layer before they let AI search, summarize, or reason over sensitive records. The first deliverable is not a broad AI platform. It is a narrow, high-trust evidence package: source fingerprints, chunk traceability, citation verification, review flags, and a remediation plan.
