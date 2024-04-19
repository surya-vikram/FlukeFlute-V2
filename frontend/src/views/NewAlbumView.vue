<template>
    <div class="form-container d-flex align-items-center" style="height: 100vh;">
        <div class="col-6 mx-auto">
            <FlashMessage />
            <form autocomplete="off" novalidate @submit.prevent="uploadAlbum">
                <fieldset>
                    <legend>New Album</legend>
                    <div>
                        <label for="title" class="form-label">Title</label>
                        <input type="text" class="form-control" id="title" v-model="title" required>
                    </div>
                    <div>
                        <label for="tracks" class="form-label mt-3">Select Tracks</label>
                        <select multiple="" class="form-select" id="tracks" v-model="selectedTracks">
                            <option v-for="track in orphanTracks" :key="track.id" :value="track.id">{{ track.title }}
                            </option>
                        </select>
                    </div>
                    <div>
                        <label for="formFile" class="form-label mt-3">Cover Image</label>
                        <input class="form-control" type="file" id="formFile" @change="handleFileUpload">
                    </div>
                    <div>
                        <label for="description" class="form-label mt-3">Description</label>
                        <textarea class="form-control" id="description" rows="3" v-model="description"></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary mt-4">Submit</button>
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
            title: '',
            file: '',
            description: '',
            orphanTracks: this.$store.state.orphanTracks, 
            selectedTracks: []
        };
    },
    mounted() {
        this.$store.dispatch('fetchOrphanTracks');
    },
    beforeUnmount() {
        this.$store.dispatch('fetchOrphanTracks'); 
    },
    methods: {
        handleFileUpload(event) {
            const file = event.target.files[0];
            this.file = file;
        },
        uploadAlbum() {
            const formData = new FormData();
            formData.append('title', this.title);
            formData.append('file', this.file);
            formData.append('tracks', this.selectedTracks); 
            formData.append('description', this.description);
            console.log(formData)
            axiosClient
                .post('/albums', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                })
                .then(response => {
                    this.$router.push({ name: 'CreatorDashView' });
                })
                .catch(error => {
                    console.error(error);
                    const errorMessage = error?.response?.data?.message || 'Error Occured !';
                    this.$store.commit('addMessage', errorMessage);
                    this.$store.commit('addCategory', 'danger');
                });
        }
    }
};
</script>

<style></style>

