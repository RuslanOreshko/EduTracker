import { ref } from "vue";

function toISO(d) {
  return d.toISOString().slice(0, 10);
}

export function useDateRange() {
  const dateFrom = ref("");
  const dateTo = ref("");
  const activePreset = ref("");

  function setFrom(v) {
    dateFrom.value = v;
    activePreset.value = "";
  }

  function setTo(v) {
    dateTo.value = v;
    activePreset.value = "";
  }

  function preset(kind) {
    const today = new Date();
    const toIso = toISO(today);

    if (kind === "30d") {
      const from = new Date(today);
      from.setDate(from.getDate() - 30);
      dateFrom.value = toISO(from);
      dateTo.value = toIso;
      activePreset.value = "30d";
      return;
    }

    if (kind === "academic") {
      const y = today.getFullYear();
      const m = today.getMonth() + 1;
      const startYear = m >= 9 ? y : y - 1;
      dateFrom.value = `${startYear}-09-01`;
      dateTo.value = toIso;
      activePreset.value = "academic";
    }
  }

  function reset() {
    dateFrom.value = "";
    dateTo.value = "";
    activePreset.value = "";
  }

  function toApiParams() {
    return {
      dateFrom: dateFrom.value || undefined,
      dateTo: dateTo.value || undefined,
    };
  }

  return {
    dateFrom,
    dateTo,
    activePreset,
    setFrom,
    setTo,
    preset,
    reset,
    toApiParams,
  };
}
