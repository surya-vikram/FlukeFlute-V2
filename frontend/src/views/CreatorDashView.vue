<template>
    <div>
        <NavCreator />
        <div>
            <div class="container py-5">
                <h2 class="mb-4 lead display-4">Albums</h2>
                <div class="row row-cols-lg-2" v-if="albums.length">
                    <div class="col-lg-3 col-md-4 col-6 mb-4 mt-1" v-for="album in albums" :key="album.id">
                        <div class="card">
                            <img :src="'data:image/png;base64,' + album.cover" class="card-img-top custom-img">
                            <div class="card-body custom-card-body d-flex align-items-center justify-content-start">
                                <h5 class="card-title .text-light-emphasis lead">{{ album.title }}</h5>
                                <div class="ms-auto">
                                    <router-link :to="{ name: 'UpdateAlbumView', params: { id: album.id } }"
                                        class="btn btn-info me-2" style="text-decoration: none;">Update</router-link>
                                    <button class="btn btn-danger" @click="deleteAlbum(album.id)">Delete</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <p class="display-4 lead" v-else>Content not available</p>
            </div>
        </div>
    </div>
</template>

<script>
import axiosClient from '@/axios';
import NavCreator from '@/components/NavCreator.vue'
export default {
    components: {
        NavCreator,
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
            axiosClient.get('/creator/albums')
                .then(response => {
                    this.albums = response.data;
                })
                .catch(error => {
                    console.error('Failed to fetch albums:', error);
                });
        },
        deleteAlbum(albumId) {
            axiosClient.delete(`/album/${albumId}`)
                .then(response => {
                    this.fetchAlbums();
                })
                .catch(error => {
                    console.error('Error deleting album:', error);
                });
        }
    }
}
</script>

<style></style>

