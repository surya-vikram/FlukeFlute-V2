<template>
    <div class="">
        <NavUser />
        <div class="container py-5">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h1 class="display-4 lead">Playlists</h1>
                <router-link class="btn btn-primary" to="/new_playlist">Create New</router-link>
            </div>
            <table class="table table-hover text-center">
                <thead>
                    <tr class="table-active">
                        <th class="lead" scope="col">Name</th>
                        <th class="lead">Edit</th>
                        <th class="lead">Delete</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="playlist in playlists" :key="playlist.id" class="table-dark">
                        <td class="text-light align-middle" scope="row">
                            <router-link :to="{ name: 'UserPlaylistView', params: { id: playlist.id } }">
                                {{ playlist.name }}
                            </router-link>
                        </td>
                        <td>
                            <button class="btn btn-info" @click="editPlaylist(playlist.id)">Edit</button>
                        </td>
                        <td>
                            <button class="btn btn-danger" @click="confirmDelete(playlist.id)">Delete</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import NavUser from '@/components/NavUser.vue';
import axiosClient from '@/axios';

export default {
    components: {
        NavUser
    },
    data() {
        return {
            playlists: [] 
        };
    },
    created() {
        this.fetchPlaylists();
    },
    methods: {

        editPlaylist(id) {
            this.$router.push({ name: 'UpdatePlaylistView', params: { id: id } });
        },
        confirmDelete(id) {
            if (confirm('Are you sure you want to delete this playlist?')) {
                this.deletePlaylist(id);
            }
        },
        deletePlaylist(id) {
            axiosClient.delete(`/playlist/${id}`)
                .then(response => {
                    this.fetchPlaylists();
                })
                .catch(error => {
                    console.error('Error deleting playlist:', error);
                });
        },
        fetchPlaylists() {
            axiosClient.get('/playlists')
                .then(response => {
                    this.playlists = response.data;
                })
                .catch(error => {
                    console.error('Error fetching playlists:', error);
                });
        }
    }
}
</script>

<style>

</style>
