<template>
  <div>
    <h2>{{ course.title }}</h2>
    <p>{{ course.description }}</p>

    <h3>Завдання</h3>
    <div v-if="error" class="error">{{ error }}</div>
    <ul>
      <li v-for="assignment in assignments" :key="assignment.id">
        <span>{{ assignment.title }} - {{ assignment.due_date }}</span>
      </li>
    </ul>

    <h3>Оцінки</h3>
    <div v-if="ratings.length > 0">
      <p>Оцінка: {{ ratings[0].rating }}</p>
      <p>Коментар: {{ ratings[0].comment }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      course: {},
      assignments: [],
      ratings: [],
      error: ''
    };
  },
  created() {
    this.fetchCourseDetails();
  },
  methods: {
    fetchCourseDetails() {
      const courseId = this.$route.params.id;
      axios.get(`http://localhost:8000/api/courses/${courseId}`)
        .then(response => {
          this.course = response.data;
          this.fetchAssignments(courseId);
          this.fetchRatings(courseId);
        })
        .catch(error => {
          console.error(error.response ? error.response.data : error.message);
          this.error = error.response ? error.response.data.detail : 'Сталася помилка';
        });
    },
    fetchAssignments(courseId) {
      axios.get(`http://localhost:8000/api/assignments/?course=${courseId}`)
        .then(response => {
          this.assignments = response.data;
        })
        .catch(error => {
          console.error(error.response ? error.response.data : error.message);
          this.error = error.response ? error.response.data.detail : 'Сталася помилка';
        });
    },
    fetchRatings(courseId) {
      axios.get(`http://localhost:8000/api/ratings/?course=${courseId}`)
        .then(response => {
          this.ratings = response.data;
        })
        .catch(error => {
          console.error(error.response ? error.response.data : error.message);
          this.error = error.response ? error.response.data.detail : 'Сталася помилка';
        });
    }
  }
};
</script>