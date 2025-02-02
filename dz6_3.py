#[ ] Зробити ще один sql скрипт, який буде змінювати таблиці
#* Додає користувачу поле Номер телефону та видаляє Ім’я собаки
#* Додає нову Таблицю “Оцінка ДЗ”
#  1. Id
#  2. Посилання на відповідь
#  3. Дата
#  4. Оцінка
#  5. Посилання на вчителя
#* Додає дедлайн до ДЗ
#* Додає дату здачі до відповіді

ALTER TABLE Users
ADD PhoneNumber VARCHAR(20);

ALTER TABLE Users
DROP COLUMN DogName;

CREATE TABLE Homework_Grades (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    HomeworkAnswerId INT NOT NULL,
    GradeDate DATE NOT NULL,
    Grade INT NOT NULL,
    TeacherId INT NOT NULL,
    FOREIGN KEY (HomeworkAnswerId) REFERENCES Homework_Answers(Id),
    FOREIGN KEY (TeacherId) REFERENCES Users(Id)
);

ALTER TABLE Homework
ADD Deadline DATE;

ALTER TABLE Homework_Answers
ADD SubmissionDate DATE;
