<template>
    <div>
        <NavUser />
        <div class="container py-5">
            <div v-if="artist" class="">
                <h2 class="mb-4 lead display-4">{{ artist.name }}</h2>
            </div>
            <table class="table table-hover text-center">
                <thead>
                    <tr class="table-active">
                        <th class="lead" scope="col">Name</th>
                        <th class="lead" scope="col">Genre</th>
                        <th class="lead" scope="col">Rating</th>
                        <th class="lead" scope="col">Released</th>
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
                        <td class="text-body">{{ track.rating }}</td>
                        <td class="text-body">{{ track.release_date.slice(0,10) }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import NavUser from '@/components/NavUser.vue';
import axiosClient from '@/axios';
import { mapActions } from 'vuex';

export default {
    components: {
        NavUser
    },
    data() {
        return {
            artist: null,
            tracks: []
        };
    },
    mounted() {
        this.fetchArtistAndTracks();
    },
    methods: {
        ...mapActions(['selectTrack']),
        fetchArtistAndTracks() {
            const artistId = this.$route.params.id;
            axiosClient.get(`/artist/${artistId}`)
                .then(response => {
                    this.artist = response.data;
                    this.tracks = this.artist.tracks;
                })
                .catch(error => {
                    console.error('Failed to fetch artist:', error);
                });
        }
    }
};
</script>

<style>
</style>



