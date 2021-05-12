import json
import os
from contextlib import contextmanager
from typing import ContextManager
from typing import Dict

from canvasapi import Canvas
from canvasapi.quiz import QuizSubmission
from git import Repo


def get_canvas() -> object:
    """
    Get the Canvas object. Read the environmental variables for URL and Access token of canvas

    :return: Returns Canvas object
    """
    return Canvas(os.getenv("CANVAS_URL"), os.getenv("CANVAS_TOKEN"))


def get_active_course_by_name(
    course_name: str = "Advanced Python for Data Science",
) -> object:
    """
    Gets the list of all courses, compares it with the course name passed as an argument
    and returns the matching course object.

    :param:(course_name): Course name as string to compare against courses

    :return: Returns the course object
    """

    courses = get_canvas().get_courses()
    for course in courses:
        if course_name == str(course.name):
            return course


def get_assignment_by_name(course: object, assign_name: str = "Final Project") -> object:
    """

    Gets the list of all assignments for a course, compares it with the assignment name passed as an argument
    and returns the course object for the assignment id.

    :param: (course): course object

    :param: (assign_name): Assignment name as string to compare against all assignments

    :return: (assignment_id): Returns the Assignment id for the course object

    """
    assignments = course.get_assignments()
    for assignment in assignments:
        if assign_name == str(assignment.name):
            return course.get_assignment(assignment.id)


def get_quiz_by_name(course: object, quiz_name: str = "Test Quiz") -> object:
    """

    Gets the list of all quizzes for a course, compares it with the quiz name passed as an argument
    and returns the course object for the quiz id.

    :param:(course): course object

    :param: (quiz_name): Quiz name as string to compare against all assignments

    :return:(course obj): Quiz id of the course object
    """

    quizzes = course.get_quizzes()
    for quiz in quizzes:
        if quiz_name == str(quiz.title):
            return course.get_quiz(quiz.id)


def get_submission_comments(repo: Repo, q_submission: QuizSubmission) -> Dict:
    """Get the required meta data information about this submission
    :param repo : Repo object
    :param q_submission : QuizSubmission
    :returns Dictionary with the required meta data"""
    return dict( #pragma: no_cover
        hexsha=repo.head.commit.hexsha[:8],
        submitted_from=repo.remotes.origin.url,
        dt=repo.head.commit.committed_datetime.isoformat(),
        branch=os.environ.get("TRAVIS_BRANCH", None),  # repo.active_branch.name,
        is_dirty=repo.is_dirty(),
        quiz_submission_id=q_submission.id,
        quiz_attempt=q_submission.attempt,
        travis_url=os.environ.get("TRAVIS_BUILD_WEB_URL", None),
        use_late_days=os.getenv("LATE_DAYS"),
    )


@contextmanager
def submit_assignment(quiz, assignment, repo_dir) -> ContextManager: #pragma: no_cover
    """
    Submits the Assignment with URL to the csci-e-29 repository and commit id information

    :param: quiz object

    :param: assignment object

    :return: Returns ContextManager object"""

    masquerade = {}
    repo = Repo(repo_dir)
    # # Begin submissions
    url = "https://github.com/sujaritha-j/2021sp-finalproject-sujaritha-j/commit/{}".format(
        repo.head.commit.hexsha
    )  # you MUST push to the classroom org, even if CI/CD runs elsewhere
    # # (you can push anytime before peer review begins)

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
                            get_submission_comments(repo, q_submission)
                        )
                    ),
                    **masquerade,
                )
