<script setup>
import { useAuthStore } from "../stores/auth";
import { getTopTeachers } from "../api/teachers.api";

const auth = useAuthStore();
const res = await getTopTeachers({ limit: 5 });
console.log(res.data);
</script>

<template>
  <h1>Dashboard</h1>
  <p>Logged in: {{ auth.isAuthenticated }}</p>
</template>
