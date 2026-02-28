<script setup>
defineProps({
  title: { type: String, default: "Помилка" },
});
</script>

<template>
  <div class="alert">
    <div class="alert__title">{{ title }}</div>
    <div class="alert__body"><slot /></div>
  </div>
</template>

<style scoped>
.alert {
  padding: 12px 12px;
  border-radius: 14px;
  background: rgba(255, 77, 77, 0.08);
  border: 1px solid rgba(255, 77, 77, 0.22);
  color: rgba(255, 200, 200, 0.95);
}

.alert__title {
  font-weight: 700;
  margin-bottom: 6px;
}

.alert__body {
  opacity: 0.95;
}
</style>
