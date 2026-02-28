<script setup>
import TopTeachersCard from "../components/dashboard/TopTeachersCard.vue";
</script>

<template>
  <div class="grid">
    <TopTeachersCard />
  </div>
</template>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: 420px;
  gap: 18px;
}

@media (max-width: 900px) {
  .grid {
    grid-template-columns: 1fr;
  }
}
</style>
