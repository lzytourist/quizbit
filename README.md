# QuizBit

### Setup
- `git clone git@github.com:lzytourist/quizbit.git`
- `cd quizbit`
- `pipenv shell && pipenv install` or `pip install -r requirements.txt`
- `python manage.py runserver`
- Import postman API collection.

### Features
- User registration, login and logout
- CRUD feature for question. Only the admin can perform certain operations.
- User practice history.
  - Mark when the first time the question was accessed by the user.
  - Submission time and total time spent for the submission.
  - Correctness and partial marking.
  - Multiple choice for a question.

  
<b>**User have to access the question before submitting the answer.</b>