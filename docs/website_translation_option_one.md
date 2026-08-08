# Website Content Translation — Option 1: Generic Translation Table

This document describes a scalable multilingual design for website CMS content.
It replaces language-specific fields like `service_name_ar` with a data-driven
translation table so new languages can be added without schema changes.

## Why the current `_ar` approach is bad

The current implementation duplicates translatable fields for each language:
- `service_name` / `service_name_ar`
- `short_description` / `short_description_ar`
- `full_description` / `full_description_ar`

That works for two languages, but it does not scale.

Problems:
- every new language requires adding new fields to every DocType
- templates and helpers need more language-specific branches
- the schema becomes tied to language codes, not to content structure
- translation maintenance becomes harder for admins and developers

## Goal

Use one translation data model to support any number of languages.
The base content DocType keeps only default-language fields.
Translations are stored as separate rows keyed by language.

## Data model

Create a reusable child DocType such as `Website Content Translation`.
This doctype stores translations for one parent record and one fieldname.

Example fields:
- `parent_doc`: Link to the translated parent doctype (`Website Service`, `Website Blog Post`, etc.)
- `parent_name`: Data or Link to parent document name
- `language`: Data / Select (e.g. `ar`, `en`, `fr`)
- `fieldname`: Data (`service_name`, `short_description`, `full_description`)
- `translated_value`: Text / Text Editor
- `parenttype`: Data or hidden field to keep the parent doctype name

### Prefer one generic translation doctype

A single translation DocType is the cleanest option:
- `Website Content Translation`
- child table link from every translatable parent doctype
- each row stores a translation for one field in one language

This is simpler than one table per parent doctype and still language-agnostic.

## Example structure

### `Website Service`

Keep the existing fields:
- `service_name`
- `route`
- `icon`
- `image`
- `short_description`
- `full_description`

Remove language-specific fields such as:
- `service_name_ar`
- `short_description_ar`
- `full_description_ar`

Add a child table field to hold translations:
- `translations` → Table → `Website Content Translation`

### `Website Content Translation`

Fields:
- `language` (Data or Select)
- `fieldname` (Data)
- `translated_value` (Text / Text Editor)
- `parent_doc` / `parent_name` link fields if needed by your app

Use the same child table for all website content types that need translations.

## Rendering logic

Replace language-specific helpers with a generic lookup.
A single `localize(item, fieldname)` helper can do the work.

Pseudo-code:

```python
from frappe import _

TRANSLATION_FIELD_CACHE = {}


def localize(item, fieldname):
    lang = frappe.local.lang
    if lang == "en":
        return item.get(fieldname)

    translations = get_translations(item)
    translation = translations.get((lang, fieldname))
    if translation:
        return translation

    return item.get(fieldname)


def get_translations(item):
    # cache by document name for performance
    name = item.name
    if name in TRANSLATION_FIELD_CACHE:
        return TRANSLATION_FIELD_CACHE[name]

    rows = frappe.get_all(
        "Website Content Translation",
        fields=["language", "fieldname", "translated_value"],
        filters={"parent_name": name}
    )
    result = {(row.language, row.fieldname): row.translated_value for row in rows}
    TRANSLATION_FIELD_CACHE[name] = result
    return result
```

### Template usage

In Jinja templates, use the same helper for every translatable field:

```jinja
<h3>{{ localize(service, "service_name") }}</h3>
<p>{{ localize(service, "short_description") }}</p>
```

This stays the same regardless of whether the active language is Arabic,
French, Spanish, or anything else.

## Fallback behavior

When a translation is missing, fall back to the default field value:
- `service_name`
- `short_description`
- `full_description`

That means a partially translated page still works.

## Admin workflow

For each content item, editors can add translation rows rather than editing
multiple duplicated fields.

Example content item form layout:
- Default-language content fields
- `Translations` child table
  - `Language`
  - `Fieldname`
  - `Translated Value`

This is more flexible and future-proof.

## Benefits

- supports unlimited languages
- one schema, instead of one field per language
- easier rendering logic with a single helper
- simpler content maintenance
- no repeated template branching for each language

## Implementation steps

1. remove `_ar` fields from translatable website doctypes
2. create `Website Content Translation` DocType
3. add a `translations` child table field to each translatable parent doctype
4. implement `localize(item, fieldname)` using translation rows
5. update templates to call `localize(...)` uniformly
6. seed translations as rows instead of duplicate fields

## Notes

- This model is ideal for CMS-style content fields.
- For UI chrome strings and fixed labels, continue using Frappe's standard
  translation pipeline (`_`, `translations/ar.csv`, etc.).
- Use this model only for content data stored in custom doctypes.
