<template>
    <div class="form-container d-flex align-items-center" style="height: 100vh;">
        <div class="col-6 mx-auto">
            <FlashMessage />
            <form autocomplete="off" novalidate @submit.prevent="uploadTrack">
                <fieldset>
                    <legend>New Track</legend>                   
                    <div>
                        <label for="title" class="form-label">Title</label>
                        <input type="text" class="form-control" id="title" v-model="title" required>
                    </div>                    
                    <div>
                        <label for="language" class="form-label mt-4">Language</label>
                        <select class="form-select" id="language" v-model="language">
                            <option v-for="language in languages" :key="language.id" :value="language.name">{{
                                language.name }}</option>
                        </select>
                    </div>
                    <div>
                        <label for="genre" class="form-label mt-4">Genre</label>
                        <select class="form-select" id="genre" v-model="genre">
                            <option v-for="genre in genres" :key="genre.id" :value="genre.name">{{ genre.name }}
                            </option>
                        </select>
                    </div>
                    <div>
                        <label for="formFile" class="form-label mt-4">Audio File</label>
                        <input class="form-control" type="file" id="formFile" @change="handleFileUpload">
                    </div>
                    <div>
                        <label for="lyrics" class="form-label mt-4">Lyrics</label>
                        <textarea class="form-control" id="lyrics" rows="3" v-model="lyrics"></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary mt-4">Submit</button>
                </fieldset>
            </form>
        </div>
    </div>
</template>

<script>
import axiosClient from '@/axios';
import FlashMessage from '@/components/FlashMessage.vue'
export default {
    components: {
        FlashMessage
    },
    data() {
        return {
            title: '',
            language: '',
            languages: this.$store.state.languages,
            genre: '',
            genres: this.$store.state.genres,
            file: '',
            lyrics: ''
        }
    },
    methods: {
        handleFileUpload(event) {
            const file = event.target.files[0];
            console.log(file)
            this.file = file;
        },
        uploadTrack() {
            const formData = new FormData();
            formData.append('title', this.title);
            formData.append('language', this.language);
            formData.append('genre', this.genre);
            formData.append('file', this.file);
            formData.append('lyrics', this.lyrics);
            console.log(formData)
            axiosClient
                .post('/tracks', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                })
                .then(response => {
                    const data = response.data;

                    this.$router.push({ name: 'CreatorDashView' });
                })
                .catch(error => {
                    const errorMessage = error?.response?.data?.message || 'Registration failed';
                    this.$store.commit('addMessage', errorMessage);
                    this.$store.commit('addCategory', 'danger');
                    console.error(error);
                });
        }
    }
}
</script>

<style>

</style>

