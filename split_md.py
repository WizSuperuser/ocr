import re
import json
from typing import Literal

import instructor
from pydantic import BaseModel, Field
from vertexai.generative_models import GenerativeModel


class Question(BaseModel):
    question: str = Field(..., description="text of question with all rich text preserved")
    solution: str = Field(..., description="text of solution with all rich text preserved")
    type: Literal["mcq", "numerical"] = Field(
        ..., description="type of question: either 'mcq' or 'numerical'"
    )
    option_1: str = Field(
        ..., description="option 1 of the mcq type question with all rich text preserved"
    )
    option_2: str = Field(
        ..., description="option 2 of the mcq type question with all rich text preserved"
    )
    option_3: str = Field(
        ..., description="option 3 of the mcq type question with all rich text preserved"
    )
    option_4: str = Field(
        ..., description="option 4 of the mcq type question with all rich text preserved"
    )
    option_5: str = Field(
        ..., description="option 5 of the mcq type question with all rich text preserved"
    )
    correct_option: Literal["1", "2", "3", "4", "5"] = Field(
        ..., description="correct answer to the mcq type question as an option number"
    )
    correct_answer: str = Field(
        ..., description="answer if the question is a numerical type"
    )
    subject: Literal["physics", "chemistry", "math"] = Field(
        ..., description="one of physics, chemistry, math"
    )
    topics: list[str] = Field(
        ..., description="topics relevant to the question and JEE mains, example: derivatives, trignometry"
    )
    techniques: list[str] = Field(..., description="techniques used to solve the problem, example: chain rule, sine rule")




ins_client = instructor.from_vertexai(
    client = GenerativeModel("gemini-2.0-flash-lite-001"),
    mode=instructor.Mode.VERTEXAI_TOOLS,
)

prompt = """
You are provided a markdown file above which contains a question and solution to a math, phyics or chemistry problem
from JEE mains. The document may contain rich text with latex equations, tables, chemistry compound diagrams, electric
circuits, geometry diagrams, and some images specific to the problem. The questions may be mcq type or numerical answer type.
Your job is to convert the questions-solution pair to the JSON schema below and tag them with the appropriate topic.
Make sure to include all the rich text including image tags and links.

For example, on a math question about derivates, the output should look like:
{
    "question": <text-of-question-with-all-rich-text-preserved>,
    "solution": <text-of-solution-with-all-rich-text-preserved>,
    "type": <whether-mcq-type-or-numerical-type>,
    "option-1": <option-1>,
    "option-2": <option-2>,
    "option-3": <option-3>,
    "option-4": <option-4>,
    "option-5": <option-5>,
    "correct-option": <option-number>,
    "correct-answer": <correct-numerical-answer-for-numerical-types>,
    "subject": "math",
    "topic": ["derivatives", "trignometry"],
    "techniques": ["chain rule", "sine rule"],
}

If there is no such question-answer pair in the file, return a single json entry with null values.
Do not remove any links and images in the text.
"""


def get_all_questions(file: str) -> list[str]:
    res: list[str] = [""]
    pattern = re.compile(r"^\d+. ")
    banner_image = re.compile(r".*height=3[3-4][0-9]&width=17[8-9][0-9]&top_left_y=22[4-5][0-9]&top_left_x=1[4-5][0-9]\)$")
    with open(file, "r") as f:
        for line in f:
            if banner_image.match(line):
                continue
            if pattern.match(line):
                res.append("")
            res[-1] += line
    return res[1:]


test = get_all_questions("allen-jan-2024.md")
print(len(test))
print(test[6])
# print(test[2])
# with open("all_questions.md", "w") as f:
#     f.write("\n".join(test))


tagged_output: list[Question] = []
i = 0
for questions in get_all_questions("allen-jan-2024.md")[6:7]:
    response = ins_client.create(
        messages=[
            {
                "role": "user",
                "content": questions,
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        response_model=Question,
    )
    i += 1
    if response.question == "":
        print(f"{i}: discarded")
        continue
    tagged_output.append(response)
    print(f"{i}: tagged")

# print(tagged_output)
print("")
print("======================")
print("")

with open("test_questions.json", "w") as f:
    questions_with_extracted_images = [question.model_dump() for question in tagged_output]
    for question in questions_with_extracted_images:
        question["images"] = []
        pattern = re.compile(r"!\[\]\(.*\)")
        question["images"] += pattern.findall(question["question"])
        question["images"] += pattern.findall(question["solution"])
    json_list = json.dumps(questions_with_extracted_images)
    f.write(json_list)




# ###########################
# IGNORE
# ###########################
# client = genai.Client(
#     vertexai=True,
#     project="dreambridge-api",
#     location="asia-south1",
# )

# model = GenerativeModel("gemini-2.0-flash-lite-001")
# llm = ChatVertexAI(model="gemini-2.0-flash-lite-001")
# questions = get_all_questions("allen-jan-2024.md")[10]
#
# response = client.models.generate_content(
#     model="gemini-2.0-flash-lite-001",
#     contents=[questions, prompt],
#     config=types.GenerateContentConfig(
#         response_mime_type="application/json",
#         response_schema=list[Question],
#     ),
# )
# structured_llm = llm.with_structured_output(Question)
# response = structured_llm.invoke()
# response = model.generate_content(
#     contents=[questions, prompt],
#     generation_config=GenerationConfig(
#         response_mime_type="application/json",
#         response_schema=question_json,
#     )
# )
# response = structured_llm.invoke([questions, prompt])

# tagged_output += response["text"]
# print("got output for one list of questions")
