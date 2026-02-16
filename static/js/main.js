let direction = "roman";

const leftInput = document.getElementById("leftInput");
const rightInput = document.getElementById("rightInput");
const swapBtn = document.getElementById("swap");

function convert() {
    const value = leftInput.value.trim();
    if (value === "") {
        rightInput.value = "";
        return;
    }

    fetch("/convert", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            from: direction,
            value: value
        })
    })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                rightInput.value = "Error";
            } else {
                rightInput.value = data.result;
            }
        })
        .catch(() => {
            rightInput.value = "Server error";
        });
}

leftInput.addEventListener("input", convert);

swapBtn.addEventListener("click", () => {
    direction = direction === "roman" ? "arabic" : "roman";

    const temp = leftInput.value;
    leftInput.value = rightInput.value;
    rightInput.value = temp;

    convert();
});