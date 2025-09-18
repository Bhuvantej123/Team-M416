function checkAnswers() {
            let total = parseInt("{{ quiz.questions|length or 0 }}");
            let score = 0;

            for (let i = 1; i <= total; i++) {
                let selected = document.querySelector('input[name="q' + i + '"]:checked');
                let correct = document.querySelector('input[name="answer' + i + '"]').value;

                if (selected && selected.value === correct) {
                    score++;
                }
            }

            document.getElementById("result").innerText =
                "You scored " + score + " out of " + total;
        }