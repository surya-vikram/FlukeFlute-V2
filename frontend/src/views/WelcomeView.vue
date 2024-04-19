<template>
    <div class="container d-flex flex-column align-items-center gap-3">
        <div class="jumbotron text-center">
            <h1 class="display-4">Musical Serendipity Awaits You</h1>
            <p class="lead">Experience the magic of music like never before!</p>
        </div>
        <router-link to="/register/user" class="btn btn-outline-primary w-50" role="button">Sign Up</router-link>
        <router-link to="/login/user" class="btn btn-outline-primary w-50" role="button">Sign In</router-link>
        <router-link to="/login/admin" class="btn btn-outline-primary w-50" role="button">Admin</router-link>
    </div>
</template>

<script>
export default {
    name: 'WelcomeView'
}
</script>

<style scoped>
.container {
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>
