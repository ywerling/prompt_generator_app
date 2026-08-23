document.addEventListener("DOMContentLoaded", () => {
  const input = document.querySelector("#promptInput");
  const counter = document.querySelector("#charCount");
  if (input && counter) {
    const updateCounter = () => counter.textContent = `${input.value.length} / ${input.maxLength}`;
    input.addEventListener("input", updateCounter);
    updateCounter();
  }

  document.querySelectorAll("[data-copy-target]").forEach((copyButton) => {
    copyButton.addEventListener("click", async () => {
      const target = document.getElementById(copyButton.dataset.copyTarget);
      const status = copyButton.parentElement.querySelector(".copy-status");
      const text = target?.value ?? target?.textContent ?? "";
      if (!text.trim()) {
        status.textContent = "Generate a prompt first.";
        return;
      }
      try {
        await navigator.clipboard.writeText(text.trim());
        status.textContent = "Copied!";
      } catch {
        if (typeof target.select === "function") target.select();
        const copied = document.execCommand("copy");
        status.textContent = copied ? "Copied!" : "Copy failed. Select the text and copy it manually.";
      }
    });
  });

  document.querySelectorAll("[data-randomize-form]").forEach((button) => {
    button.addEventListener("click", () => {
      button.closest("form").querySelectorAll("select[data-randomizable]").forEach((select) => {
        const firstChoice = select.options.length > 1 ? 1 : 0;
        select.selectedIndex = firstChoice + Math.floor(Math.random() * (select.options.length - firstChoice));
        select.dispatchEvent(new Event("change", { bubbles: true }));
      });
    });
  });
});
