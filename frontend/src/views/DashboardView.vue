<script setup>
import TopTeachersCard from "../components/dashboard/TopTeachersCard.vue";
import StatsTeacherCard from "../components/dashboard/StatsTeacherCard.vue";
import CompareTeachersCard from "../components/dashboard/CompareTeachersCard.vue";
import AvgPerWorkdayCard from "../components/dashboard/AvgPerWorkdayCard.vue";
</script>

<template>
  <div class="grid">
    <TopTeachersCard />
    <StatsTeacherCard />

    <CompareTeachersCard class="span2" />
    <div class="full">
      <AvgPerWorkdayCard />
    </div>
  </div>
</template>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 520px));
  gap: 18px;
  align-items: start;
  justify-content: center;
}

.grid > * {
  min-width: 0;
}

.full {
  grid-column: 1 / -1;
}

.span2 {
  grid-column: 1 / -1;
}

@media (max-width: 1100px) {
  .grid {
    grid-template-columns: 1fr;
  }
  .full {
    grid-column: auto;
  }
}
</style>
