from vertexai.generative_models import GenerativeModel

model = GenerativeModel("gemini-2.0-flash-lite-001")

prompt = """
You are provided a markdown file above which contains questions and solutions to math, phyics and chemistry problems
from JEE mains. The document contains rich text with latex equations, tables, chemistry compound diagrams, electric
circuits, geometry diagrams, and some images specific to problems.
Your job is to split the document into questions-solution pairs and tag them with the appropriate topic.
For example, on a math question about derivates, the output should look like:
{
    "question": <text-of-question-with-markdown-formatting-preserved>,
    "solution": <text-of-solution-with-markdown-formatting-preserved>,
    "option-1": <option-1>,
    "option-2": <option-2>,
    "option-3": <option-3>,
    "option-4": <option-4>,
    "option-5": <option-5>,
    "correct-option": <option-number>
    "subject": "math",
    "topic": ["derivatives", "trignometry"],
    "techniques": ["chain rule", "sine rule"],
}
Create this json representation for the 10 question-solution pairs in the markdown file.
If there are no questions in the file, simply return null in all the fields.
"""


def get_all_questions(file) -> list[str]:
    start = 1
    res: list[str] = [""]
    with open(file, "r") as f:
        for line in f:
            if (
                line.find("MATHEMATICS") >= 0
                or line.find("PHYSICS") >= 1
                or line.find("CHEMISTRY") >= 1
            ):
                start = 1
                res.append("")
            elif line.startswith(str(start + 10) + ". "):
                res.append("")
                start += 10
            res[-1] += line
    return res


# test = get_all_questions("jee_2025_ph_1.md")
# print(len(test))
# print(test[1])

tagged_output = ""
for questions in get_all_questions("jee_2025_ph_1.md"):
    response = model.generate_content([questions, prompt])
    tagged_output += response.text
    print("got output for one list of questions")

    # ser: str = json.loads(response.text)
with open("tagged_questions.json", "w") as f:
    f.write(tagged_output)
