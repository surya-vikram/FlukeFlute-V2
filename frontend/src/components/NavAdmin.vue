<template>
  <nav class="navbar navbar-expand-lg bg-primary" data-bs-theme="dark">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">FlukeFlute</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarColor01"
        aria-controls="navbarColor01" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarColor01">
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/admin/dashboard">Dashboard</router-link>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" role="button" aria-haspopup="true"
              aria-expanded="false">Manage</a>
            <div class="dropdown-menu">
              <router-link class="dropdown-item" to="/manage/tracks">Tracks</router-link>
              <div class="dropdown-divider"></div>
              <router-link class="dropdown-item" to="/manage/albums">Albums</router-link>
              <div class="dropdown-divider"></div>
              <router-link class="dropdown-item" to="/manage/creators">Creators</router-link>
            </div>
          </li>
        </ul>
        <ul class="navbar-nav ms-auto">
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
  components: {
    LogoutModal
  }
};
</script>

<style>

</style>