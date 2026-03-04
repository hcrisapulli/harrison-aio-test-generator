import re
from flask import Flask, Response, jsonify, render_template, request
import generator

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024

_TITLE_MAX = 120
_DESC_MAX = 200
_PREC_MAX = 200
_TAGS_MAX = 200
_SNAME_MAX = 100
_KPFX_MAX = 50
_TID_MAX = 50
_MAX_TC = 20
PRIORITIES = {"Critical", "High", "Medium", "Low"}


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/generate")
def generate():
    body = request.get_json(force=False, silent=False)
    if body is None:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    suite_name = (body.get("suite_name") or "").strip()
    if not suite_name:
        return jsonify({"error": "Suite name is required."}), 400
    if len(suite_name) > _SNAME_MAX:
        return jsonify({"error": f"Suite name too long (max {_SNAME_MAX})."}), 400

    key_prefix = (body.get("key_prefix") or "").strip()
    if not key_prefix:
        return jsonify({"error": "Key prefix is required."}), 400
    if len(key_prefix) > _KPFX_MAX:
        return jsonify({"error": f"Key prefix too long (max {_KPFX_MAX})."}), 400

    task_id = (body.get("task_id") or "").strip()
    if len(task_id) > _TID_MAX:
        return jsonify({"error": f"Task ID too long (max {_TID_MAX})."}), 400

    test_cases = body.get("test_cases")
    if not isinstance(test_cases, list) or not test_cases:
        return jsonify({"error": "At least one test case is required."}), 400
    if len(test_cases) > _MAX_TC:
        return jsonify({"error": f"Maximum {_MAX_TC} test cases allowed."}), 400

    validated = []
    for i, tc in enumerate(test_cases, 1):
        lbl = f"Test case {i}"
        title = (tc.get("title") or "").strip()
        if not title:
            return jsonify({"error": f"{lbl}: Title required."}), 400
        if len(title) > _TITLE_MAX:
            return jsonify({"error": f"{lbl}: Title too long."}), 400

        desc = (tc.get("description") or "").strip()
        prec = (tc.get("precondition") or "").strip()
        pri = (tc.get("priority") or "Medium").strip()
        if pri not in PRIORITIES:
            return jsonify({"error": f"{lbl}: Invalid priority."}), 400

        tags = (tc.get("tags") or "").strip()
        steps = [str(s).strip() for s in (tc.get("steps") or []) if str(s).strip()]
        if not steps:
            return jsonify({"error": f"{lbl}: At least one step required."}), 400
        results = [str(r).strip() for r in (tc.get("expected_results") or []) if str(r).strip()]

        validated.append({"title": title, "description": desc, "precondition": prec,
                           "priority": pri, "tags": tags, "steps": steps, "expected_results": results})

    data = {"suite_name": suite_name, "module": (body.get("module") or "").strip(),
            "key_prefix": key_prefix, "task_id": task_id, "test_cases": validated}

    try:
        csv_content = generator.generate_csv(data)
    except Exception as exc:
        return jsonify({"error": f"Generation failed: {exc}"}), 500

    safe = re.sub(r"[^\w\-. ]", "_", suite_name).replace(" ", "_")
    fname = f"{safe}_aio_tests.csv"
    return Response(csv_content, status=200, mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename=\"{fname}\"",
                 "Content-Type": "text/csv; charset=utf-8"})


if __name__ == "__main__":
    app.run(debug=True, port=5001)
