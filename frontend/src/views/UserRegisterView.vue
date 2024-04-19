<template>
    <div class="container margin-top">
        <UserForm @login-event="registerUser" legend="User Registration" />
    </div>
</template>

<script>
import UserForm from '@/components/UserForm.vue';
import axiosClient from '@/axios';

export default {
    components: {
        UserForm
    },

    methods: {
        async registerUser(name, username, email, password, confirmPassword) {
            try {
                const formData = {};
                formData.username = username;
                formData.password = password;
                formData.name = name;
                formData.email = email;
                formData.confirmPassword = confirmPassword;

                const response = await axiosClient.post('/user', formData);
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
