<script setup>
defineProps({
  height: { type: String, default: "14px" },
  width: { type: String, default: "100%" },
  radius: { type: String, default: "10px" },
});
</script>

<template>
  <div class="sk" :style="{ height, width, borderRadius: radius }"></div>
</template>

<style scoped>
.sk {
  background: rgba(255, 255, 255, 0.06);
  position: relative;
  overflow: hidden;
}

.sk::after {
  content: "";
  position: absolute;
  inset: 0;
  transform: translateX(-100%);
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.08),
    transparent
  );
  animation: shimmer 1.1s infinite;
}

@keyframes shimmer {
  100% {
    transform: translateX(100%);
  }
}
</style>
