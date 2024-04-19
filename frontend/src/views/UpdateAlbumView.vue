<template>
    <div class="form-container d-flex align-items-center" style="height: 100vh;">
        <div class="col-6 mx-auto">
            <FlashMessage />
            <form autocomplete="off" novalidate @submit.prevent="updateAlbum">
                <fieldset>
                    <legend>Update Album</legend>
                    <div>
                        <label for="title" class="form-label">Title</label>
                        <input type="text" class="form-control" id="title" v-model="title" required>
                    </div>
                    <div>
                        <label for="tracks" class="form-label mt-3">Select Tracks</label>
                        <select multiple="" class="form-select" id="tracks" v-model="selectedTracks">
                            <option v-for="track in allTracks" :key="track.id" :value="track.id">{{ track.title }}
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
            album_id: null,
            title: '',
            file: '',
            description: '',
            allTracks: [],
            selectedTracks: []
        };
    },
    async mounted() {
        this.album_id = this.$route.params.id;
        const [albumResponse, tracksResponse] = await Promise.all([
            axiosClient.get(`/album/${this.album_id}`),
            axiosClient.get(`/available_tracks/${this.album_id}`)
        ]);

        const album = albumResponse.data;
        this.allTracks = tracksResponse.data;

        this.title = album.title;
        this.description = album.description;
        this.selectedTracks = album.tracks.map(track => track.id);
    },
    beforeUnmount() {
        this.$store.dispatch('fetchOrphanTracks');
    },
    methods: {
        handleFileUpload(event) {
            const file = event.target.files[0];
            this.file = file;
        },
        updateAlbum() {
            const formData = new FormData();
            formData.append('title', this.title);
            formData.append('file', this.file);
            formData.append('tracks', this.selectedTracks);
            formData.append('description', this.description);

            axiosClient.put(`/album/${this.album_id}`, formData, {
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
