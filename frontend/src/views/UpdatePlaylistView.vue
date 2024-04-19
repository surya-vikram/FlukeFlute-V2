<template>
    <div class="form-container d-flex align-items-center" style="height: 100vh;">
        <div class="col-6 mx-auto">
            <FlashMessage />
            <form autocomplete="off" novalidate @submit.prevent="updatePlaylist">
                <fieldset>
                    <legend class="lead display-4 mb-4">Update Playlist</legend>
                    <div>
                        <label for="name" class="form-label">Name</label>
                        <input type="text" class="form-control" id="name" v-model="name" required>
                    </div>
                    <div>
                        <label for="tracks" class="form-label mt-3">Select Tracks</label>
                        <select multiple class="form-select" id="tracks" v-model="selectedTracks">
                            <option v-for="track in tracks" :key="track.id" :value="track.id">{{ track.title }}</option>
                        </select>
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
            name: '',
            tracks: [],
            selectedTracks: []
        };
    },
    mounted() {
        this.fetchTracks();
        this.fetchSelectedTracks();
    },
    methods: {
        fetchTracks() {
            axiosClient.get('/tracks')
                .then(response => {
                    this.tracks = response.data;
                })
                .catch(error => {
                    console.error('Error fetching tracks:', error);
                });
        },
        fetchSelectedTracks() {
            axiosClient.get(`/playlist/${this.$route.params.id}`)
                .then(response => {
                    this.name = response.data.name;
                    this.selectedTracks = response.data.tracks.map(track => track.id);
                })
                .catch(error => {
                    console.error('Error fetching tracks:', error);
                });
        },
        updatePlaylist() {
            axiosClient.put(`/playlist/${this.$route.params.id}`, {
                name: this.name,
                track_ids: this.selectedTracks
            })
                .then(response => {
                    this.$router.push({ name: 'UserPlaylistsView' });
                })
                .catch(error => {
                    console.error('Error updating playlist:', error);
                });
        }
    }
};
</script>

<style>
/* Add custom styles if needed */
</style>
