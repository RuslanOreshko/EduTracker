<script setup>
import { onMounted, ref } from "vue";

import Card from "../ui/Card.vue";
import Skeleton from "../ui/Skeleton.vue";
import Alert from "../ui/Alert.vue";
import Button from "../ui/Button.vue";
import DateRange from "../ui/DateRange.vue";

import { getTopTeachers } from "../../api/teachers.api";
import { titleCaseUk, formatLessons } from "../../utils/format";
import { useDateRange } from "../../composables/usedateRange";

const loading = ref(true);
const error = ref("");
const data = ref(null);

const dr = useDateRange();

// Вибір дати
async function load() {
  loading.value = true;
  error.value = "";

  try {
    const res = await getTopTeachers({
      limit: 5,
      ...dr.toApiParams(),
    });
    data.value = res.data;
  } catch (e) {
    console.error(e);
    error.value = "Не вдалося завантажити топ викладачів.";
  } finally {
    loading.value = false;
  }
}

function formatDate(iso) {
  if (!iso) return "";
  const [y, m, d] = iso.split("-");
  return `${d}.${m}.${y}`;
}

onMounted(load);
</script>

<template>
  <Card>
    <template #header>
      <div class="head">
        <div>
          <div class="title">Top teachers</div>
          <div class="sub" v-if="data">
            {{ formatDate(data.date_from) }} - {{ formatDate(data.date_to) }}
          </div>
          <div class="sub" v-else-if="loading">
            <Skeleton height="12px" width="100px" />
          </div>
        </div>

        <Button variant="ghost" @click="load" :disabled="loading"
          >Refresh</Button
        >
      </div>
    </template>

    <div class="filters">
      <DateRange
        :from="dr.dateFrom.value"
        :to="dr.dateTo.value"
        :activePresset="dr.activePresset"
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
        @reset="
          () => {
            dr.reset();
            load();
          }
        "
      />
    </div>

    <Alert v-if="error" title="API error">
      {{ error }}
    </Alert>

    <div class="list" v-else-if="loading">
      <div class="row" v-for="i in 5" :key="i">
        <Skeleton height="14px" width="28px" radius="8px" />
        <Skeleton height="14px" width="60%" />
        <Skeleton height="14px" width="70px" />
      </div>
    </div>

    <div v-else class="list">
      <div
        class="row"
        v-for="(item, idx) in data?.top ?? []"
        :key="item.teacher + idx"
      >
        <div class="rank">#{{ idx + 1 }}</div>

        <div class="teacher" :title="item.teacher">
          {{ titleCaseUk(item.teacher) }}
        </div>

        <div class="lessons">
          <span class="num">{{ formatLessons(item.total_lessons) }}</span>
          <span class="lbl">lessons</span>
        </div>
      </div>

      <div class="empty" v-if="(data?.top ?? []).length === 0">
        Немає даних за вибраний період.
      </div>
    </div>
  </Card>
</template>

<style scoped>
.head {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.title {
  font-weight: 800;
  font-size: 14px;
  letter-spacing: 0.2px;
}

.sub {
  margin-top: 4px;
  font-size: 12px;
  opacity: 0.6;
}

.list {
  display: grid;
  gap: 10px;
}

.row {
  display: grid;
  grid-template-columns: 46px 1fr auto;
  align-items: center;
  gap: 12px;

  padding: 10px 12px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.rank {
  font-weight: 800;
  font-size: 12px;
  opacity: 0.7;
}

.teacher {
  font-weight: 700;
  font-size: 13px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.lessons {
  text-align: right;
  line-height: 1.1;
}

.num {
  font-weight: 900;
  font-size: 14px;
}

.lbl {
  display: block;
  margin-top: 3px;
  font-size: 11px;
  opacity: 0.55;
}

.empty {
  padding: 12px 12px;
  border-radius: 14px;
  border: 1px dashed rgba(255, 255, 255, 0.14);
  opacity: 0.7;
}

.filters {
  margin-bottom: 12px;
}
</style>
