<template>
    <div class="container margin-top">
        <LoginForm @login-event="loginUser" legend="User Login" />
    </div>
</template>

<script>
import LoginForm from '@/components/LoginForm.vue';
import axiosClient from '@/axios';

export default {
    components: {
        LoginForm
    },

    methods: {
        async loginUser(username, password) {
            try {
                const formData = {
                    username: username,
                    password: password
                };

                const response = await axiosClient.post('/login/user', formData);
                const data = response.data;

                if (data) {                    
                    localStorage.setItem('access_token', data.access_token);
                    this.$store.commit('setUserId', data.user_id);
                    this.$store.commit('setUserRoles', data.roles);
                    this.$router.push({ name: 'UserDashView' });
                } else {
                    throw new Error('Invalid response from server');
                }

            } catch (error) {
                const errorMessage = error?.response?.data?.message || 'Login failed';
                this.$store.commit('addMessage', errorMessage);
                this.$store.commit('addCategory', 'danger');
                console.error(error);
            }
        }
    }
};
</script>

<style scoped>

</style>

