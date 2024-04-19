<template>
    <div>
        <NavUser/>
        <div v-if="current_user" class="container text-light mt-5">
            <div v-if="current_user.pfp" class="rounded-circle overflow-hidden pfp mb-4">
                <img :src="'data:image/png;base64,' + current_user.pfp" class="w-100 h-100 object-fit-cover pfp">
            </div>
            <p>Name: {{ current_user.name }}</p>
            <p>Username: {{ current_user.username }}</p>
            <p>Email: {{ current_user.email }}</p>
            <p v-if="current_user.stage_name">Stage Name: {{ current_user.stage_name }}</p>
            <p v-if="current_user.bio">Bio: {{ current_user.bio }}</p>
            <p v-if="current_user.visits">Days Visited: {{ current_user.visits }}</p>
            <p v-if="current_user.tracks">Number of Tracks: {{ current_user.tracks }}</p>
            <p v-if="current_user.albums">Number of Albums: {{ current_user.albums }}</p>
            <p v-if="current_user.playlists">Number of Playlists: {{ current_user.playlists }}</p>
        </div>
    </div>
</template>

<script>
import axiosClient from '@/axios';
import NavUser from '@/components/NavUser.vue';
export default {
    components: {
        NavUser
    },
    data() {
        return {
            current_user: null
        };
    },
    mounted() {
        this.fetchProfile();
    },
    methods: {
        fetchProfile(){
                axiosClient.get('/user')
                .then(response => {
                    this.current_user = response.data;
                })
                .catch(error => {
                    console.error('Error fetching user data:', error);
                });
        }
    }
};
</script>

<style>
</style>
