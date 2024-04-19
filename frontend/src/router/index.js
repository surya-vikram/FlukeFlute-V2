import { createRouter, createWebHistory } from 'vue-router'
import WelcomeView from '@/views/WelcomeView.vue'
import AdminLoginView from '@/views/AdminLoginView.vue'
import UserLoginView from '@/views/UserLoginView.vue'
import UserRegisterView from '@/views/UserRegisterView.vue'
import CreatorRegisterView from '@/views/CreatorRegisterView.vue'
import CreatorDashView from '@/views/CreatorDashView.vue'
import CreatorTracksView from '@/views/CreatorTracksView.vue'
import UserDashView from '@/views/UserDashView.vue' 
import AdminDashView from '@/views/AdminDashView.vue'
import NewTrackView from '@/views/NewTrackView.vue' 
import AlbumView from '@/views/AlbumView.vue' 
import NewAlbumView from '@/views/NewAlbumView.vue' 
import ArtistsView from '@/views/ArtistsView.vue'
import ArtistView from '@/views/ArtistView.vue'
import TracksView from '@/views/TracksView.vue'
import TrackView from '@/views/TrackView.vue'
import ProfileView from '@/views/ProfileView.vue'
import ManageCreators from '@/views/ManageCreators.vue'
import ManageTracks from '@/views/ManageTracks.vue'
import ManageAlbums from '@/views/ManageAlbums.vue'
import UpdateTrackView from '@/views/UpdateTrackView'
import UpdateAlbumView from '@/views/UpdateAlbumView'
import UpdatePlaylistView from '@/views/UpdatePlaylistView'
import UserPlaylistsView from '@/views/UserPlaylistsView.vue'
import UserPlaylistView from '@/views/UserPlaylistView.vue'
import NewPlaylistView from '@/views/NewPlaylistView.vue'
import FilterTracksView from '@/views/FilterTracksView.vue'

const routes = [
  { path: '/', name: 'WelcomeView', component: WelcomeView },
  { path: '/login/admin', name: 'AdminLoginView', component: AdminLoginView },
  { path: '/login/user', name: 'UserLoginView', component: UserLoginView },
  { path: '/register/user', name: 'UserRegisterView', component: UserRegisterView },
  { path: '/register/creator', name: 'CreatorRegisterView', component: CreatorRegisterView },
  { path: '/user/dashboard', name: 'UserDashView', component: UserDashView },
  { path: '/creator/dashboard', name: 'CreatorDashView', component: CreatorDashView },
  { path: '/creator/tracks', name: 'CreatorTracksView', component: CreatorTracksView },
  { path: '/admin/dashboard', name: 'AdminDashView', component: AdminDashView },
  { path: '/creator/new_track', name: 'NewTrackView', component: NewTrackView },
  { path: '/creator/new_album', name: 'NewAlbumView', component: NewAlbumView },
  { path: '/new_playlist', name: 'NewPlaylistView', component: NewPlaylistView },
  { path: '/album/:id', name: 'AlbumView', component: AlbumView, props: true },
  { path: '/filter_tracks/:id', name: 'FilterTracksView', component: FilterTracksView, props: true },
  { path: '/artists', name: 'ArtistsView', component: ArtistsView },
  { path: '/artist/:id', name: 'ArtistView', component: ArtistView, props: true },
  { path: '/tracks', name: 'TracksView', component: TracksView },
  { path: '/track/:id', name: 'TrackView', component: TrackView, props: true },
  { path: '/profile', name: 'ProfileView', component: ProfileView },
  { path: '/manage/creators', name: 'ManageCreators', component: ManageCreators },
  { path: '/manage/tracks', name: 'ManageTracks', component: ManageTracks },
  { path: '/manage/albums', name: 'ManageAlbums', component: ManageAlbums },
  { path: '/update/album/:id', name: 'UpdateAlbumView', component: UpdateAlbumView, props: true },
  { path: '/update/track/:id', name: 'UpdateTrackView', component: UpdateTrackView, props: true },
  { path: '/update/playlist/:id', name: 'UpdatePlaylistView', component: UpdatePlaylistView, props: true },
  { path: '/playlists', name: 'UserPlaylistsView', component: UserPlaylistsView },
  { path: '/playlist/:id', name: 'UserPlaylistView', component: UserPlaylistView, props: true },
  
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router

