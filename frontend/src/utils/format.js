export function titleCaseUk(str = "") {
  const s = String(str ?? "").trim();
  if (!s) return "";

  return s
    .split(/\s+/)
    .filter(Boolean)
    .map((w) => {
      const first = w.charAt(0);
      const rest = w.slice(1);
      return first ? first.toUpperCase() + rest : w;
    })
    .join(" ");
}

export function formatLessons(value) {
  if (value === null || value === undefined) return "-";

  const n = Number(value);
  if (Number.isNaN(n)) return String(value);

  return Number.isInteger(n) ? String(n) : String(n);
}
