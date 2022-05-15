const allRanges = document.querySelectorAll(".range-wrap");
allRanges.forEach(wrap => {
  const range = wrap.querySelector(".range");
  const bubble = wrap.querySelector(".bubble");

  range.addEventListener("input", () => {
    setBubble(range, bubble);
  });
  setBubble(range, bubble);
});

function setBubble(range, bubble) {
  const val = range.value;
  const min = range.min ? range.min : -1;
  const max = range.max ? range.max : 10;
  const newVal = Number(((val - min) * 40) / (max - min));
  if (val!=-1){
    bubble.innerHTML = val;
  }
  else{
    bubble.innerHTML = "Aucune valeur"
  }

  // Sorta magic numbers based on size of the native UI thumb
  bubble.style.left = `calc(${newVal}% + (${8.5 - newVal * 0.5}px))`;
}