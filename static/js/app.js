const detectBtn = document.getElementById("detectBtn");
const resultContent = document.getElementById("resultContent");

function renderResult(data) {
  const verdictClass = data.is_plagiarized ? "result-alert" : "result-ok";
  resultContent.innerHTML = `
    <p class="${verdictClass}">${data.verdict}</p>
    <p><strong>AI Similarity Score:</strong> ${data.ai_similarity_score}%</p>
    <p><strong>Language:</strong> ${data.language}</p>
    <p><strong>Reference Samples Compared:</strong> ${data.references_compared}</p>
  `;
}

detectBtn.addEventListener("click", async () => {
  const code = document.getElementById("codeInput").value;
  const language = document.getElementById("language").value;

  if (!code.trim()) {
    resultContent.innerHTML = `<p class="result-alert">Please paste code first.</p>`;
    return;
  }

  resultContent.textContent = "Running analysis...";

  try {
    const response = await fetch("/api/detect", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code, language }),
    });

    const data = await response.json();
    if (!response.ok) {
      resultContent.innerHTML = `<p class="result-alert">${data.error || "Detection failed."}</p>`;
      return;
    }
    renderResult(data);
  } catch (error) {
    resultContent.innerHTML = `<p class="result-alert">Server error. Please try again.</p>`;
  }
});
