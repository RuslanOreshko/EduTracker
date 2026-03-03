<script setup>
import Input from "./Input.vue";
import Button from "./Button.vue";

const props = defineProps({
  from: { type: String, default: "" },
  to: { type: String, default: "" },
  activePresset: { type: String, default: "" },
});

const emit = defineEmits(["update:from", "update:to", "reset", "preset"]);
</script>

<template>
  <div class="wrap">
    <div class="row">
      <div class="field">
        <div class="label">From</div>
        <Input
          type="date"
          :model-value="from"
          @update:modelValue="(v) => emit('update:from', v)"
        />
      </div>

      <div class="field">
        <div class="label">To</div>
        <Input
          type="date"
          :modelValue="to"
          @update:modelValue="(v) => emit('update:to', v)"
        />
      </div>
    </div>

    <div class="presets">
      <Button
        variant="ghost"
        :data-active="activePresset === 'academic'"
        @click="emit('preset', 'academic')"
        >Academic year</Button
      >
      <Button
        variant="ghost"
        :data-active="activePresset === '30d'"
        @click="emit('preset', '30d')"
        >Last 30 days</Button
      >
      <Button variant="ghost" @click="emit('reset')">Reset</Button>
    </div>
  </div>
</template>

<style scoped>
.wrap {
  display: grid;
  gap: 10px;
}

.row {
  display: grid;
  grid-template-columns: 1fr 1fr auto;
  gap: 10px;
  align-items: end;
}

.field .label {
  font-size: 12px;
  opacity: 0.65;
  margin-bottom: 6px;
}

.presets {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.active {
  background: rgba(255, 255, 255, 0.12) !important;
  border-color: rgba(255, 255, 255, 0.22) !important;
}

@media (max-width: 520px) {
  .row {
    grid-template-columns: 1fr;
  }
  .apply {
    width: 100%;
  }
}
</style>
