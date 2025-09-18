function checkAnswers() {
    // ✅ Get total number of questions from data attribute
    let total = parseInt(document.getElementById("quizContainer").dataset.total, 10);
    let score = 0;

    for (let i = 1; i <= total; i++) {
        // User's selected answer
        let selected = document.querySelector('input[name="q' + i + '"]:checked');
        // Correct answer from hidden input
        let correct = document.getElementById("answer" + i).value;

        if (selected && selected.value.toUpperCase() === correct.toUpperCase()) {
            score++;
        }
    }

    // ✅ Show result
    document.getElementById("result").innerText =
        "✅ You scored " + score + " out of " + total;
}
