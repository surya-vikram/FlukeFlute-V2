<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App',
  mounted() {
    this.$store.dispatch('fetchLanguages');
    this.$store.dispatch('fetchGenres');
  }
};
</script>


