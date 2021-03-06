""" private command, not callable """
from random import choice

# thanks Erik!
WELCOME_MSG = """Welcome {user}++!

Introduce yourself if you like ...
- What do you use Python for?
- What is your day job?
- And: >>> random.choice(pybites_init_questions)
{welcome_question}

Although you will meet some awesome folks here, you can also talk to me :)
Type `help` in a direct message to me (@karmabot) to get started ...

Enjoy PyBites Slack and keep calm and code in Python!
@bbelderbos and @julian.sequeira
"""
# some Pythonic welcome questions
WELCOME_QUESTIONS = """How did you use Python for the first time?
What is your favorite Python module?
What was the last Python book you read?
Did you go to Pycon? If so what was the best you got out of it?
Do you have any particular interest or hobby?
How did you hear about PyBites?
What is your favorite software principle of the Zen of Python (import this)
Are you a 100 Days of Code survivor or planning to take the challenge?
What is your favorite TV show, movie or book?
How many Christopher Nolan movies did you see? If > 1 favorite?
If you were to build a chatbot what would it do?
AI, hype or life threatening?
How do you currently use Python?
Are you teaching Python or inspire to do so?
Australia or Spain?
Star Trek or Star Wars?
Tabs or spaces? (be careful!)
Do you use test drive development (TDD)?
What is your favorite editor?
What other programming languages do you know and/or use?"""


def welcome_user(user):
    """Welcome a new PyBites community member"""
    questions = WELCOME_QUESTIONS.split('\n')
    random_question = choice(questions)
    return WELCOME_MSG.format(user=user['name'],
                              welcome_question=random_question)


if __name__ == '__main__':
    output = welcome_user(dict(name='bob'))
    print(output)
