/**
 * app.js — AIO Test Case Generator frontend logic
 */
(function () {
  "use strict";

  const testCaseList  = document.getElementById("testCaseList");
  const addBtn        = document.getElementById("addBtn");
  const generateBtn   = document.getElementById("generateBtn");
  const btnText       = document.getElementById("btnText");
  const btnSpinner    = document.getElementById("btnSpinner");
  const errorBanner   = document.getElementById("errorBanner");
  const template      = document.getElementById("tcTemplate");

  const MAX_TC = 20;
  let cardCount = 0;

  // ── Card management ───────────────────────────────────────────────────────

  function addCard() {
    if (cardCount >= MAX_TC) {
      showError(`Maximum of ${MAX_TC} test cases allowed.`);
      return;
    }

    cardCount++;
    const frag  = template.content.cloneNode(true);
    const card  = frag.querySelector(".tc-card");
    card.dataset.index = cardCount;
    card.querySelector(".tc-num").textContent = cardCount;
    card.classList.add("expanded");

    // Title → preview sync
    const titleInput   = card.querySelector(".tc-title");
    const titlePreview = card.querySelector(".tc-card-title-preview");
    const charCount    = card.querySelector(".char-count");
    const charCounter  = card.querySelector(".char-counter");

    titleInput.addEventListener("input", () => {
      const val = titleInput.value.trim();
      titlePreview.textContent = val ? `— ${val}` : "";
      const len = titleInput.value.length;
      charCount.textContent = len;
      charCounter.classList.toggle("near-limit", len >= 100 && len < 120);
      charCounter.classList.toggle("at-limit",   len >= 120);
    });

    // Collapse / expand on header click
    const header = card.querySelector(".tc-card-header");
    header.addEventListener("click", (e) => {
      if (e.target.classList.contains("tc-remove-btn")) return;
      card.classList.toggle("expanded");
    });

    // Remove button
    card.querySelector(".tc-remove-btn").addEventListener("click", () => {
      card.remove();
      renumberCards();
    });

    // Tag chips
    card.querySelectorAll(".tag-chip").forEach((chip) => {
      chip.addEventListener("click", () => {
        const tagsInput = card.querySelector(".tc-tags");
        const tag = chip.dataset.tag;
        const current = tagsInput.value.split(",").map(t => t.trim()).filter(Boolean);

        if (current.includes(tag)) {
          tagsInput.value = current.filter(t => t !== tag).join(",");
          chip.classList.remove("active");
        } else {
          current.push(tag);
          tagsInput.value = current.join(",");
          chip.classList.add("active");
        }

        // Sync active state
        syncTagChips(card);
      });
    });

    testCaseList.appendChild(frag);
    updateAddBtn();
  }

  function syncTagChips(card) {
    const tagsInput = card.querySelector(".tc-tags");
    const current   = tagsInput.value.split(",").map(t => t.trim()).filter(Boolean);
    card.querySelectorAll(".tag-chip").forEach(chip => {
      chip.classList.toggle("active", current.includes(chip.dataset.tag));
    });
  }

  function renumberCards() {
    const cards = testCaseList.querySelectorAll(".tc-card");
    cardCount = cards.length;
    cards.forEach((card, i) => {
      card.dataset.index = i + 1;
      card.querySelector(".tc-num").textContent = i + 1;
    });
    updateAddBtn();
  }

  function updateAddBtn() {
    addBtn.disabled = cardCount >= MAX_TC;
    addBtn.style.opacity = cardCount >= MAX_TC ? "0.4" : "1";
  }

  addBtn.addEventListener("click", addCard);

  // Start with one card
  addCard();

  // ── Payload builder ───────────────────────────────────────────────────────

  function buildPayload() {
    const test_cases = [];

    testCaseList.querySelectorAll(".tc-card").forEach((card) => {
      const steps = card.querySelector(".tc-steps").value
        .split("\n").map(s => s.trim()).filter(Boolean);
      const expected_results = card.querySelector(".tc-results").value
        .split("\n").map(r => r.trim()).filter(Boolean);

      test_cases.push({
        title:            card.querySelector(".tc-title").value.trim(),
        description:      card.querySelector(".tc-desc").value.trim(),
        precondition:     card.querySelector(".tc-prec").value.trim(),
        priority:         card.querySelector(".tc-priority").value,
        tags:             card.querySelector(".tc-tags").value.trim(),
        steps,
        expected_results,
      });
    });

    return {
      suite_name: document.getElementById("suiteName").value.trim(),
      module:     document.getElementById("moduleField").value.trim(),
      key_prefix: document.getElementById("keyPrefix").value.trim(),
      task_id:    document.getElementById("taskId").value.trim(),
      test_cases,
    };
  }

  // ── Client-side validation ────────────────────────────────────────────────

  function validate(payload) {
    if (!payload.suite_name) return "Suite Name is required.";
    if (!payload.key_prefix) return "Key Prefix is required.";
    if (!payload.test_cases.length) return "Add at least one test case.";

    for (let i = 0; i < payload.test_cases.length; i++) {
      const tc  = payload.test_cases[i];
      const lbl = `Test Case ${i + 1}`;
      if (!tc.title)         return `${lbl}: Title is required.`;
      if (!tc.steps.length)  return `${lbl}: At least one step is required.`;
    }
    return null;
  }

  // ── Error / loading helpers ───────────────────────────────────────────────

  function showError(msg) {
    errorBanner.textContent = msg;
    errorBanner.style.display = "block";
    errorBanner.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  function hideError() {
    errorBanner.style.display = "none";
    errorBanner.textContent   = "";
  }

  function setLoading(on) {
    generateBtn.disabled      = on;
    btnText.textContent       = on ? "Generating…" : "Generate & Download CSV";
    btnSpinner.style.display  = on ? "inline-block" : "none";
  }

  // ── Generate & download ───────────────────────────────────────────────────

  generateBtn.addEventListener("click", async () => {
    hideError();

    const payload = buildPayload();
    const err     = validate(payload);
    if (err) { showError(err); return; }

    setLoading(true);
    try {
      const response = await fetch("/generate", {
        method:  "POST",
        headers: { "Content-Type": "application/json" },
        body:    JSON.stringify(payload),
      });

      if (!response.ok) {
        let msg = `Server error (${response.status})`;
        try { const j = await response.json(); if (j.error) msg = j.error; } catch (_) {}
        showError(msg);
        return;
      }

      // Derive filename from Content-Disposition header or fall back
      let filename = "aio_tests.csv";
      const cd = response.headers.get("Content-Disposition") || "";
      const m  = cd.match(/filename="([^"]+)"/);
      if (m) filename = m[1];

      const blob = await response.blob();
      const url  = URL.createObjectURL(blob);
      const a    = document.createElement("a");
      a.href     = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);

    } catch (err) {
      showError("Network error: " + err.message);
    } finally {
      setLoading(false);
    }
  });
})();
