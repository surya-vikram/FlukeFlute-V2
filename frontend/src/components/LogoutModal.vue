<template>
    <div>
        <button class="nav-link" @click="displayModal">Logout</button>
        <div class="modal" :class="{ 'show': showModal }">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title lead">Confirm Logout Request !</h5>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" @click="hideModal">Cancel</button>
                        <button type="button" class="btn btn-primary" @click="logoutUser"><i class="bi bi-box-arrow-right"></i></button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            showModal: false
        };
    },
    methods: {
        logoutUser() {
            this.showModal = false;
            localStorage.removeItem('access_token');
            this.$router.push({ name: 'WelcomeView' });
        },
        displayModal() {
            this.showModal = true;
        },
        hideModal() {
            this.showModal = false;
        }
    }
};
</script>

<style scoped>
</style>
