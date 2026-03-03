<script setup>
import { computed, nextTick, ref, watch } from "vue";
import Input from "./Input.vue";
import Skeleton from "./Skeleton.vue";

const props = defineProps({
  modelValue: { type: String, default: "" },
  items: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  open: { type: Boolean, default: false },
  placeholder: { type: String, default: "Введи викладача..." },
});

const emit = defineEmits([
  "update:modelValue",
  "select",
  "open",
  "close",
  "enter",
]);

const activeIdx = ref(-1);

watch(
  () => props.items,
  () => {
    activeIdx.value = props.items.length ? 0 : -1;
  },
);

function onInput(v) {
  emit("update:modelValue", v);
  emit("open");
}

function onKeydown(e) {
  if (!props.open) {
    if (e.key === "ArrowDown") emit("open");
    return;
  }

  if (e.key === "Escape") {
    emit("close");
    return;
  }

  if (e.key === "ArrowDown") {
    e.preventDefault();
    if (!props.items.length) return;
    activeIdx.value = Math.min(activeIdx.value + 1, props.items.length - 1);
    return;
  }

  if (e.key === "ArrowUp") {
    e.preventDefault();
    if (!props.items.length) return;
    activeIdx.value = Math.max(activeIdx.value - 1, 0);
    return;
  }

  if (e.key === "Enter") {
    if (props.items.length && activeIdx.value >= 0) {
      const it = props.items[activeIdx.value];
      if (it?.display_name) emit("select", it.display_name);
      emit("close");
      return;
    }

    emit("enter");
  }
}

function onBlur() {
  setTimeout(() => emit("close"), 120);
}

function pick(name) {
  emit("select", name);
  emit("close");
}
</script>

<template>
  <div class="wrap">
    <Input
      :model-value="modelValue"
      :placeholder="placeholder"
      @update:modelValue="onInput"
      @keydown="onKeydown"
      @focus="emit('open')"
      @blur="onBlur"
    />

    <div v-if="open" class="drop">
      <div v-if="loading" class="loading">
        <Skeleton height="12px" width="70%" />
        <Skeleton height="12px" width="55%" />
        <Skeleton height="12px" width="62%" />
      </div>

      <template v-else>
        <button
          v-for="(it, idx) in items"
          :key="it.display_name + idx"
          class="item"
          :data-active="idx === activeIdx"
          type="button"
          @mousedown.prevent="pick(it.display_name)"
        >
          {{ it.display_name }}
        </button>

        <div v-if="!items.length" class="empty">Нічого не знайдено</div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.wrap {
  position: relative;
}

.drop {
  position: absolute;
  z-index: 50;
  top: calc(100% + 8px);
  left: 0;
  right: 0;

  border-radius: 14px;
  background: #111318;
  border: 1px solid rgba(255, 255, 255, 0.1);
  overflow: hidden;
  box-shadow: 0 18px 50px rgba(0, 0, 0, 0.55);
}

.loading {
  padding: 12px 12px;
  display: grid;
  gap: 10px;
}

.item {
  width: 100%;
  text-align: left;
  padding: 10px 12px;
  border: 0;
  background: transparent;
  color: rgba(230, 233, 239, 0.92);
  cursor: pointer;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.item:hover,
.item[data-active="true"] {
  background: rgba(255, 255, 255, 0.06);
}

.empty {
  padding: 10px 12px;
  opacity: 0.7;
  font-size: 13px;
}
</style>
