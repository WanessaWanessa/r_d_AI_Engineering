# Prompt changelog

Each version is a separate file `extract_vN.md`: front matter (`version`, `date`, `description`), then a `## system` section and a `## user` section. `{text}` in the user section is replaced with the input text.

## v1 — 2026-10-15 (baseline)

- Role, task and general rules: use only the text, missing -> null, `is_confirmed` for rumors, `sentiment` for the subject company, `language`.
- Half of the labelling conventions from `schema.py`, the ones about not inventing data and putting it in the right place:
  - no guessed year in dates;
  - ticker only if written in the text;
  - brokers / analyst firms -> `analyst_action`, not `companies`;
  - insider-trade numbers -> `insider_transactions` only, not `key_figures`.
- Field details come only from the JSON schema passed to the model through structured output.
- On purpose, the prompt does **not** include the normalization and interpretation conventions: absolute money units (`$117.68M` -> 117680000, `(42c)` -> -0.42), "First Middle Last" name order, a company's denial counts as confirmed, takeover target -> positive sentiment. These are left for v2 so we can measure what they add.
