# AKUMA

AKUMA is a desktop application for generating synthetic datasets with configurable schemas and controlled, measurable data corruption for testing data pipelines and data-quality assumptions.

## Why AKUMA?

Generating valid synthetic data is relatively easy. Generating data that is wrong in controlled, measurable, and eventually reproducible ways is a different problem.

Real-world data is rarely simply "valid" or "invalid." It contains inconsistencies: missing values, malformed records, unexpected types, broken relationships, invalid ranges, and combinations of errors that downstream systems were not designed to expect.

AKUMA is my attempt to explore a simple question:

**How do you generate the right incorrect data?**

The purpose is not merely to corrupt a dataset randomly. It is to make inconsistency configurable enough that a developer or data engineer can deliberately challenge assumptions made by an ETL pipeline, validation layer, or downstream system.

## Engineering Idea

Most data systems contain implicit assumptions.

A field expected to contain an integer will always contain an integer.
A required value will always exist.
A relationship between records will remain valid.
An input file will conform to its expected structure.

Those assumptions often remain invisible until real data violates them.

AKUMA approaches data corruption as a controllable input rather than an accidental failure. The goal is to let users define what should be wrong, how much of it should be wrong, and where those inconsistencies should appear.

This makes it possible to test not only whether a pipeline works with expected data, but also how it behaves when its assumptions stop being true.

## Controlled Corruption

Randomly damaging data is easy. Useful corruption requires constraints.

AKUMA is being designed around explicit corruption parameters: how much data should be affected, which fields may be affected, and which types of errors may be introduced.

The long-term goal is to make corrupted datasets reproducible and their failure characteristics measurable, allowing the same assumptions to be challenged repeatedly under controlled conditions.

## Status

(!) 30.07.2026 — Work in progress.

AKUMA is currently in early development. The core GUI and navigation are implemented, and development is currently focused on completing configuration logic, corruption controls, validation, and UX behavior before moving to the generation and corruption backend.

## Planned MVP

- Desktop GUI
- Configurable data fields
- Synthetic data generation
- Controlled generation of corrupted records
- Configurable corruption amount
- Multiple corruption types
- Optional restriction of corruption to selected columns
- CSV, JSON, Parquet, XML, and Excel (.xlsx) export
- Validation and user-facing error handling

## License

AKUMA is source-available software. See [LICENSE](LICENSE) for usage, modification, and distribution terms.
