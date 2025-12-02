document.getElementById("predictForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    let data = {};
    const inputs = document.querySelectorAll("#predictForm input, #predictForm select");
    inputs.forEach(input => {
        data[input.id] = input.value;
    });

    const response = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    if(result.prediction){
        document.getElementById("result").innerText = "Prediction: " + result.prediction;
    } else {
        document.getElementById("result").innerText = "Error: " + result.error;
    }
});

