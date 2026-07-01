# GIS Provenance Profile

## Purpose

The GIS provenance profile adapts the RAG provenance scanner for municipal, infrastructure, public-works, emergency-management, and critical-infrastructure AI-security pilots.

It turns a generic provenance manifest into a sector-coverage report that identifies which civic/infrastructure GIS layers appear to be present and which expected sectors are missing from the scanned source set.

## Strategic value

This profile connects the repository's cryptographic provenance work to a high-impact revenue lane:

> AI-secured infrastructure intelligence for public-sector and civic data systems.

The profile supports buyer conversations where a municipality, consultant, or infrastructure operator wants to know whether its documents, datasets, and GIS layers are traceable enough to enter an AI retrieval, search, or readiness-scoring workflow.

## Supported sector profile

The current profile checks for candidate layer coverage across:

| Sector | Example keywords |
|---|---|
| Roads / transportation | roads, streets, bridges, highway, transport |
| Parcels / property | parcels, property, assessor, lots |
| Water | water, hydrants, mains |
| Sewer / wastewater | sewer, wastewater, stormwater, drains |
| Electric / energy | electric, grid, power, substations |
| Telecom | telecom, fiber, broadband, towers |
| Public safety | police, fire, EMS, safety |
| Emergency management | emergency, shelters, evacuation, hazard |
| Healthcare / public health | health, hospitals, clinics |
| Schools / civic | schools, libraries, town hall, municipal assets |
| Flood / environment | flood, wetlands, watershed, environmental layers |
| Zoning / land use | zoning, planning, land use |

## Run command

Generate the base provenance manifest first:

```bash
make rag-provenance
```

Then generate the GIS profile:

```bash
make gis-profile
```

Direct command:

```bash
python scripts/17_gis_provenance_profile.py \
  --manifest results/provenance/rag_provenance_manifest.json
```

Default outputs:

- `results/provenance/gis_provenance_profile.json`
- `results/provenance/gis_provenance_profile.md`

## Claim boundary

The GIS provenance profile is a source-readiness and missing-sector screen. It does not certify map completeness, source accuracy, emergency readiness, public safety readiness, operational security, or infrastructure security.

## Buyer-facing interpretation

A covered sector means the scanner found at least one GIS candidate whose path/name matched the sector keyword profile. A missing sector means no candidate was found by the current keyword profile. Missing does not prove the organization lacks the data; it means the scanned source set did not expose a matching candidate.

## Next build steps

1. Add jurisdiction, owner, department, and source-system fields.
2. Add explicit layer taxonomy configuration.
3. Add shapefile sidecar grouping.
4. Add Google Drive folder metadata ingestion.
5. Add municipal missing-sector report scoring.
6. Add signed GIS layer registry support.
