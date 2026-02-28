<script setup>
import { useAuthStore } from "../stores/auth";
import { useRouter } from "vue-router";

const auth = useAuthStore();
const router = useRouter();

async function logout() {
  await auth.logout();
  router.push("/login");
}
</script>

<template>
  <div class="app">
    <header class="header">
      <div class="header__inner">
        <div class="brand">EduTracker</div>

        <button class="btn" @click="logout">Logout</button>
      </div>
    </header>
    <main class="main">
      <div class="container">
        <router-view />
      </div>
    </main>
  </div>
</template>

<style scoped>
.app {
  min-height: 100hv;
  background: #0f1115;
  color: #e6e9ef;
  display: flex;
  flex-direction: column;
}

.header {
  height: 64px;
  width: 100%;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  background: #111318;
}

.header__inner {
  height: 64px;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;

  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand {
  font-weight: 700;
  font-size: 16px;
}

.main {
  flex: 1;
  padding: 32px 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.btn {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #fff;
  padding: 8px 14px;
  border-radius: 8px;
  cursor: pointer;
}

.btn:hover {
  background: rgba(255, 255, 255, 0.12);
}
</style>
