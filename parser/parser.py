import docx
import regex as re
from . import ClosedQuestion, OpenedQuestion, AccordanceQuestion, TYPE_CLOSED_QUESTIONS, TYPE_ACCORDANCE_QUESTIONS, TYPE_OPENED_QUESTIONS


class Paragraph:

    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text


def load_from_text(file):
    with open(file, 'r', encoding="UTF-8") as f:
        text = f.read()
    return [Paragraph(line) for line in text.split('\n')]


def load_questions(paragraphs, quest_type, question_handler=None, answer_handler=None, right_answer_handler=None):
    __is_question = False
    __start_answer = False
    __question = ""
    __answers = []
    __questions = []
    for i in range(len(paragraphs)):
        if paragraphs[i].text.startswith("/////"):
            break
        if len(paragraphs[i].text.strip()) > 0:
            if not __is_question:
                __question += paragraphs[i].text.strip() + "\n"
            else:
                __start_answer = True
                __answers.append(paragraphs[i].text.strip())
        else:
            if __question == "":
                continue
            if not __is_question:
                __is_question = True
                __start_answer = False
                __question = __question.strip()
            elif __start_answer:
                if quest_type == TYPE_CLOSED_QUESTIONS:
                    if question_handler is not None:
                        __question = question_handler(__question)
                    if answer_handler is not None:
                        __new_answers = []
                        for answer in __answers[:-1]:
                            __new_answers.append(answer_handler(answer))
                        __new_answers.append(__answers[-1])
                        __answers = __new_answers
                    if right_answer_handler is not None:
                        __answers[-1] = right_answer_handler(__answers[-1])
                    match_ra = re.findall(r"(Ответ:)?([\w\d]+\W*)", __answers[-1])
                    right_answers = [
                        m[-1].strip(", \t\n.:")
                        for m in filter(lambda m: m[-1].strip(", \t\n.:").lower() != "ответ", match_ra)
                    ]
                    __questions.append(ClosedQuestion(__question, __answers[:-1], right_answers))
                elif quest_type == TYPE_OPENED_QUESTIONS:
                    if question_handler is not None:
                        __question = question_handler(__question)
                    if answer_handler is not None:
                        __answers = list(map(answer_handler, __answers))
                    __questions.append(OpenedQuestion(__question, __answers))
                elif quest_type == TYPE_ACCORDANCE_QUESTIONS:
                    if question_handler is not None:
                        __question = question_handler(__question)
                    if answer_handler is not None:
                        __answers__ = list(map(answer_handler, __answers[:-1]))
                        __answers__.append(__answers[-1])
                        __answers = __answers__
                    if right_answer_handler is not None:
                        __answers[-1] = right_answer_handler(__answers[-1])
                    __questions.append(parse_accordance_question(f"{__question}\n\n"+'\n'.join(__answers)))
                __question = ""
                __answers = []
                __is_question = False
                __start_answer = False
    return __questions


def parse_accordance_question(text):
    lines = text.splitlines()
    question_text = ""
    answers = 0
    for i in range(len(lines)):
        if len(lines[i].strip()) > 0:
            question_text += lines[i] + "\n"
        else:
            answers = i + 1
            break
    question_re = re.match(r'^(\d+\.?)?.*', question_text)
    if question_re and question_re.groups()[0] is not None:
        question_text = question_text.replace(question_re.groups()[0], "").strip()
    column1 = []
    column2 = []
    for answer in lines[answers:-1]:
        delimiter = re.search(r'[\s\t]{3,}', answer).group()
        columns = list(filter(lambda x: len(x) > 0, map(lambda x: x.strip(), re.split(delimiter, answer))))
        column1.append(columns[0])
        column2.append(columns[1])
    match = re.findall(r'(Ответ:)?([\W^\n]*(\d+[\W^\n]+\d+)[\W^\n]*)', lines[-1])
    right = {}
    for m in match:
        rs = re.split("\W+", m[-1])
        if len(rs) == 2:
            right[int(rs[0])] = int(rs[1])
    return AccordanceQuestion(question_text, column1, column2, right)


def load_questions_from_file(file, quest_type, question_handler=None, answer_handler=None, right_answer_handler=None):
    if file.endswith(".txt"):
        paragraphs = load_from_text(file)
    elif file.endswith(".docx"):
        source = docx.Document(file)
        paragraphs = source.paragraphs
    else:
        return None
    return load_questions(paragraphs, quest_type, question_handler, answer_handler, right_answer_handler)


if __name__ == "__main__":
    import regex as re

    questions = load_questions_from_file(
        "./source/closed.txt",
        TYPE_CLOSED_QUESTIONS,
        question_handler=lambda q: re.split('[\t\s\)\.]+', q, 1)[-1].strip(),
        answer_handler=lambda a: re.split('[\t\s\)\.]+', a, 1)[-1].strip(),
        right_answer_handler=lambda a: a.replace("Ответ:", "").strip()
    )

    for question in questions:
        print(question)
