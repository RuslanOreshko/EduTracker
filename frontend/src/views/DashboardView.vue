<script setup>
import TopTeachersCard from "../components/dashboard/TopTeachersCard.vue";
import StatsTeacherCard from "../components/dashboard/StatsTeacherCard.vue";
</script>

<template>
  <div class="grid">
    <TopTeachersCard />
    <StatsTeacherCard />
  </div>
</template>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: 520px 520px;
  gap: 18px;
  align-items: start;
}

@media (max-width: 1100px) {
  .grid {
    grid-template-columns: 1fr;
  }
}
</style>
