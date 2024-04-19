<template>
    <nav class="navbar navbar-expand-lg bg-primary" data-bs-theme="dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">FlukeFlute</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarColor01"
                aria-controls="navbarColor01" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <!-- Left-aligned section -->
            <div class="collapse navbar-collapse" id="navbarColor01">
                <ul class="navbar-nav me-auto">
                    <!-- Navigation links -->
                    <li class="nav-item">
                        <router-link class="nav-link" to="/user/dashboard">Albums</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/artists">Artists</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/tracks">Tracks</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/playlists">Playlists</router-link>
                    </li>
                    <!-- Filter dropdown -->
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" role="button"
                            aria-haspopup="true" aria-expanded="false">Filter</a>
                        <div class="dropdown-menu">
                            <router-link :to="{ name: 'FilterTracksView', params: { id: 3 } }" style="text-decoration: none;" class="dropdown-item"> Latest </router-link>
                            <div class="dropdown-divider"></div>
                            <router-link :to="{ name: 'FilterTracksView', params: { id: 2 } }" style="text-decoration: none;" class="dropdown-item"> Trending </router-link>
                            <div class="dropdown-divider"></div>
                            <router-link :to="{ name: 'FilterTracksView', params: { id: 1 } }" style="text-decoration: none;" class="dropdown-item"> Top-Rated </router-link>
                        </div>
                    </li>
                </ul>
            </div>

            <!-- Right-aligned section -->
            <div class="d-flex">
                <!-- Search form -->
                <form class="d-flex me-2" @submit.prevent="showSearchResults">
                    <input class="form-control me-sm-2" type="search" placeholder="Search" v-model="searchQuery">
                    <button class="btn btn-secondary my-2 my-sm-0" type="submit">Search</button>
                </form>
                <!-- User actions -->
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <router-link class="nav-link" :to="isCreator ? '/creator/dashboard' : '/register/creator'">Creator</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/profile">Profile</router-link>
                    </li>
                    <li class="nav-item">
                        <LogoutModal />
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<script>
import LogoutModal from '@/components/LogoutModal.vue';

export default {
    data() {
        return {
            searchQuery: ''
        }
    },
    computed: {
        isCreator() {
            return this.$store.state.roles.includes('Creator');
        }
    },
    components: {
        LogoutModal
    },
    methods: {
        showSearchResults() {
            this.$store.commit('addSearchQuery', this.searchQuery);
            this.searchQuery = '';
            this.$emit('search');
        }
    }
};
</script>

<style>

</style>
