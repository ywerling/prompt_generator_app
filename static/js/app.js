document.addEventListener("DOMContentLoaded", () => {
  const input = document.querySelector("#promptInput");
  const counter = document.querySelector("#charCount");
  if (!input || !counter) return;
  const updateCounter = () => counter.textContent = `${input.value.length} / ${input.maxLength}`;
  input.addEventListener("input", updateCounter);
  updateCounter();
});
