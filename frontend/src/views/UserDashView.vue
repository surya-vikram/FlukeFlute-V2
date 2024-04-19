<template>
    <div>
        <NavUser @search="handleSearch" />
        <div class="container py-5">
            <h2 class="mb-4 lead display-4">Albums</h2>
            <div class="row row-cols-lg-2" v-if="albums.length">
                <div class="col-lg-3 col-md-4 col-6 mb-4 mt-1" v-for="album in albums" :key="album.id">
                    <div class="card">
                        <router-link :to="{ name: 'AlbumView', params: { id: album.id } }"
                            style="text-decoration: none;">
                            <img :src="'data:image/png;base64,' + album.cover" class="card-img-top custom-img">
                            <div class="card-body custom-card-body d-flex align-items-center justify-content-start">
                                <h5 class="card-title .text-light-emphasis lead">{{ album.title }}</h5>
                            </div>
                        </router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import NavUser from '@/components/NavUser.vue'
import axiosClient from '@/axios';

export default {
    components: {
        NavUser
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
            axiosClient.get('/albums')
                .then(response => {
                    this.albums = response.data;
                })
                .catch(error => {
                    console.error('Failed to fetch albums:', error);
                });
        },
        handleSearch(){
            const searchQuery = this.$store.state.searchQuery
            // this.$store.commit('removeSearchQuery')
            axiosClient.get(`/search/${searchQuery}`)
            .then(response => {
                this.albums = response.data.albums
            })
            .catch(error => {
                console.error('Failed to get search results', error);
            });
        }
    }
};
</script>

<style>

</style>
