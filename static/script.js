const card = document.querySelector(".container");

document.addEventListener("mousemove", (e) => {
    if (!card) return;
    let x = (window.innerWidth/2 - e.pageX)/25;
    let y = (window.innerHeight/2 - e.pageY)/25;
    card.style.transform = `rotateY(${x}deg) rotateX(${y}deg)`;
});
