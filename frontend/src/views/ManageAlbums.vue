<template>
    <div>
        <NavAdmin />
        <div class="container py-5">
            <h2 class="mb-4 lead display-4">Albums</h2>
            <table class="table table-hover text-center">
                <thead>
                    <tr class="table-active">
                        <th class="lead" scope="col">Title</th>
                        <th class="lead" scope="col">Release Year</th>
                        <th class="lead" scope="col">Delete</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="album in albums" :key="album.id" class="table-dark">
                        <td class="text-light align-middle" scope="row">
                            {{ album.title }}
                        </td>
                        <td class="text-body align-middle">{{ album.date_created.slice(0,4) }}</td>
                        <td><button class="btn btn-danger" @click="deleteAlbum(album.id)">Remove</button></td>
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
            albums: []
        };
    },
    mounted() {
        this.fetchAlbums();
    },
    methods: {
        fetchAlbums() {
            axiosClient.get('/all_albums')
                .then(response => {
                    this.albums = response.data;
                })
                .catch(error => {
                    console.error('Failed to fetch albums:', error);
                });
        },
        deleteAlbum(albumId) {
            axiosClient.delete(`/remove_album/${albumId}`)
                .then(response => {
                    this.fetchAlbums();
                })
                .catch(error => {
                    console.error('Error deleting album:', error);
                });
        }
    }
};
</script>

<style></style>
