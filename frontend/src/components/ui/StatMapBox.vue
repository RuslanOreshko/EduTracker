<script setup>
import { computed, ref, watch } from "vue";
import Button from "./Button.vue";

const props = defineProps({
  title: { type: String, default: "" },
  map: { type: Object, default: null },
  step: { type: Number, default: 8 },
});

const emit = defineEmits(["pick"]);

const limit = ref(props.step);

watch(
  () => props.map,
  () => {
    limit.value = props.step;
  },
);

const sorted = computed(() => {
  const obj = props.map || {};
  return Object.entries(obj).sort((a, b) => Number(b[1]) - Number(a[1]));
});

const visible = computed(() => sorted.value.slice(0, limit.value));
const totalCount = computed(() => sorted.value.length);

function showMore() {
  limit.value += props.step;
}

function onPick(name) {
  if (typeof name !== "string") return;
  emit("pick", name);
}
</script>

<template>
  <div class="box">
    <div class="boxTitle">{{ title }}</div>

    <div class="rows">
      <button
        class="r_btn"
        v-for="[k, v] in visible"
        :key="k"
        type="button"
        @click="onPick(k)"
        :title="`Фільтр: ${k}`"
      >
        <div class="k">{{ k }}</div>
        <div class="v">{{ v }}</div>
      </button>

      <Button v-if="totalCount > limit" variant="ghost" @click="showMore">
        Show more
      </Button>
    </div>
  </div>
</template>

<style scoped>
.box {
  padding: 12px 12px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.boxTitle {
  font-weight: 800;
  font-size: 12px;
  opacity: 0.8;
  margin-bottom: 10px;
}

.rows {
  display: grid;
  gap: 8px;
}

.r_btn {
  all: unset;
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 10px;
  align-items: center;

  padding: 8px 10px;
  border-radius: 12px;

  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);

  cursor: pointer;
}

.r_btn:hover {
  background: rgba(255, 255, 255, 0.06);
}

.k {
  font-weight: 700;
  font-size: 13px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.v {
  font-weight: 900;
  font-size: 13px;
  opacity: 0.95;
}
</style>
