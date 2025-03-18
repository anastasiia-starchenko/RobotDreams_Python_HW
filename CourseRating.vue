<template>
  <div>
    <h3>Оцінка курсу</h3>
    <form @submit.prevent="submitRating">
      <input v-model="rating" type="number" min="1" max="5" placeholder="Ваша оцінка" />
      <textarea v-model="comment" placeholder="Коментар"></textarea>
      <button type="submit">Оцінити</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      rating: '',
      comment: ''
    };
  },
  methods: {
    submitRating() {
      const courseId = this.$route.params.id;
      axios.post('http://localhost:8000/api/ratings/', {
        course: courseId,
        rating: this.rating,
        comment: this.comment
      })
      .then(response => {
        alert('Оцінка успішно додана!');
      })
      .catch(error => {
        console.error(error.response ? error.response.data : error.message);
        this.error = error.response ? error.response.data.detail : 'Сталася помилка';
      });
    }
  }
};
</script>