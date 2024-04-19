<template>
    <div v-if="hasMessage" class="alert alert-dismissible" :class="alertClass">
        <button type="button" class="btn-close" @click="clearMessage"></button>
        {{ $store.state.message }}
    </div>
</template>

<script>
export default {
    computed: {
        hasMessage() {
            return this.$store.state.message !== '';
        },
        alertClass() {
            return `alert alert-dismissible alert-${this.$store.state.category}`;
        }
    },
    methods: {
        clearMessage() {
            this.$store.commit('clearMessage');
        }
    }
};
</script>
