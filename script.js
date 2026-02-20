document.addEventListener("DOMConentLoaded", function() {
    const heading = document.querySelector("h1");

    if (heading) {
        heading.addEventListener("click", function() {
            heading.textContent = "You clicked the heading!";
        });
    }
});


function releaseDucks(count = 30) {

  let container = document.querySelector(".duck-confetti");

  if (!container) {
    container = document.createElement("div");
    container.className = "duck-confetti";
    document.body.appendChild(container);
  }

  for (let i = 0; i < count; i++) {

    const duck = document.createElement("img");
    duck.src = "images/duck.png";
    duck.className = "duck";

    // random horizontal position
    duck.style.left = Math.random() * 100 + "vw";

    // random size
    const size = 60 + Math.random() * 60;
    duck.style.width = size + "px";

    // random fall duration
    const duration = 6 - size / 30;
    duck.style.animationDuration = duration + "s";

    // random delay
    duck.style.animationDelay = Math.random() * 0.5 + "s";

    container.appendChild(duck);

    // remove after animation finishes
    setTimeout(() => {
      duck.remove();
    }, duration * 1000 + 1000);
  }
}

document.addEventListener("DOMContentLoaded", () => {

  if (window.location.pathname.includes("collection.html")) {
    releaseDucks(80);
  }

});
