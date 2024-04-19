<template>
    <div>
        <NavUser @search="handleSearch" />
        <div class="container py-5">
            <h2 class="mb-4 lead display-4">Artists</h2>
            <div class="row row-cols-lg-2" v-if="artists.length">
                <div class="col-lg-3 col-md-4 col-6 mb-4 mt-1" v-for="artist in artists" :key="artist.id">
                    <div class="card">
                        <router-link :to="{ name: 'ArtistView', params: { id: artist.id } }"
                            style="text-decoration: none;">
                            <img :src="'data:image/png;base64,' + artist.pfp" class="card-img-top custom-img">
                            <div class="card-body custom-card-body d-flex align-items-center justify-content-start">
                                <h5 class="card-title .text-light-emphasis lead">{{ artist.name }}</h5>
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
            artists: []
        };
    },
    mounted() {
        this.fetchArtists();
    },
    methods: {
        fetchArtists() {
            axiosClient.get('/artists')
                .then(response => {
                    this.artists = response.data;
                })
                .catch(error => {
                    console.error('Failed to fetch artists:', error);
                });
        },
        handleSearch(){
            const searchQuery = this.$store.state.searchQuery
            // this.$store.commit('removeSearchQuery')
            axiosClient.get(`/search/${searchQuery}`)
            .then(response => {
                this.artists = response.data.artists
            })
            .catch(error => {
                console.error('Failed to get search results', error);
            });
        }
    }
};
</script>

<style></style>
