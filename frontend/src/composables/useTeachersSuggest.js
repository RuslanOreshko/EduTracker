import { computed, ref, watch } from "vue";
import { suggestTeachers } from "../api/teachers.api";

export function useTeacherSuggest({
  minLen = 2,
  debounceMs = 300,
  limit = 10,
} = {}) {
  const query = ref("");
  const loading = ref(false);
  const error = ref("");
  const items = ref([]);
  const open = ref(false);

  let reqId = 0;
  let t = null;

  async function runSuggest(q) {
    const id = ++reqId;

    error.value = "";
    if (!q || q.trim().length < minLen) {
      items.value = [];
      loading.value = false;
      return;
    }

    loading.value = true;
    try {
      const res = await suggestTeachers({ q: q.trim(), limit });
      if (id !== reqId) return;
      items.value = res.data?.items ?? [];
    } catch (e) {
      if (id !== reqId) return;
      items.value = [];
      error.value = "Suggest не працює";
    } finally {
      if (id === reqId) loading.value = false;
    }
  }

  watch(query, (v) => {
    open.value = true;
    if (t) clearTimeout(t);
    t = setTimeout(() => runSuggest(v), debounceMs);
  });

  function setQuery(v) {
    query.value = v ?? "";
  }

  function close() {
    open.value = false;
  }

  function reset() {
    query.value = "";
    items.value = [];
    error.value = "";
    loading.value = false;
    open.value = false;
  }

  return {
    query,
    loading,
    error,
    items,
    open,
    setQuery,
    close,
    reset,
    runSuggest,
  };
}
