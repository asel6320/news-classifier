const classifyButton = document.getElementById("classifyButton");
const newsText = document.getElementById("newsText");

const result = document.getElementById("result");
const category = document.getElementById("category");

const businessProbability = document.getElementById("businessProbability");
const sportsProbability = document.getElementById("sportsProbability");
const technologyProbability = document.getElementById("technologyProbability");

const errorMessage = document.getElementById("errorMessage");


classifyButton.addEventListener("click", async function () {

    const text = newsText.value.trim();

    if (!text) {
        errorMessage.textContent = "Please enter some news text.";
        result.classList.add("hidden");
        return;
    }

    errorMessage.textContent = "";
    classifyButton.disabled = true;
    classifyButton.textContent = "Classifying...";

    try {

        const response = await fetch(
            "/predict",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    text: text
                })
            }
        );

        if (!response.ok) {
            throw new Error("Prediction request failed.");
        }

        const data = await response.json();

        category.textContent = data.category;

        businessProbability.textContent =
            data.probabilities.Business + "%";

        sportsProbability.textContent =
            data.probabilities.Sports + "%";

        technologyProbability.textContent =
            data.probabilities.Technology + "%";

        result.classList.remove("hidden");

    } catch (error) {

        errorMessage.textContent =
            "Could not connect to the classification server.";

        result.classList.add("hidden");

    } finally {

        classifyButton.disabled = false;
        classifyButton.textContent = "Classify News";
    }
});