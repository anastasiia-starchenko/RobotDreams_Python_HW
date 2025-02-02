# Описати за допомогою SQL систему таблиць, яка буде зберігати інформацію для школи:
#* Користувач
#  1. Id
#  2. Email
#  3. Пароль
#  4. Ім’я
#  5. Прізвище
#  6. Ім’я собаки
#  7. Фото (Опціонально)

#* Курс
#  1. Id
#  2. Посилається на користувача в ролі викладача
#  3. Посилається на багато користувачів в ролі студента
#  4. Назва
#  5. Опис

#* Заняття
#  a. Id
#  b. Посилається на курс
#  c. Назва
#  d. Опис

#* Домашнє завдання
#  1. Id
#  2. Посилається на курс
#  3. Опис
#  4. Максимальна оцінка

#* Відповідь на домашнє завдання
#  1. Id
#  2. Посилається на завдання
#  3. Опис
#  4. Посилається на студента
#  5. Оцінка


INSERT INTO Users (Id, Email, Password, FirstName, LastName, DogName, PhotoUrl)
VALUES
    (1, 'ns2303603@gmail.com', '12345', 'Anastasiia', 'Starchenko', 'Sharik', NULL);

INSERT INTO Users (Id, Email, Password, FirstName, LastName, DogName, PhotoUrl)
VALUES
    (2, 'ihor.harahatiy@lms.com', 'helloworld', 'Ihor', 'Harahatiy', NULL, NULL);

INSERT INTO Courses (Id, TeacherId, Name, Description)
VALUES
    (1, 2, 'robot_dreams', 'Python для веб розробки');

INSERT INTO Course_Students (CourseId, StudentId)
VALUES
    (1, 1);

INSERT INTO Lessons (Id, CourseId, Name, Description)
VALUES
    (1, 1, 'Database', 'Вступ до баз даних. Посилання на заняття: https://lms.robotdreams.cc/course/2169/lesson/39429');
INSERT INTO Lessons (Id, CourseId, Name, Description)
VALUES
    (1, 1, 'Database', 'Вступ до баз даних. Посилання на заняття: https://lms.robotdreams.cc/course/2169/lesson/39429');

INSERT INTO Homework (Id, CourseId, Description, MaxGrade)
VALUES
    (1, 1, 'Вступ до баз даних. Виконати завдання 6.', 6);

INSERT INTO Homework_Answers (Id, HomeworkId, Description, StudentId, Grade)
VALUES
    (1, 1, 'Відповідь на завдання доступна за посиланням: https://lms.robotdreams.cc/course/2169/lesson/39429', 1, 6);
