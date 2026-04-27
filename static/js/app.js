const detectBtn = document.getElementById("detectBtn");
const resultContent = document.getElementById("resultContent");
const generatedSolutionBox = document.getElementById("generatedSolutionBox");

function renderResult(data) {
  const verdictClass = data.is_plagiarized ? "result-alert" : "result-ok";
  const warningHtml = data.warning
    ? `<p class="result-warning"><strong>Warning:</strong> ${escapeHtml(data.warning)}</p>`
    : "";
  resultContent.innerHTML = `
    ${warningHtml}
    <p class="${verdictClass}">${data.verdict}</p>
    <p><strong>AI Similarity Score:</strong> ${data.ai_similarity_score}%</p>
    <p><strong>Similarity with AI-generated Solution:</strong> ${data.ai_reference_similarity_score}%</p>
    <p><strong>AI Provider Used:</strong> ${data.ai_provider || "fallback-only"}</p>
    <p><strong>Language:</strong> ${data.language}</p>
    <p><strong>Reference Samples Compared:</strong> ${data.references_compared}</p>
  `;

  if (data.generated_solution) {
    generatedSolutionBox.classList.remove("hidden");
    generatedSolutionBox.innerHTML = `
      <h3>Generated AI Solution</h3>
      <pre><code>${escapeHtml(data.generated_solution)}</code></pre>
    `;
  } else {
    generatedSolutionBox.classList.add("hidden");
    generatedSolutionBox.innerHTML = "";
  }
}

function escapeHtml(str) {
  return str
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

detectBtn.addEventListener("click", async () => {
  const problemStatement = document.getElementById("problemStatement").value;
  const code = document.getElementById("codeInput").value;
  const language = document.getElementById("language").value;

  if (!problemStatement.trim()) {
    resultContent.innerHTML = `<p class="result-alert">Please enter a problem statement first.</p>`;
    generatedSolutionBox.classList.add("hidden");
    generatedSolutionBox.innerHTML = "";
    return;
  }

  if (!code.trim()) {
    resultContent.innerHTML = `<p class="result-alert">Please paste code first.</p>`;
    generatedSolutionBox.classList.add("hidden");
    generatedSolutionBox.innerHTML = "";
    return;
  }

  resultContent.textContent = "Generating AI solution and running analysis...";
  generatedSolutionBox.classList.add("hidden");
  generatedSolutionBox.innerHTML = "";

  try {
    const response = await fetch("/api/detect", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ problem_statement: problemStatement, code, language }),
    });

    const data = await response.json();
    if (!response.ok) {
      resultContent.innerHTML = `<p class="result-alert">${data.error || "Detection failed."}</p>`;
      generatedSolutionBox.classList.add("hidden");
      generatedSolutionBox.innerHTML = "";
      return;
    }
    renderResult(data);
  } catch (error) {
    resultContent.innerHTML = `<p class="result-alert">Server error. Please try again.</p>`;
  }
});
