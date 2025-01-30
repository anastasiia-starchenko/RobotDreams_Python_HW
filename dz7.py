#На базі бази даних з попереднього домашнього завдання створити інтернет-сторінку для LMS
#Мають оброблятися таки запити:
#[ ] GET та POST /register — сторінка реєстрації.
#  * email
#  * пароль
#  * ім’я
#  * прізвище
#[ ] GET /users — список користувачів (усі поля).
#[ ] GET /courses — список курсів (усі поля).
#[ ] GET та POST /courses/create — сторінка створення курсу
#  * назва
#  * ID викладача
#  * список ID студентів
#[ ] GET /courses/<course_id> — вся інформація щодо курсу (назва, студенти, лекції, домашні завдання).
#[ ] GET та POST /courses/<course_id>/lectures — сторінка додавання заняття до курсу
#  * назва
#  * опис
#[ ] GET та POST /courses/<course_id>/tasks — сторінка домашнього завдання
#  * опис
#[ ] GET та POST /courses/<course_id>/tasks/<task_id>/answers — сторінка відповіді на домашнє завдання
#  * опис
#  * ID студента
#[ ] GET та POST /courses/<course_id>/tasks/<task_id>/answers/<answer_id>/mark — сторінка оцінки відповіді на домашнє завдання
#  * дата
#  * оцінка
#  * ID вчителя
#[ ] GET та POST /courses/<course_id>/rating — сторінка рейтингу
#  * повертає список усіх студентів та їхню середню оцінку
#  * студенти відсортовані за середньою оцінкою за завдання
#  * сортування та агрегація потрібно зробити через SQL

const express = require('express');
const mysql = require('mysql2');
const bodyParser = require('body-parser');

const app = express();

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'example',
  database: 'PostgreSQL'
});

db.connect((err) => {
  if (err) {
    console.error('Database connection error: ', err.stack);
    return;
  }
  console.log('Successful database connection');
});

app.route('/register')
  .get((req, res) => {
    res.send(`
      <h2>Реєстрація</h2>
      <form action="/register" method="POST">
        <input type="email" name="email" placeholder="Email" required><br>
        <input type="password" name="password" placeholder="Пароль" required><br>
        <input type="text" name="firstName" placeholder="Ім'я" required><br>
        <input type="text" name="lastName" placeholder="Призвище" required><br>
        <button type="submit">Зареєструватися</button>
      </form>
    `);
  })
  .post((req, res) => {
    const { email, password, firstName, lastName } = req.body;

    const query = 'INSERT INTO Users (Email, Password, FirstName, LastName) VALUES (?, ?, ?, ?)';

    db.query(query, [email, password, firstName, lastName], (err, result) => {
      if (err) {
        res.status(500).send('Error during registration');
        return;
      }
      res.send('Successful registration');
    });
  });


app.get('/users', (req, res) => {
  const query = 'SELECT * FROM Users';
  db.query(query, (err, results) => {
    if (err) {
      res.status(500).send('Error retrieving user data');
      return;
    }
    res.json(results);
  });
});


app.get('/courses', (req, res) => {
  const query = 'SELECT * FROM Courses';
  db.query(query, (err, results) => {
    if (err) {
      res.status(500).send('Error retrieving course data');
      return;
    }
    res.json(results);
  });
});

(GET та POST /courses/create)
app.route('/courses/create')
  .get((req, res) => {
    res.send(`
      <h2>Створити курс</h2>
      <form action="/courses/create" method="POST">
        <input type="text" name="name" placeholder="Назва курсу" required><br>
        <input type="text" name="teacherId" placeholder="ID викладача" required><br>
        <input type="text" name="studentIds" placeholder="ID студентів (через кому)" required><br>
        <button type="submit">Створити курс</button>
      </form>
    `);
  })
  .post((req, res) => {
    const { name, teacherId, studentIds } = req.body;
    const studentsArray = studentIds.split(',').map(id => id.trim());

    const query = 'INSERT INTO Courses (Name, TeacherId) VALUES (?, ?)';

    db.query(query, [name, teacherId], (err, result) => {
      if (err) {
        res.status(500).send('Error creating course');
        return;
      }

      const courseId = result.insertId;  // Отримуємо ID створеного курсу
      const studentQuery = 'INSERT INTO Course_Students (CourseId, StudentId) VALUES ?';


      const studentValues = studentsArray.map(studentId => [courseId, studentId]);

      db.query(studentQuery, [studentValues], (err) => {
        if (err) {
          res.status(500).send('Error adding students to course');
          return;
        }
        res.send('Course successfully created');
      });
    });
  });


const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Сервер працює на порту ${PORT}`);
});
