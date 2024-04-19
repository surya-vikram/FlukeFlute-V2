<template>
    <div class="form-container d-flex align-items-center mt-4" style="height: 90vh;">
        <div class="col-6 mx-auto">
            <FlashMessage />
            <form autocomplete="off" novalidate @submit.prevent="handleLogin">
                <fieldset>
                    <legend class="lead display-4 mb-4">{{ legend }}</legend>
                    <div class="row mb-3">
                        <div class="mb-3">
                            <label for="username" class="form-label">Username</label>
                            <input type="text" class="form-control" id="username" v-model="username" required>
                        </div>
                        <div class="mb-3">
                            <label for="password" class="form-label">Password</label>
                            <input type="password" class="form-control" id="password" v-model="password" required>
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
            username: '',
            password: ''
        };
    },
    methods: {
        handleLogin() {
            this.$emit('login-event', this.username, this.password);
        }
    }
};
</script>

<style scoped>

</style>