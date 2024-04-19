<template>
    <div class="form-container d-flex align-items-center mt-4" style="height: 80vh;">
        <div class="col-6 mx-auto">
            <FlashMessage />
            <form autocomplete="off" novalidate @submit.prevent="registerCreator">
                <fieldset>
                    <legend class="mb-4 lead display-4">Creator Registration</legend>
                    <div class="row mb-3">
                        <div class="mb-3">
                            <label for="stageName" class="form-label">Stage Name</label>
                            <input type="text" class="form-control" id="stageName" v-model="stageName" required>
                        </div>
                        <div class="mb-3">
                            <label for="bio" class="form-label">Bio</label>
                            <textarea class="form-control" id="bio" v-model="bio" required></textarea>
                        </div>
                        <div class="mb-3">
                            <label for="pfp" class="form-label mt-4">PFP</label>
                            <input class="form-control" type="file" id="pfp" @change="handleFileUpload">
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary">Submit</button>
                </fieldset>
            </form>
        </div>
    </div>
</template>

<script>
import axiosClient from '@/axios';
import FlashMessage from '@/components/FlashMessage.vue';

export default {
    components: {
        FlashMessage
    },
    data() {
        return {
            bio: '',
            pfp: '',
            stageName: ''
        };
    },
    methods: {
        handleFileUpload(event) {
            const file = event.target.files[0];
            this.pfp = file;
        },
        registerCreator() {
            const formData = new FormData();
            formData.append('bio', this.bio);
            formData.append('stageName', this.stageName);
            formData.append('pfp', this.pfp);

            axiosClient
                .post('/artists', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                })
                .then(response => {
                    const data = response.data;
                    this.$store.commit('addUserRole', 'Creator');
                    this.$router.push({ name: 'CreatorDashView' });
                })
                .catch(error => {
                    const errorMessage = error?.response?.data?.message || 'Registration failed';
                    this.$store.commit('addMessage', errorMessage);
                    this.$store.commit('addCategory', 'danger');
                    console.error(error);
                });
        }
    }
};
</script>

<style scoped>

</style>

