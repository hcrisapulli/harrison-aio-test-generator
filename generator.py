import csv
import io


def generate_csv(data: dict) -> str:
    key_prefix = data["key_prefix"]
    task_id = (data.get("task_id") or "").strip()
    include_req = bool(task_id)

    output = io.StringIO()
    header = ["Key", "Title", "Description", "Pre-condition", "BDDKeyword",
              "Steps", "Data", "Expected Result", "Priority", "Status", "Tags"]
    if include_req:
        header.append("Requirements")

    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL, lineterminator="\r\n")
    writer.writerow(header)

    for i, tc in enumerate(data["test_cases"], start=1):
        key = f"{key_prefix}-{i:03d}"
        title = tc["title"]
        desc = tc.get("description", "")
        prec = tc.get("precondition", "")
        priority = tc.get("priority", "Medium")
        tags = tc.get("tags", "")
        steps = tc.get("steps", [])
        results = tc.get("expected_results", [])

        max_len = max(len(steps), len(results), 1)
        steps_p = list(steps) + [""] * (max_len - len(steps))
        results_p = list(results) + [""] * (max_len - len(results))

        for row_idx in range(max_len):
            step = steps_p[row_idx]
            result = results_p[row_idx]

            if row_idx == 0:
                row = [key, title, desc, prec, "", step, "", result, priority, "Draft", tags]
            else:
                row = ["", "", "", "", "", step, "", result, "", "", ""]

            if include_req:
                row.append(task_id if row_idx == 0 else "")

            writer.writerow(row)

    return output.getvalue()
