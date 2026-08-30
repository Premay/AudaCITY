# Future Past-Question API Integration

Status: NOT PART OF PHASE 1.

ALOC/QBoard is the intended initial external provider, subject to current API terms and confirmed content usage rights.

Do not place the ALOC token in repository documentation, source code or AI prompts.

Store it server-side as:
ALOC_API_KEY=...

## Future flow
ALOC API → ALOCProvider → Normalisation → Validation → Deduplication → Licensing check → Review → Database → Student API

Do not call ALOC directly from Flutter or on every student question.

Use controlled ingestion and database serving where permitted.

Retain source/provider, external question ID, source URL where available, year, licence status, import timestamp and review status.

API availability does not prove commercial redistribution rights. Verify current provider terms before public/commercial publication.

Conserve the limited API allowance through batching/caching and database storage.
