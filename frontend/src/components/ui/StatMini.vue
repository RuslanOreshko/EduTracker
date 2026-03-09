<script setup>
defineProps({
  label: { type: String, default: "" },
  value: { type: [String, Number], default: "-" },
  hint: { type: String, default: "" },
});
</script>

<template>
  <div class="mini">
    <div class="mini__value">{{ value }}</div>
    <div class="mini__label">{{ label }}</div>
    <div class="mini__hint" v-if="hint">{{ hint }}</div>
  </div>
</template>

<style scoped>
.mini {
  padding: 10px 12px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.mini__value {
  font-weight: 900;
  font-size: 18px;
  line-height: 1.1;
  color: rgba(230, 233, 239, 0.9); /* НЕ сліпучий білий */
}

.mini__label {
  margin-top: 6px;
  font-size: 11px;
  opacity: 0.62;
}

.mini__hint {
  margin-top: 6px;
  font-size: 11px;
  opacity: 0.55;
}
</style>
