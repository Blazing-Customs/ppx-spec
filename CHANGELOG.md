# Changelog

All notable changes to the PPX specification will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
for schemas, with a separate dated/versioned track for the normative spec document.

## [0.1.0-draft] - 2026-04-23

### Added
- Initial draft of the PPX (Preference Profile Exchange) specification.
- Core data model: `Profile`, `Claim`, `ContextModifier`, `ConsentGrant`, `EvidenceRef`,
  `DiscoveryCard`, `ExtensionDescriptor`, `DerivedView`.
- Eight core JSON Schemas (2020-12 draft).
- Three extension schemas: `core`, `fragrance`, `travel`.
- Six example payloads demonstrating valid profile, grant, derived view, discovery
  card, and context modifier shapes.
- Conformance suite with eight executable tests: deny-by-default, redaction,
  expired-grant, writeback-pending, cross-domain-denial, revocation, discovery-card,
  schema-roundtrip.
- Five binding documents: MCP, A2A, AG-UI, A2UI, HTTP.
- Governance scaffolding: namespace registration, versioning policy, proposal
  template, conformance levels.
- MkDocs Material site deployed to GitHub Pages.

### Notes
- Status: **Draft, pre-standardization, pre-stable.** Not suitable for production
  commitments. Breaking changes expected before `1.0`.
- High-impact domains (health, employment, housing, insurance, credit) are
  explicitly out of scope for v0.1.
- A2UI bindings target v0.8 (stable); v0.9 draft features are not cited normatively.

[0.1.0-draft]: https://github.com/Blazing-Customs/ppx-spec/releases/tag/v0.1.0-draft
