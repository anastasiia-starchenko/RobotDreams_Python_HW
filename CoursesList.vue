<template>
  <div>
    <h2>Курси</h2>
    <div v-if="error" class="error">{{ error }}</div>
    <ul>
      <li v-for="course in courses" :key="course.id">
        <router-link :to="'/courses/' + course.id">{{ course.title }}</router-link>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      courses: [],
      error: ''
    };
  },
  created() {
    this.fetchCourses();
  },
  methods: {
    fetchCourses() {
      axios.get('http://localhost:8000/api/courses/')
        .then(response => {
          this.courses = response.data;
        })
        .catch(error => {
          console.error(error.response ? error.response.data : error.message);
          this.error = error.response ? error.response.data.detail : 'Сталася помилка';
        });
    }
  }
};
</script>