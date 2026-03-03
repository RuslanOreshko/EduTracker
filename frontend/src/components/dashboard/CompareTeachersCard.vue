<script setup>
import { computed, ref, watch } from "vue";

import Card from "../ui/Card.vue";
import Button from "../ui/Button.vue";
import Alert from "../ui/Alert.vue";
import Skeleton from "../ui/Skeleton.vue";
import DateRange from "../ui/DateRange.vue";
import TeacherAutocomplete from "../ui/TeacherAutocomplete.vue";
import StatMapBox from "../ui/StatMapBox.vue";

import { compareTeachers } from "../../api/teachers.api";
import { useDateRange } from "../../composables/usedateRange";
import { useTeacherSuggest } from "../../composables/useTeachersSuggest";

const loading = ref(false);
const error = ref("");
const mustPickError = ref("");
const data = ref(null);

const teacherAText = ref("");
const teacherBText = ref("");
const selectedA = ref("");
const selectedB = ref("");

const topN = ref(5);

const tsA = useTeacherSuggest({ debounceMs: 320, limit: 10 });
const tsB = useTeacherSuggest({ debounceMs: 320, limit: 10 });

const dr = useDateRange();

function formatDate(iso) {
  if (!iso) return "";
  const [y, m, d] = String(iso).split("-");
  return `${d}.${m}.${y}`;
}

function listToMap(list) {
  const out = {};
  for (const row of list || []) {
    const k = row?.name;
    const v = row?.count;
    if (!k) continue;
    out[String(k)] = Number(v) || 0;
  }
  return out;
}

const aSubjectMap = computed(() =>
  listToMap(data.value?.teacher_a?.by_subject_top),
);
const aGroupMap = computed(() =>
  listToMap(data.value?.teacher_a?.by_group_top),
);

const bSubjectMap = computed(() =>
  listToMap(data.value?.teacher_b?.by_subject_top),
);
const bGroupMap = computed(() =>
  listToMap(data.value?.teacher_b?.by_group_top),
);

const winnerLabel = computed(() => {
  const w = data.value?.comparison?.winner;
  if (w === "teacher_a") return "Teacher A";
  if (w === "teacher_b") return "Teacher B";
  return "-";
});

watch(teacherAText, (v) => {
  mustPickError.value = "";
  selectedA.value = "";
  tsA.open.value = true;
  tsA.setQuery(v);
});

watch(teacherBText, (v) => {
  mustPickError.value = "";
  selectedB.value = "";
  tsB.open.value = true;
  tsB.setQuery(v);
});

async function onPickA(name) {
  teacherAText.value = name;
  selectedA.value = name;
  tsA.close();

  if (selectedB.value || teacherBText.value.trim().length >= 2) {
    await load(true);
  }
}

async function onPickB(name) {
  teacherBText.value = name;
  selectedB.value = name;
  tsB.close();

  if (selectedA.value || teacherAText.value.trim().length >= 2) {
    await load(true);
  }
}

async function onReset() {
  tsA.close();
  tsB.close();
  dr.reset();

  error.value = "";
  mustPickError.value = "";
  data.value = null;
}

async function load(fromPick = false) {
  error.value = "";
  mustPickError.value = "";
  data.value = null;

  const a = (selectedA.value || teacherAText.value.trim()).trim();
  const b = (selectedB.value || teacherBText.value.trim()).trim();

  if (a.length < 2 || b.length < 2) {
    mustPickError.value = "Введи обох викладачів (мінімум 2 символи)";
    return;
  }

  if (!selectedA.value && (tsA.items.value?.length ?? 0) > 0) {
    mustPickError.value = "Викладача A вибери зі списку або допиши точніше";
    return;
  }
  if (!selectedB.value && (tsB.items.value?.length ?? 0) > 0) {
    mustPickError.value = "Викладача B вибери зі списку або допиши точніше";
    return;
  }

  loading.value = true;

  try {
    const res = await compareTeachers({
      teacherA: a,
      teacherB: b,
      topN: Math.min(20, Math.max(1, Number(topN.value) || 5)),
      ...dr.toApiParams(),
    });

    data.value = res.data;
  } catch (e) {
    console.error(e);
    error.value = "Не вдалося порівняти викладачів.";
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
          <div class="title">Compare teachers</div>
          <div class="sub">Порівняння двох викладачів</div>
        </div>

        <Button variant="ghost" @click="load" :disabled="loading">Load</Button>
      </div>
    </template>

    <div class="form">
      <div class="grid2">
        <div>
          <div class="label">Teacher A *</div>
          <TeacherAutocomplete
            v-model="teacherAText"
            :items="tsA.items.value"
            :loading="tsA.loading.value"
            :open="tsA.open.value"
            placeholder="Викладач A"
            @open="() => (tsA.open.value = true)"
            @close="tsA.close"
            @select="onPickA"
          />
        </div>

        <div>
          <div class="label">Teacher B *</div>
          <TeacherAutocomplete
            v-model="teacherBText"
            :items="tsB.items.value"
            :loading="tsB.loading.value"
            :open="tsB.open.value"
            placeholder="Викладач B"
            @open="() => (tsB.open.value = true)"
            @close="tsB.close"
            @select="onPickB"
          />
        </div>
      </div>

      <div class="grid2">
        <div>
          <div class="label">Top N (1-20)</div>
          <input
            class="miniInput"
            type="number"
            min="1"
            max="20"
            v-model="topN"
          />
        </div>

        <div class="right">
          <Button variant="ghost" @click="onReset">Reset</Button>
        </div>
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
    <Alert v-if="mustPickError" title="Error">{{ mustPickError }}</Alert>

    <div v-else-if="loading" class="skWrap">
      <Skeleton height="14px" width="60%" />
      <Skeleton height="14px" width="40%" />
      <Skeleton height="14px" width="70%" />
    </div>

    <div v-else-if="data" class="result">
      <!-- summary -->
      <div class="summary">
        <div>
          <div class="sumTitle">
            Winner: <b>{{ winnerLabel }}</b>
          </div>
          <div class="sumSub">{{ data.summary }}</div>
          <div class="sumSub">
            {{ formatDate(data.date_from) }} - {{ formatDate(data.date_to) }}
          </div>
        </div>

        <div class="sumRight">
          <div class="sumNum">{{ data.comparison.difference_lessons }}</div>
          <div class="sumLbl">diff lessons</div>
          <div class="sumLbl2">+{{ data.comparison.difference_percent }}%</div>
        </div>
      </div>

      <!-- totals -->
      <div class="totals">
        <div class="tBox">
          <div class="tName">A: {{ data.teacher_a.name }}</div>
          <div class="tNum">{{ data.teacher_a.total_lessons }}</div>
          <div class="tLbl">lessons</div>
        </div>

        <div class="tBox">
          <div class="tName">B: {{ data.teacher_b.name }}</div>
          <div class="tNum">{{ data.teacher_b.total_lessons }}</div>
          <div class="tLbl">lessons</div>
        </div>
      </div>

      <!-- top lists -->
      <div class="cols">
        <div class="col">
          <div class="colTitle">Teacher A</div>
          <StatMapBox title="Top subjects" :map="aSubjectMap" :step="8" />
          <StatMapBox title="Top groups" :map="aGroupMap" :step="8" />
        </div>

        <div class="col">
          <div class="colTitle">Teacher B</div>
          <StatMapBox title="Top subjects" :map="bSubjectMap" :step="8" />
          <StatMapBox title="Top groups" :map="bGroupMap" :step="8" />
        </div>
      </div>
    </div>

    <div v-else class="hint">Введи A і B та натисни <b>Load</b></div>
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

.right {
  display: flex;
  justify-content: flex-end;
}

.dates {
  margin-top: 4px;
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
  font-size: 13px;
}

.sumSub {
  margin-top: 6px;
  font-size: 12px;
  opacity: 0.7;
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

.sumLbl2 {
  margin-top: 3px;
  font-size: 11px;
  opacity: 0.7;
}

.totals {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.tBox {
  padding: 12px 12px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.tName {
  font-weight: 800;
  font-size: 12px;
  opacity: 0.8;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.tNum {
  margin-top: 8px;
  font-weight: 900;
  font-size: 18px;
}

.tLbl {
  margin-top: 4px;
  font-size: 11px;
  opacity: 0.6;
}

.cols {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.col {
  display: grid;
  gap: 12px;
}

.colTitle {
  font-weight: 900;
  font-size: 12px;
  opacity: 0.7;
  padding-left: 2px;
}

.miniInput {
  width: 100%;
  border-radius: 12px;
  padding: 10px 12px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.85);
  outline: none;
}

@media (max-width: 900px) {
  .grid2,
  .cols,
  .totals {
    grid-template-columns: 1fr;
  }
}
</style>
