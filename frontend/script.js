function correctSentence() {
  const text = document.getElementById("userText").value;
  const mode = document.getElementById("mode").value;

  fetch("https://smart-auto-correct.onrender.com/correct", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ text: text, mode: mode })
  })
  .then(response => response.json())
  .then(data => {
    const outputDiv = document.getElementById("output");
    if (data.corrected) {
      outputDiv.innerText = `✅ AI Suggestion:\n${data.corrected}`;
    } else {
      outputDiv.innerText = `❌ Error: ${data.error}`;
    }
  })
  .catch(error => {
    document.getElementById("output").innerText = `❌ Network Error: ${error}`;
  });
}
