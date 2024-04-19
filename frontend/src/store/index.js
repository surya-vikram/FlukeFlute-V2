import { createStore } from 'vuex';
import createPersistedState from 'vuex-persistedstate';
import axiosClient from '@/axios';

const store = createStore({
  state: {
    user_id: null,
    roles: null,
    orphanTracks: [],
    message: '',
    category: '',
    genres: [],
    languages: [],
    tracks: [],
    albums: [],
    artists: [],
    currentTrack: null, 
    searchQuery: null
  },

  mutations: {
    setCurrentTrack(state, track) {
      state.currentTrack = track;
    },
    setOrphanTracks(state, orphanTracks) {
      state.orphanTracks = orphanTracks;
    },
    removeOrphanTracks(state) {
      state.orphanTracks = []
    },
    setUserId(state, userId) {
      state.user_id = userId;
    },
    removeUserId(state) {
      state.user_id = null;
    },
    setUserRoles(state, roles) {
      state.roles = roles;
    },
    removeUserRoles(state) {
      state.roles = null;
    },
    addUserRole(state, role) {
      state.roles?.push(role);
    },
    setGenres(state, genres) {
      state.genres = genres;
    },
    setLanguages(state, languages) {
      state.languages = languages;
    },
    setTracks(state, tracks) {
      state.tracks = tracks;
    },
    setAlbums(state, albums) {
      state.albums = albums;
    },
    setArtists(state, artists) {
      state.artists = artists;
    },
    addMessage(state, message) {
      state.message = message;
    },
    addSearchQuery(state, searchQuery) {
      state.searchQuery = searchQuery;
    },
    removeSearchQuery(state) {
      state.searchQuery = null;
    },
    addCategory(state, category) {
      state.category = category;
    },
    clearMessage(state) {
      state.message = '';
      state.category = '';
    },
  },

  actions: {
    fetchOrphanTracks({ commit }) {
      axiosClient.get('/creator/orphan')
        .then(response => {
          commit('setOrphanTracks', response?.data)
        });  
    },
    fetchGenres({ commit }) {
      axiosClient.get('/genres')
        .then(response => {
          commit('setGenres', response?.data);
        })
        .catch(error => {
          console.error('Failed to fetch genres:', error);
        });
    },
    fetchLanguages({ commit }) {
      axiosClient.get('/languages')
        .then(response => {
          commit('setLanguages', response?.data);
        })
        .catch(error => {
          console.error('Failed to fetch languages:', error);
        });
    },
    fetchTracks({ commit }) {
      axiosClient.get('/tracks')
        .then(response => {
          commit('setTracks', response?.data);
        })
        .catch(error => {
          console.error('Failed to fetch tracks:', error);
        });
    },
    fetchAlbums({ commit }) {
      axiosClient.get('/albums')
        .then(response => {
          commit('setAlbums', response?.data);
        })
        .catch(error => {
          console.error('Failed to fetch albums:', error);
        });
    },
    fetchArtists({ commit }) {
      axiosClient.get('/artists')
        .then(response => {
          commit('setArtists', response?.data);
        })
        .catch(error => {
          console.error('Failed to fetch artists:', error);
        });
    },
    selectTrack({ commit }, track) {
      commit('setCurrentTrack', track);
    },
  },

  plugins: [createPersistedState()],
});

export default store;



