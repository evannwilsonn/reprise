# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Hiring managers first: people at data, AI-infrastructure and storage companies who open the page from Evan Wilson's resume or LinkedIn and give it about a minute. They need to see quickly what question was asked, what was found, and that the work is careful and real. Engineers reviewing depth come second; they read the method, assumptions and repo. Viewers arrive on desktop and phone about equally.

## Product Purpose

Reprise answers one question with evidence: when an AI model needs earlier conversation context again, how much does keeping it in storage (GPU memory, server memory, SSD, hard drives) save versus recomputing it? It replays 39,632 real requests from Mooncake's public production traces through a simulated GPU cluster and compares caching policies on time to first token, GPU time, cost and SSD wear. Success: a reader leaves knowing the answer, its limits, and that the author can turn an industry claim into a tested, reproducible analysis.

## Positioning

It tests a storage-vendor claim (KV-cache offloading makes inference ~95% faster) against real production traffic instead of a benchmark, and reports where the claim holds (fully reusable requests) and where it doesn't (hard drives at low bandwidth, SSD wear when caching everything).

## Operating Context

Static page (HTML, inline data) published as a Claude artifact and from the GitHub repo. Data comes from dbt reporting marts built on DuckDB and Snowflake. Controls: cluster scenario and workload (chat, tools & agents, synthetic).

## Capabilities and Constraints

- Real: request traces (arrival time, token counts, prefix-block hashes; no text). Assumed: model (Llama 3.1 70B), cluster (4 × 8 H100), tier specs, prices, all in seeds/.
- Not modelled: queueing, decode, contention, load/compute overlap. Absolute times are indicative; policy comparisons are the point.
- Traces cover one hour, so multi-day context return cannot be shown.
- Every number on the page must come from data.json; no invented figures.

## Brand Commitments

Each portfolio project has its own visual identity; a small shared signature may tie them to Evan. Names: Reprise (this), Cloverfield, Cloverleaf, Switchyard, Curbside, Clip Curator, Throughline, Bellwether.

## Evidence on Hand

dashboard/data.json (126 simulations, hit bands, warm-up curves, tier economics), README findings, Mooncake trace manifest with SHA-256. No testimonials, users, or external validation exist; do not imply any.

## Product Principles

1. Lead with the answer, then the evidence, then the assumptions.
2. Say what is real and what is assumed, right next to the claim.
3. Show where the industry claim fails as clearly as where it holds.
4. Every control changes a real number; nothing decorative pretends to be data.

## Accessibility & Inclusion

WCAG AA contrast in light and dark; charts readable without color alone; works at phone width.
