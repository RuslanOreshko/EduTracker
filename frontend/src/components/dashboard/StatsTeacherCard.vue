<script setup>
import { ref, watch } from "vue";

import Card from "../ui/Card.vue";
import Input from "../ui/Input.vue";
import Button from "../ui/Button.vue";
import Alert from "../ui/Alert.vue";
import Skeleton from "../ui/Skeleton.vue";
import DateRange from "../ui/DateRange.vue";

import { getTeacherStats } from "../../api/teachers.api";
import { useDateRange } from "../../composables/usedateRange";

import TeacherAutocomplete from "../ui/TeacherAutocomplete.vue";
import { useTeacherSuggest } from "../../composables/useTeachersSuggest";

const teacherText = ref("");
const selectedTeacher = ref("");
const mustPickError = ref("");
const ts = useTeacherSuggest({ debounceMs: 320, limit: 10 });

const loading = ref(false);
const error = ref("");
const data = ref(null);

const subject = ref("");
const group = ref("");
const splitBySlash = ref(true);

const dr = useDateRange();

// Зручний вибір викладача
watch(teacherText, (v) => {
  mustPickError.value = "";
  selectedTeacher.value = "";
  ts.open.value = true;
  ts.setQuery(v);
});

function onPick(name) {
  teacherText.value = name;
  selectedTeacher.value = name;
  ts.close();
}

// вибір дати
function formatDate(iso) {
  if (!iso) return "";
  const [y, m, d] = iso.split("-");
  return `${d}.${m}.${y}`;
}

function sortMapdesc(obj) {
  if (!obj) return [];
  return Object.entries(obj)
    .sort((a, b) => Number(b[1]) - Number(a[1]))
    .reduce((acc, [k, v]) => {
      acc[k] = v;
      return acc;
    }, {});
}

function avgPerDay(total, byDate) {
  const n = Object.keys(byDate || {}).length;
  if (!n) return "0";
  return (Number(total) / n).toFixed(2);
}

function lastDate(byDate) {
  const keys = Object.keys(byDate || {});
  if (!keys.length) return "-";
  keys.sort();
  return keys[keys.length - 1];
}

async function load() {
  error.value = "";
  mustPickError.value = "";
  data.value = null;

  const manual = teacherText.value.trim();
  const teacherForApi = selectedTeacher.value || manual;

  if (teacherForApi.length < 2) {
    mustPickError.value = "Введи хоча б 2 символи";
    return;
  }

  if (!selectedTeacher.value && (ts.items.value?.length ?? 0) > 0) {
    mustPickError.value = "Вибери викладача зі списку або допиши точніше";
    return;
  }

  loading.value = true;

  try {
    const res = await getTeacherStats({
      teacher: teacherForApi,
      subject: subject.value.trim() || undefined,
      group: group.value.trim() || undefined,
      splitTeachersBySlash: splitBySlash.value,
      ...dr.toApiParams(),
    });

    data.value = res.data;
  } catch (e) {
    console.error(e);
    error.value = "Не вдалося завантажити статистику викладача.";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <Card>
    <template #header>
      <div class="head">
        <div>
          <div class="title">Teacher stats</div>
          <div class="sub">Статистика по конкретному викладачу</div>
        </div>

        <Button variant="ghost" @click="load" :disabled="loading">
          Load
        </Button>
      </div>
    </template>

    <div class="form">
      <div class="grid2">
        <div>
          <div class="label">Teacher *</div>
          <TeacherAutocomplete
            v-model="teacherText"
            :items="ts.items.value"
            :loading="ts.loading.value"
            :open="ts.open.value"
            placeholder="Напр: ніколаєнко а. і."
            @open="() => (ts.open.value = true)"
            @close="ts.close"
            @select="onPick"
          />
        </div>

        <div class="toggle">
          <label class="check">
            <input type="checkbox" v-model="splitBySlash" />
            <span>Split by "/"</span>
          </label>
        </div>
      </div>

      <div class="grid2">
        <div>
          <div class="label">Subject (Optional)</div>
          <Input v-model="subject" placeholder="Напр: Математичний аналіз" />
        </div>

        <div>
          <div class="label">Group (Optional)</div>
          <Input v-model="group" placeholder="КН-3/1" />
        </div>
      </div>

      <div class="dates">
        <DateRange
          :from="dr.dateFrom.value"
          :to="dr.dateTo.value"
          :activePreset="dr.activePreset.value"
          @update:from="(v) => dr.setFrom(v)"
          @update:to="(v) => dr.setTo(v)"
          @preset="(k) => dr.preset(k)"
          @reset="() => dr.reset()"
        />
      </div>
    </div>

    <Alert v-if="error" title="Error">{{ error }}</Alert>
    <Alert v-if="mustPickError" title="Error">{{ mustPickError }}</Alert>

    <div v-else-if="loading" class="skWrap">
      <Skeleton height="14px" width="60%" />
      <Skeleton height="14px" width="40%" />
      <Skeleton height="14px" width="70%" />
    </div>

    <div v-else-if="data" class="result">
      <div class="summary">
        <div class="sumLeft">
          <div class="sumTitle">{{ data.teacher }}</div>
          <div class="sumSub">
            {{ formatDate(data.date_from) }} - {{ formatDate(data.date_to) }}
          </div>
        </div>

        <div class="sumRight">
          <div class="sumNum">{{ data.total_lessons }}</div>
          <div class="sumLbl">Lessons</div>
        </div>
      </div>

      <div class="cols">
        <div class="box">
          <div class="boxTitle">By group</div>

          <div class="rows">
            <div
              class="r"
              v-for="(v, k) in sortMapdesc(data.by_group)"
              :key="k"
            >
              <div class="k">{{ k }}</div>
              <div class="v">{{ v }}</div>
            </div>
          </div>
        </div>

        <div class="box">
          <div class="boxTitle">By subject</div>
          <div class="rows">
            <div
              class="r"
              v-for="(v, k) in sortMapdesc(data.by_subject)"
              :key="k"
            >
              <div class="k">{{ k }}</div>
              <div class="v">{{ v }}</div>
            </div>
          </div>
        </div>

        <div class="box">
          <div class="boxTitle">By date (compact)</div>

          <div class="mini">
            <div>
              days: <b>{{ Object.keys(data.by_date || {}).length }}</b>
            </div>
            <div>
              avg/days:
              <b>{{ avgPerDay(data.total_lessons, data.by_date) }}</b>
            </div>
            <div>
              last date:
              <b>{{ lastDate(data.by_date) }}</b>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="hint">Введи викладача і натисни <b>Load</b></div>
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

.grid2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  align-items: end;
}

.toggle {
  display: flex;
  justify-content: flex-end;
}

.check {
  display: flex;
  gap: 10px;
  align-items: center;
  font-size: 13px;
  opacity: 0.9;
}

.check input {
  width: 16px;
  height: 16px;
}

.dates {
  margin-top: 4px;
}

.skWrap {
  display: grid;
  gap: 10px;
}

.result {
  display: grid;
  gap: 8px;
}

.kv {
  display: grid;
  grid-template-columns: 160px 1fr;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.k {
  opacity: 0.7;
  font-size: 12px;
}

.v {
  font-weight: 700;
  font-size: 13px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.hint {
  opacity: 0.65;
  font-size: 13px;
  padding: 6px 0;
}

.result {
  display: grid;
  gap: 12px;
}

.summary {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 12px;

  padding: 12px 12px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.sumTitle {
  font-weight: 900;
  font-size: 14px;
}

.sumSub {
  margin-top: 4px;
  font-size: 12px;
  opacity: 0.65;
}

.sumRight {
  text-align: right;
  line-height: 1.1;
}

.sumNum {
  font-weight: 900;
  font-size: 18px;
}

.sumLbl {
  margin-top: 4px;
  font-size: 11px;
  opacity: 0.6;
}

.cols {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

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

.r {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 10px;
  align-items: center;
  padding: 8px 10px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
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

.pillRow {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.pill {
  min-width: 140px;
  padding: 10px 12px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.pillNum {
  font-weight: 900;
  font-size: 16px;
}

.pillLbl {
  margin-top: 4px;
  font-size: 11px;
  opacity: 0.6;
}

.mini {
  display: grid;
  gap: 6px;
  font-size: 13px;
  opacity: 0.85;
}

@media (max-width: 900px) {
  .cols {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 900px) {
  .grid2 {
    grid-template-columns: 1fr;
  }
  .toggle {
    justify-content: flex-start;
  }
}
</style>
