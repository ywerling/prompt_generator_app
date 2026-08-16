document.addEventListener("DOMContentLoaded", () => {
  const input = document.querySelector("#promptInput");
  const counter = document.querySelector("#charCount");
  if (input && counter) {
    const updateCounter = () => counter.textContent = `${input.value.length} / ${input.maxLength}`;
    input.addEventListener("input", updateCounter);
    updateCounter();
  }

  const copyButton = document.querySelector("#copyPrompt");
  const generatedPrompt = document.querySelector("#generatedPrompt");
  const copyStatus = document.querySelector("#copyStatus");

  if (copyButton && generatedPrompt && copyStatus) {
    copyButton.addEventListener("click", async () => {
      if (!generatedPrompt.value.trim()) {
        copyStatus.textContent = "Generate a prompt first.";
        return;
      }

      try {
        await navigator.clipboard.writeText(generatedPrompt.value);
        copyStatus.textContent = "Copied!";
      } catch {
        generatedPrompt.select();
        const copied = document.execCommand("copy");
        copyStatus.textContent = copied ? "Copied!" : "Copy failed. Select the text and copy it manually.";
      }
    });
  }
});
