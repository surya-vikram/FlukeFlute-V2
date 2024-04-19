<template>
    <div>
        <NavUser />
        <div class="container py-5">
            <h2 class="mb-4 lead display-4">{{ pageTitle }}</h2>
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
import NavUser from '@/components/NavUser.vue';
import axiosClient from '@/axios';
import { mapActions } from 'vuex';

export default {
    components: {
        NavUser
    },
    data() {
        return {
            id: null,
            tracks: []
        };
    },
    computed: {
        pageTitle() {
            if (this.id === '1') {
                return 'Top-Rated Tracks';
            } else if (this.id === '2') {
                return 'Trending Tracks';
            } else {
                return 'Latest Tracks';
            }
        }
    },
    methods: {
        ...mapActions(['selectTrack']),
        fetchTracks() {
            axiosClient.get(`/filter/${this.id}`)
                .then(response => {
                    this.tracks = response.data;
                })
                .catch(error => {
                    console.error('Failed to fetch tracks:', error);
                });
        },
    },
    beforeRouteUpdate(to, from, next) {
        
        if (to.params.id !== this.id) {
            this.id = to.params.id;
            this.fetchTracks();
        }
        next(); 
    },
    mounted() {
    
        this.id = this.$route.params.id;
        this.fetchTracks();
    },
};
</script>
