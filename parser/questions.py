TYPE_CLOSED_QUESTIONS = "closed"
TYPE_ACCORDANCE_QUESTIONS = "accordance"
TYPE_OPENED_QUESTIONS = "opened"
STYLES = {}
STEPS = {}


def initialize(styles, steps):
    global STYLES, STEPS
    for key, value in styles.items():
        STYLES[key] = value
    for key, value in steps.items():
        STEPS[key] = value


class ClosedQuestion:

    def __init__(self, question_text: str, answers: list, right_answer: list):
        self.question_text = question_text
        self.answers = answers
        self.right_answer = right_answer

    def __str__(self):
        return "Quest:\t" + self.question_text + "\nAnswers:\n\t" + "\n\t".join(
            self.answers) + "\nRight:\t" + ", ".join(self.right_answer)

    def right(self):
        return ", ".join(self.right_answer)


class AccordanceQuestion:

    def __init__(self, question_text: str, column1: list, column2: list, right_answer: dict):
        self.question_text = question_text
        self.column1 = column1
        self.column2 = column2
        self.right_answer = right_answer

    def __str__(self):
        return "Quest:\t" + self.question_text + \
            "\nAnswers:\n\t" + "\n\t".join(
                [f"{self.column1[i - 1]} -> {self.column2[j - 1]}" for i, j in self.right_answer.items()]) + \
            "\nRight:\t" + ", ".join([f"{k}-{v}" for k, v in self.right_answer.items()])

    def right(self):
        return ", ".join([f"{k}-{chr(ord('А')+v-1)}" for k, v in self.right_answer.items()])


class OpenedQuestion:

    def __init__(self, question_text: str, answers: list):
        self.question_text = question_text
        self.answers = answers

    def __str__(self):
        return "Quest:\t" + self.question_text + "\nAnswers:\n\t" + "\n\t".join(self.answers)

    def right(self):
        return "\n".join(self.answers)
