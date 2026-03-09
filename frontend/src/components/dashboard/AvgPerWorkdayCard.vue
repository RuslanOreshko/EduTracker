<script setup>
import { ref, watch, computed } from "vue";

import Card from "../ui/Card.vue";
import Button from "../ui/Button.vue";
import Alert from "../ui/Alert.vue";
import Skeleton from "../ui/Skeleton.vue";
import DateRange from "../ui/DateRange.vue";
import TeacherAutocomplete from "../ui/TeacherAutocomplete.vue";
import StatMini from "../ui/StatMini.vue";

import { getAvgPerWorkday } from "../../api/teachers.api";
import { useDateRange } from "../../composables/usedateRange";
import { useTeacherSuggest } from "../../composables/useTeachersSuggest";

const dr = useDateRange();

const teacherText = ref("");
const selectedTeacher = ref("");
const mustPickError = ref("");

const ts = useTeacherSuggest({ debounceMs: 300, limit: 10 });

const loading = ref("");
const error = ref("");
const data = ref(null);

function formatDate(iso) {
  if (!iso) return "";
  const [y, m, d] = String(iso).split("-");
  return `${d}.${m}.${y}`;
}

watch(teacherText, (v) => {
  mustPickError.value = "";
  selectedTeacher.value = "";
  ts.open.value = true;
  ts.setQuery(v);
});

async function onPick(name) {
  teacherText.value = name;
  selectedTeacher.value = name;
  ts.close();
  await load(true);
}

async function onReset() {
  ts.close();
  dr.reset();

  teacherText.value = "";
  selectedTeacher.value = "";

  error.value = "";
  mustPickError.value = "";
  data.value = null;

  await load(false);
}

async function load(fromPeak = false) {
  error.value = "";
  mustPickError.value = "";
  data.value = null;

  const manual = teacherText.value.trim();
  const teacherForApi =
    selectedTeacher.value || (manual.length ? manual : null);

  if (
    !selectedTeacher.value &&
    manual.length >= 2 &&
    (ts.items.value?.length ?? 0) > 0
  ) {
    mustPickError.value = "Вибери викладача зі списку або допиши точніше";
    return;
  }

  if (!teacherForApi && manual.length === 1) {
    mustPickError.value = "Введи хоча б 2 символи або очисть поле";
    return;
  }
  loading.value = true;

  try {
    const res = await getAvgPerWorkday({
      teacher: teacherForApi ?? undefined,
      ...dr.toApiParams(),
    });
    data.value = res.data;
  } catch (e) {
    console.error(e);
    error.value = "Не вдалося завантажити середній показник.";
  } finally {
    loading.value = false;
  }
}

const titleLine = computed(() => {
  if (data.value?.teacher) return `для ${data.value.teacher}`;
  return "за всіх викладачів";
});
</script>

<template>
  <Card>
    <template #header>
      <div class="head">
        <div>
          <div class="title">Avg lessons / workday</div>
          <div class="sub" v-if="data">
            {{ titleLine }} · {{ formatDate(data.date_from) }} -
            {{ formatDate(data.date_to) }}
          </div>
          <div class="sub" v-else>Середній показник за період</div>
        </div>

        <div class="actions">
          <Button variant="ghost" @click="load" :disabled="loading"
            >Load</Button
          >
          <Button variant="ghost" @click="onReset" :disabled="loading"
            >Reset</Button
          >
        </div>
      </div>
    </template>

    <div class="form">
      <div>
        <div class="label">Teacher (optional)</div>
        <TeacherAutocomplete
          v-model="teacherText"
          :items="ts.items.value"
          :loading="ts.loading.value"
          :open="ts.open.value"
          placeholder="Порожньо = по всіх"
          @open="() => (ts.open.value = true)"
          @close="ts.close"
          @select="onPick"
        />
      </div>

      <div class="dates">
        <DateRange
          :from="dr.dateFrom.value"
          :to="dr.dateTo.value"
          :activePreset="dr.activePreset.value"
          @update:from="
            (v) => {
              dr.setFrom(v);
              load();
            }
          "
          @update:to="
            (v) => {
              dr.setTo(v);
              load();
            }
          "
          @preset="
            (k) => {
              dr.preset(k);
              load();
            }
          "
          @reset="onReset"
        />
      </div>
    </div>

    <Alert v-if="error" title="Error">{{ error }}</Alert>
    <Alert v-else-if="mustPickError" title="Error">{{ mustPickError }}</Alert>

    <div v-else-if="loading" class="skWrap">
      <Skeleton height="14px" width="60%" />
      <Skeleton height="14px" width="40%" />
      <Skeleton height="14px" width="70%" />
    </div>

    <div v-else-if="data" class="grid3">
      <StatMini
        label="avg lessons / workday"
        :value="Number(data.awg_lessons_per_workday).toFixed(2)"
      />
      <StatMini label="workdays" :value="data.workdays_count" />
      <StatMini label="total lessons" :value="data.total_lessons" />
    </div>

    <div v-else class="hint">
      Натисни <b>Load</b> (або вибери викладача зі списку).
    </div>
  </Card>
</template>

<style scoped>
.head {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.actions {
  display: flex;
  gap: 8px;
}

.title {
  font-weight: 800;
  font-size: 14px;
}

.sub {
  margin-top: 4px;
  font-size: 12px;
  opacity: 0.6;
}

.form {
  display: grid;
  gap: 12px;
  margin-bottom: 12px;
}

.label {
  font-size: 12px;
  opacity: 0.65;
  margin-bottom: 6px;
}

.dates {
  margin-top: 4px;
}

.grid3 {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 10px;
}

.skWrap {
  display: grid;
  gap: 10px;
}

.hint {
  opacity: 0.65;
  font-size: 13px;
  padding: 6px 0;
}

@media (max-width: 900px) {
  .grid3 {
    grid-template-columns: 1fr;
  }
}
</style>
