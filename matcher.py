"""
matcher.py
Keyword matching and test case composition for the AIO smart generator.
"""

import re
from templates_db import (
    COVERAGE_CATEGORIES,
    FEATURE_TEMPLATES,
    KEYWORD_MAP,
    CHECKLIST_FEATURE_MAP,
)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_checklist_questions():
    """Return ordered list of {key, label, short} dicts for the frontend."""
    return [
        {"key": k, "label": v["label"], "short": v["short"]}
        for k, v in COVERAGE_CATEGORIES.items()
    ]


def match_features(description: str) -> dict:
    """
    Analyse a plain-text description and return:
      {
        "features":  [list of template keys matched],
        "context":   {module, item, items, document_type, integration, ...},
        "tags":      [suggested tags],
      }
    """
    desc_lower = description.lower()
    words = set(re.findall(r"[a-z0-9]+", desc_lower))

    matched_features = []
    context = _default_context()
    tags = set()

    for entry in KEYWORD_MAP:
        keywords = [k.lower() for k in entry["keywords"]]
        # Match if ANY keyword appears as a substring of the description
        if any(kw in desc_lower for kw in keywords):
            for feat in entry["features"]:
                if feat not in matched_features:
                    matched_features.append(feat)

            # Merge context hints from the matching entry
            for ctx_key in ("module", "item", "items", "document_type",
                            "integration", "status", "field", "condition",
                            "wizard_name", "location", "filter_type", "action"):
                val = entry.get(ctx_key)
                if val and context.get(ctx_key) == _default_context().get(ctx_key):
                    context[ctx_key] = val

            for tag in entry.get("tags", []):
                tags.add(tag)

    # Fallback: if nothing matched at all, use crud as a safe default
    if not matched_features:
        matched_features = ["crud"]

    # Enrich context from description text where possible
    context = _enrich_context(context, description)

    return {
        "features": matched_features,
        "context": context,
        "tags": sorted(tags),
    }


def apply_coverage(features: list, checklist: dict) -> list:
    """
    Given matched features and a checklist dict {category_key: bool},
    add extra template keys that the user has opted into.
    Returns augmented feature list (no duplicates).
    """
    augmented = list(features)
    for cat_key, selected in checklist.items():
        if not selected:
            continue
        extra_feats = CHECKLIST_FEATURE_MAP.get(cat_key, [])
        for feat in extra_feats:
            if feat not in augmented:
                augmented.append(feat)
    return augmented


def generate_test_cases(description: str, checklist: dict,
                         extra_context: dict | None = None) -> list:
    """
    Main entry point.  Returns a list of test-case dicts ready for generator.py:
      [{title, description, precondition, priority, tags, steps, expected_results}, ...]

    Parameters
    ----------
    description   : free-text description from the user
    checklist     : {category_key: bool} from the frontend checklist
    extra_context : optional overrides for {module, item, items, ...}
    """
    match = match_features(description)
    features = apply_coverage(match["features"], checklist)
    ctx = match["context"]

    # User-supplied context overrides detected context
    if extra_context:
        for k, v in extra_context.items():
            if v:
                ctx[k] = v

    test_cases = []
    seen_titles = set()

    for feat_key in features:
        templates = FEATURE_TEMPLATES.get(feat_key, [])
        for tmpl in templates:
            # Render title with context
            try:
                title = tmpl["title"].format(**ctx)
            except KeyError:
                title = tmpl["title"]

            # Deduplicate
            if title in seen_titles:
                continue
            seen_titles.add(title)

            # Render steps / results
            steps = _render_list(tmpl.get("steps", []), ctx)
            # templates_db uses "results" key; support both for flexibility
            results = _render_list(
                tmpl.get("expected_results") or tmpl.get("results", []), ctx
            )

            # Build tags — combine template tags with match tags
            raw_tags = tmpl.get("tags", [])
            if isinstance(raw_tags, str):
                # Convert comma-separated string or single tag to list
                tc_tags_raw = [t.strip() for t in raw_tags.split(",") if t.strip()]
            else:
                tc_tags_raw = list(raw_tags)
            for t in match["tags"]:
                if t not in tc_tags_raw:
                    tc_tags_raw.append(t)

            test_cases.append({
                "title": title,
                "description": tmpl.get("description", ""),
                "precondition": _render(tmpl.get("precondition", ""), ctx),
                "priority": tmpl.get("priority", "Medium"),
                "tags": ",".join(tc_tags_raw),
                "steps": steps,
                "expected_results": results,
            })

    return test_cases


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _default_context() -> dict:
    return {
        "module": "Module",
        "item": "item",
        "items": "items",
        "document_type": "document",
        "integration": "integration",
        "status": "status",
        "field": "field",
        "condition": "condition",
        "wizard_name": "setup wizard",
        "location": "document view",
        "filter_type": "status",
        "action": "action",
    }


def _enrich_context(ctx: dict, description: str) -> dict:
    """
    Try to pull concrete nouns from the description to make context more specific.
    Very lightweight — just capitalise the first noun-like word we find.
    """
    # If module is still generic, try to extract a noun phrase from description
    if ctx["module"] == "Module":
        # Take the first 1-3 words that look like a feature name
        words = re.findall(r"[A-Za-z][a-z]+", description)
        if words:
            ctx["module"] = " ".join(words[:2]).title()
    if ctx["item"] == "item":
        words = re.findall(r"[A-Za-z][a-z]+", description)
        if words:
            ctx["item"] = words[0].lower()
            ctx["items"] = words[0].lower() + "s"
    return ctx


def _render(template_str: str, ctx: dict) -> str:
    if not template_str:
        return ""
    try:
        return template_str.format(**ctx)
    except KeyError:
        return template_str


def _render_list(lst: list, ctx: dict) -> list:
    return [_render(s, ctx) for s in lst]
