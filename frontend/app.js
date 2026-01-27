// --------------------
// VOICE INPUT (Speech → Text)
// --------------------
function startVoice() {
    if (!("webkitSpeechRecognition" in window)) {
        alert("Voice input not supported in this browser.");
        return;
    }

    const recognition = new webkitSpeechRecognition();
    recognition.lang = "en-IN";   // English input
    recognition.start();

    recognition.onresult = function (event) {
        document.getElementById("question").value =
            event.results[0][0].transcript;
    };
}

// --------------------
// TRANSLATE FUNCTION
// --------------------
async function translateText(text, targetLang) {
    if (targetLang === "en") return text;

    const response = await fetch(
        `https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=${targetLang}&dt=t&q=` +
        encodeURIComponent(text)
    );

    const data = await response.json();
    return data[0].map(item => item[0]).join("");
}

// --------------------
// MAIN AI CALL
// --------------------
async function askAI() {
    const questionInput = document.getElementById("question");
    const answerBox = document.getElementById("answerBox");
    const language = document.getElementById("language").value;

    const question = questionInput.value.trim();
    if (!question) {
        answerBox.innerHTML = `<div class="alert alert-warning">Enter a question</div>`;
        return;
    }

    answerBox.innerHTML =
        `<div class="alert alert-info">Processing your request...</div>`;

    try {
        const response = await fetch("http://127.0.0.1:8000/query", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                question: question,
                region: "Manipur",
                domain: "Agriculture"
            })
        });

        const data = await response.json();

        let answerText = data.answer || "No response available.";

        // Translate if Manipuri selected
        if (language === "mni") {
            answerText = await translateText(answerText, "mni");
        }

        answerBox.innerHTML = `
            <div class="card p-3">
                <strong>Answer:</strong>
                <p>${answerText}</p>
            </div>`;

        // Speak ONLY if English
        if (language === "en") {
            speakAnswer(answerText);
        }

    } catch (error) {
        answerBox.innerHTML =
            `<div class="alert alert-danger">AI service unavailable</div>`;
    }
}

// --------------------
// TEXT → SPEECH (English Only)
// --------------------
function speakAnswer(text) {
    if (!("speechSynthesis" in window)) return;

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "en-IN";
    speechSynthesis.speak(utterance);
}

