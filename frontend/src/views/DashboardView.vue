<script setup>
import { useAuthStore } from "../stores/auth";
const auth = useAuthStore();
</script>

<template>
  <h1>Dashboard</h1>
  <p>Logged in: {{ auth.isAuthenticated }}</p>
</template>
