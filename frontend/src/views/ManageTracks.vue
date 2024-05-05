<template>
    <div>
        <NavAdmin />
        <div class="container py-5">
            <h2 class="mb-4 lead display-4">Tracks</h2>
            <table class="table table-hover text-center">
                <thead>
                    <tr class="table-active">
                        <th class="lead" scope="col">Name</th>
                        <th class="lead" scope="col">Rating</th>
                        <th class="lead" scope="col">Delete</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="track in tracks" :key="track.id" class="table-dark">
                        <td class="text-light align-middle" scope="row">
                            {{ track.title }}
                        </td>
                        <td class="text-body align-middle">{{ track.rating }}</td>
                        <td><button class="btn btn-danger" @click="deleteTrack(track.id)">Remove</button></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import NavAdmin from '@/components/NavAdmin.vue'
import axiosClient from '@/axios';

export default {
    components: {
        NavAdmin
    },
    data() {
        return {
            tracks: []
        };
    },
    mounted() {
        this.fetchTracks();
    },
    methods: {
        fetchTracks() {
            axiosClient.get('/all_tracks')
                .then(response => {
                    this.tracks = response.data;
                })
                .catch(error => {
                    console.error('Failed to fetch tracks:', error);
                });
        },
        deleteTrack(trackId) {
            axiosClient.delete(`/remove_track/${trackId}`)
                .then(response => {
                    this.fetchTracks(); 
                })
                .catch(error => {
                    console.error('Error deleting track:', error);
                });
        }
    }
};
</script>

<style></style>
