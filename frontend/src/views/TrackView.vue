<template>
    <div>
        <NavUser />
        <div class="container mt-5">
            <div class="row">
                <div class="col-md-8">
                    <h2>{{ currentTrack.title }}</h2><br>
                    <p>Artist: {{ currentTrack.creator }}</p>
                    <p>Genre: {{ currentTrack.genre }}</p>
                    <p>Language: {{ currentTrack.language }}</p>
                    <p>Date Released: {{ currentTrack.release_date }}</p>
                </div>
                <div class="col-md-4 text-md-right mt-5">
                    <p class="mt-4">Rating: {{ currentTrack.rating }}</p>
                    <div class="btn-group mt-2">
                        <button type="button" class="btn btn-primary dropdown-toggle" data-bs-toggle="dropdown"
                            aria-haspopup="true" aria-expanded="false">
                            Rate
                        </button>
                        <div class="dropdown-menu">
                            <a v-for="ratingValue in [1, 2, 3, 4, 5]" :key="ratingValue" class="dropdown-item"
                                @click="rateSong(ratingValue)">{{ ratingValue }}</a>
                        </div>
                    </div>
                </div>
            </div>

            <h3 class="mt-4 mb-3">Lyrics</h3>
            <pre class="mb-5 lead" style="height: 150px;">
      {{ currentTrack.lyrics || 'The artist has not uploaded any lyrics for the song' }}
        </pre>
            <audio controls class="w-100 mb-3">
                <source :src="'data:audio/mp3;base64,' + currentTrack.audio" type="audio/mp3">
            </audio>
        </div>
    </div>
</template>

<script>
import { mapState } from 'vuex';
import axiosClient from '@/axios';
import NavUser from '@/components/NavUser.vue'
export default {
    components: {
        NavUser
    },
    computed: {
        ...mapState(['currentTrack']),
    },

    methods: {
        rateSong(ratingValue) {
            axiosClient.post('/rate', {
                rating_value: ratingValue,
                track_id: this.currentTrack.id
            })
                .then(response => {
                    console.log('Rating successful:', response.data);
                    this.$router.push('/tracks')
                })
                .catch(error => {
                    console.error('Error rating song:', error);
                });
        }
    }
};

</script>

