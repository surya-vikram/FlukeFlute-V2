<template>
    <div>
        <NavUser />
        <div class="container py-5">
            <h2 class="mb-4 lead display-4" v-if="playlist">{{ playlist?.name }}</h2>

            <table class="table table-hover text-center" v-if="tracks?.length">
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
                        <td class="text-body">{{ track.release_date }}</td>
                    </tr>
                </tbody>
            </table>

            <p v-else-if="!playlist">Loading playlist...</p>
            <p v-else>No tracks available for this playlist.</p>
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
            playlist: null,
            tracks: []
        };
    },
    mounted() {
        this.fetchPlaylistTracks();
    },
    methods: {
        ...mapActions(['selectTrack']),
        fetchPlaylistTracks() {
            const playlistId = this.$route.params.id;
            axiosClient.get(`/playlist/${playlistId}`)
                .then(response => {
                    this.playlist = response.data;
                    this.tracks = this.playlist.tracks;
                })
                .catch(error => {
                    console.error('Failed to fetch playlist tracks:', error);
                });
        }
    }
};
</script>

<style>
</style>

