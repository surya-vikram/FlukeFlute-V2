<template>
    <div class="form-container d-flex align-items-center mt-4" style="height: 90vh;">
        <div class="col-6 mx-auto">
            <FlashMessage />
            <form autocomplete="off" novalidate @submit.prevent="handleLogin">
                <fieldset>
                    <legend class="mb-3">{{ legend }}</legend>
                    <div class="row mb-3">
                        <div class="mb-3">
                            <label for="name" class="form-label">Name</label>
                            <input type="text" class="form-control" id="name" v-model="name" required>
                        </div>
                        <div class="mb-3">
                            <label for="username" class="form-label">Username</label>
                            <input type="text" class="form-control" id="username" v-model="username" required>
                        </div>
                        <div class="mb-3">
                            <label for="email" class="form-label">Email</label>
                            <input type="email" class="form-control" id="email" v-model="email" required>
                        </div>
                        <div class="mb-3">
                            <label for="password" class="form-label">Password</label>
                            <input type="password" class="form-control" id="password" v-model="password" required>
                        </div>
                        <div class="mb-3">
                            <label for="confirm_password" class="form-label">Confirm Password</label>
                            <input type="password" class="form-control" id="confirm_password" v-model="confirmPassword"
                                required>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary">Submit</button>
                </fieldset>
            </form>
        </div>
    </div>
</template>

<script>

import FlashMessage from '@/components/FlashMessage.vue';

export default {
    components: {
        FlashMessage
    },
    props: [
        'legend'
    ],
    data() {
        return {
            name: '',
            username: '',
            email: '',
            password: '',
            confirmPassword: ''
        };
    },
    methods: {
        handleLogin() {
            this.$emit('login-event', this.name, this.username, this.email, this.password, this.confirmPassword);
        }
    }
};
</script>

<style scoped>

</style>
