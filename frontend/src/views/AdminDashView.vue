<template>
    <div>
        <NavAdmin/>
        <div class="container px-5 py-3">
            <div class="row mt-5">
                <div class="col-md-6">
                    <h2>Total Users: {{ users }}</h2>
                    <h2>Total Creators: {{ creators }}</h2>
                </div>
                <div class="col-md-6">
                    <img :src="usersCreatorsChart" class="img-fluid" alt="Users/Creators Chart">
                </div>
            </div>
            <div class="row mt-5">
                <div class="col-md-6">
                    <h2>Genres Distribution</h2>
                </div>
                <div class="col-md-6">
                    <img :src="genresChart" class="img-fluid" alt="Genres Chart">
                </div>
            </div>
            <div class="row mt-5">
                <div class="col-md-6">
                    <h2>Languages Distribution</h2>
                </div>
                <div class="col-md-6">
                    <img :src="languagesChart" class="img-fluid" alt="Languages Chart">
                </div>
            </div>
            <div class="row mt-5">
                <div class="col-md-6">
                    <h2>Albums : {{ albums }}</h2>
                    <h2>Tracks : {{ tracks }}</h2>
                    <h2>Playlists : {{ playlists }}</h2>
                </div>
                <div class="col-md-6">
                    <img :src="statsChart" class="img-fluid" alt="Stats Chart">
                </div>
            </div>
            <div class="row mt-5">
                <div class="col-md-6">
                    <h2>Tracks Performance</h2>
                </div>
                <div class="col-md-6">
                    <img :src="ratingsChart" class="img-fluid" alt="Ratings Chart">
                </div>
            </div>
            <div class="row mt-5">
                <div class="col-md-6">
                    <h2>Users Activity</h2>
                </div>
                <div class="col-md-6">
                    <img :src="activityChart" class="img-fluid" alt="Activity Chart">
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axiosClient from '@/axios';
import NavAdmin from '@/components/NavAdmin.vue';

export default {
    components: {
        NavAdmin
    },
    data() {
        return {
            users: 0,
            creators: 0,
            albums: 0,
            tracks: 0,
            playlists: 0,
            usersCreatorsChart: null,
            genresChart: null,
            languagesChart: null,
            statsChart: null,
            ratingsChart: null,
            activityChart: null
        };
    },
    mounted() {
        this.fetchAdminPlots();
    },
    methods: {
        fetchAdminPlots() {
            axiosClient.get('/stats')
                .then(response => {
                    const { data } = response;
                    this.users = data.users;
                    this.creators = data.creators;
                    this.albums = data.albums;
                    this.tracks = data.tracks;
                    this.playlists = data.playlists;
                    this.usersCreatorsChart = `data:image/png;base64,${data.usersCreatorsChart}`;
                    this.genresChart = `data:image/png;base64,${data.genresChart}`;
                    this.languagesChart = `data:image/png;base64,${data.languagesChart}`;
                    this.statsChart = `data:image/png;base64,${data.statsChart}`;
                    this.ratingsChart = `data:image/png;base64,${data.ratingsChart}`;
                    this.activityChart = `data:image/png;base64,${data.appActivity}`;
                })
                .catch(error => {
                    console.error('Error fetching admin plots:', error);
                });
        }
    }
};
</script>

<style>
</style>
