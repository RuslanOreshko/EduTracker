<script setup>
defineProps({
  modelValue: { type: [String, Number], default: "" },
  placeholder: { type: String, default: "" },
  type: { type: String, default: "" },
  disable: { type: Boolean, default: false },
});

defineEmits(["update:modelValue"]);
</script>

<template>
  <input
    class="input"
    :type="type"
    :placeholder="placeholder"
    :value="modelValue"
    @input="$emit('update:modelValue', $event.target.value)"
  />
</template>

<style scoped>
.input {
  width: 100%;
  border-radius: 12px;
  padding: 10px 12px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #e6e9ef;
  outline: none;
}

.input::placeholder {
  color: rgba(230, 233, 239, 0.45);
}

.input:focus {
  border-color: rgba(255, 255, 255, 0.22);
}
</style>
