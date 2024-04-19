<template>
    <div>
        <NavUser @search="handleSearch" />
        <div class="container py-5">
            <h2 class="mb-4 lead display-4">Tracks</h2>
            <table class="table table-hover text-center">
                <thead>
                    <tr class="table-active">
                        <th class="lead" scope="col">Name</th>
                        <th class="lead" scope="col">Genre</th>
                        <th class="lead" scope="col">Language</th>
                        <th class="lead" scope="col">Rating</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="track in tracks" :key="track.id" class="table-dark">
                        <td class="text-light" scope="row">
                            <router-link :to="{ name: 'TrackView', params: { id: track.id } }"
                                @click.native="selectTrack(track)">
                                {{ track.title }}
                            </router-link>
                        </td>
                        <td class="text-body">{{ track.genre }}</td>
                        <td class="text-body">{{ track.language }}</td>
                        <td class="text-body">{{ track.rating }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import NavUser from '@/components/NavUser.vue'
import axiosClient from '@/axios';
import { mapActions } from 'vuex';

export default {
    components: {
        NavUser
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
        ...mapActions(['selectTrack']),
        fetchTracks() {
            axiosClient.get('/tracks')
                .then(response => {
                    this.tracks = response.data;
                })
                .catch(error => {
                    console.error('Failed to fetch tracks:', error);
                });
        },
        handleSearch(){
            const searchQuery = this.$store.state.searchQuery
            // this.$store.commit('removeSearchQuery')
            axiosClient.get(`/search/${searchQuery}`)
            .then(response => {
                this.tracks = response.data.tracks
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
