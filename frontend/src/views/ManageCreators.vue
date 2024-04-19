<template>
    <div>
        <NavAdmin />
        <div class="container py-5">
            <h2 class="mb-4 lead display-4">Creators</h2>
            <table class="table table-hover text-center">
                <thead>
                    <tr class="table-active">
                        <th class="lead" scope="col">Name</th>
                        <th class="lead" scope="col">Popularity</th>
                        <th class="lead" scope="col">Flag/Unflag</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="creator in creators" :key="creator.id" class="table-dark">
                        <td class="text-light align-middle">{{ creator.name }}</td>
                        <td class="text-light align-middle">{{ creator.popularity }}</td>
                        <td>
                            <button @click="toggleFlag(creator.id)" class="btn"
                                :class="creator.is_flagged ? 'btn-success' : 'btn-danger'">
                                {{ creator.is_flagged ? 'Unflag' : 'Flag' }}
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import axiosClient from '@/axios'; 
import NavAdmin from '@/components/NavAdmin.vue'

export default {
    components: {
        NavAdmin
    },
    data() {
        return {
            creators: []
        };
    },
    mounted() {
        this.fetchCreators();
    },
    methods: {
        fetchCreators() {
            axiosClient.get('/creators')
                .then(response => {
                    this.creators = response.data;
                })
                .catch(error => {
                    console.error('Error fetching creators:', error);
                });
        },
        toggleFlag(creatorId) {
            axiosClient.put(`/flag/${creatorId}`)
                .then(response => {
                    this.fetchCreators();
                })
                .catch(error => {
                    console.error('Error toggling flag:', error);
                });
        }
    }
};
</script>

<style scoped>
</style>

