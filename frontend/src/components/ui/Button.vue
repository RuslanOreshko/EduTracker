<script setup>
defineProps({
  variant: { type: String, default: "primary" },
  type: { type: String, default: "button" },
  disabled: { type: Boolean, default: false },
});
</script>

<template>
  <button
    class="btn"
    :class="`btn--${variant}`"
    :type="type"
    :disabled="disabled"
  >
    <slot />
  </button>
</template>

<style scoped>
.btn {
  border-radius: 10px;
  padding: 9px 14px;
  font-weight: 600;
  cursor: pointer;
  border: 1px solid transparent;
  transition: 0.15s ease;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn--primary {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.12);
  color: #fff;
}

.btn--primary:hover:enabled {
  background: rgba(255, 255, 255, 0.14);
}

.btn--ghost {
  background: transparent;
  border-color: rgba(255, 255, 255, 0.12);
  color: rgba(230, 233, 239, 0.9);
}

.btn--ghost:hover:enabled {
  background: rgba(255, 255, 255, 0.06);
}
</style>
