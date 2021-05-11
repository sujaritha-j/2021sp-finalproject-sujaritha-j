import json
import os
import re
from contextlib import contextmanager
from pathlib import Path
from pprint import pprint
from typing import Dict, ContextManager
from typing import List

from canvasapi.quiz import QuizSubmissionQuestion, QuizSubmission
from django.core.management import BaseCommand
from dotenv import load_dotenv
from git import Repo

from .canvas_util import get_active_course_by_name
from .canvas_util import get_assignment_by_name
from .canvas_util import get_quiz_by_name

from ...models import DimDate, FactReview


def print_question(self, questions):  # pragma: no cover - print test
    """ Get some basic information about the questions and print it to help develop the code
    :param : questions obj
    """
    for q in questions:
        print("{} - {}".format(q.question_name, q.question_text.split("\n", 1)[0]))
        # MC and some q's have 'answers' not 'answer'
        pprint(
            {
                k: getattr(q, k, None)
                for k in ["question_type", "id", "answers", "answer"]
            }
        )
        print()

def get_reviews_by_date(self, answers):
    """ read the parquet file and match the answers
    :param : dict question
    :return: dict of answers
    """
    return_answer = dict()
    for attribute, value in answers.items():
        date = DimDate.objects\
            .filter\
            (id=FactReview.objects.values('date').order_by('-{}'.format(attribute)).first()['date'])\
            .first()\
            .date\
            .strftime('%Y-%m-%d')
        return_answer[attribute] = str(date)
    return return_answer

def get_answers_hours(self, question, i=0):  # pragma: no cover - not part of final package
    """For multiple choice answer, returns answer_id
    :param: question obj and integer
    :return: str - answer_id
    """
    answer_id = i
    for answers_options in question.answers:
        if "15+" in str(answers_options["text"]):
            answer_id = answers_options["id"]

    return answer_id

def get_true_false_answer(self, question, i=0):  # pragma: no cover - not part of final package
    """For multiple choice answer, returns answer_id
    :param: question obj and int
    :return: str answer id
    """
    answer_id = i
    for answers_options in question.answers:
        if "True" in str(answers_options["text"]):
            answer_id = answers_options["id"]

    return answer_id

def get_git_commit_id(self):  # pragma: no cover - not part of final package
    """
    Gets the git commit id
    :return: str
    """
    git_root_dir = Path(__file__).parents[3]
    repo = Repo(git_root_dir)
    commit_id = repo.head.object.hexsha
    return commit_id.strip()

def get_answers(self, questions: List[QuizSubmissionQuestion], quiz) -> List[
    Dict
]:  # pragma: no cover - not part of final package and it is specific to the questions/answers for this quiz
    """Creates answers for Canvas quiz questions
    : param : questions list, quiz obj
    : return : list
    """
    # Formulate your answers see docs for QuizSubmission.answer_submission_questions below
    # It should be a list of dicts, one per q, each with an 'id' and 'answer' field
    # The format of the 'answer' field depends on the question type
    # You are responsible for collating questions with the functions to call - do not hard code
    answers_list = list()
    for q in questions:
        question_identifier = re.findall(r'id="(\w+)"', q.question_text)
        if "hours" in question_identifier:
            answers_list.append({"id": q.id, "answer": self.get_answers_hours(q)})
        elif "clean" in question_identifier:
            answers_list.append({"id": q.id, "answer": self.get_true_false_answer(q)})
        elif "commit" in question_identifier:
            answers_list.append({"id": q.id, "answer": self.get_git_commit_id()})
        elif "date" in question_identifier:
            answers_list.append({"id": q.id, "answer": self.get_reviews_by_date(q.answer)})
    return answers_list

def get_submission_comments(self, repo: Repo, q_submission: QuizSubmission) -> Dict:
    """Get the required meta data information about this submission
    :param repo : Repo object
    :param q_submission : QuizSubmission
    :returns Dictionary with the required meta data"""
    return dict(
        hexsha=repo.head.commit.hexsha[:8],
        submitted_from=repo.remotes.origin.url,
        dt=repo.head.commit.committed_datetime.isoformat(),
        branch='master',
        is_dirty=repo.is_dirty(),
        quiz_submission_id=q_submission.id,
        quiz_attempt=q_submission.attempt,
        travis_url=os.environ.get("TRAVIS_BUILD_WEB_URL", None),
        use_late_days=os.getenv("LATE_DAYS"),
        document_git_repo="https://github.com/sujaritha-j/2021sp-finalproject-sujaritha-j"  # please update doc
    )

@contextmanager
def submit_assignment(self, quiz, assignment, repo_dir) -> ContextManager:
    """Submits the Assignment with URL to the csci-e-29 repository and commit id information
    :param - quiz object
    :param - assignment object
    :returns - ContextManager object"""
    masquerade = {}
    repo = Repo(repo_dir)
    # # Begin submissions
    url = "https://github.com/sujaritha-j/2021sp-finalproject-sujaritha-j/commit/{}".format(
        repo.head.commit.hexsha
    )

    q_submission = None
    try:
        # Attempt quiz submission first - only submit assignment if successful
        q_submission = quiz.create_submission(**masquerade)
        yield q_submission

    finally:
        if q_submission is not None:
            completed = q_submission.complete(**masquerade)
            print(completed)
            # Only submit assignment if quiz finished successfully
            if completed is not None:
                assignment.submit(
                    dict(
                        submission_type="online_url",
                        url=url,
                    ),
                    comment=dict(
                        text_comment=json.dumps(
                            self.get_submission_comments(repo, q_submission)
                        )
                    ),
                    **masquerade,
                )

def submit_the_assignment(self, quiz,
                          assignment) -> object:  # pragma: no cover - not part of final package and the results are being printed out for verification
    """Submit the assignment and print the responses
    :param : quiz, assignment objects
    """
    masquerade = {}
    git_root_dir = Path(__file__).parents[3]
    with self.submit_assignment(quiz, assignment, git_root_dir) as q_submission:
        questions = q_submission.get_submission_questions(**masquerade)
        self.print_question(questions)
        # Submit your answers
        answers = self.get_answers(questions, quiz)
        responses = q_submission.answer_submission_questions(
            attempt=q_submission.attempt,
            validation_token=q_submission.validation_token,
            quiz_questions=answers,
            **masquerade,
        )
        print(responses)

def start_submission_process(self):  # pragma: no cover - It uses the functions already tested
    """Get the objects needed for the submission process"""
    load_dotenv()
    # get course
    course = get_active_course_by_name(os.getenv("CANVAS_COURSE_NAME"))
    # use course to get assignment and quiz
    assignment = get_assignment_by_name(course, os.getenv("CANVAS_ASSIGN_NAME"))
    quiz = get_quiz_by_name(course, os.getenv("CANVAS_QUIZ_NAME"))
    # call submit assignment
    self.submit_the_assignment(quiz, assignment)
