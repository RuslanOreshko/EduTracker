import { http } from "./http";

export function getTopTeachers({ dateFrom, dateTo, limit = 5 } = {}) {
  return http.get("/teachers/teacher/top", {
    params: {
      date_from: dateFrom ?? undefined,
      date_to: dateTo ?? undefined,
      limit,
    },
  });
}

export function getTeacherStats({
  teacher,
  dateFrom,
  dateTo,
  subject,
  group,
  splitTeachersBySlash = true,
} = {}) {
  return http.get("/teachers/teacher", {
    params: {
      teacher,
      date_from: dateFrom ?? undefined,
      date_to: dateTo ?? undefined,
      subject: subject ?? undefined,
      group: group ?? undefined,
      split_teachers_by_slash: splitTeachersBySlash,
    },
  });
}

export function compareTeachers({
  teacherA,
  teacherB,
  dateFrom,
  dateTo,
  topN = 5,
} = {}) {
  return http.get("/teachers/teacher/compare", {
    params: {
      teacher_a: teacherA,
      teacher_b: teacherB,
      date_from: dateFrom ?? undefined,
      date_to: dateTo ?? undefined,
      top_n: topN,
    },
  });
}

export function getTeacherPeakLoad({ teacher, dateFrom, dateTo } = {}) {
  return http.get("/teachers/teacher/peak-load", {
    params: {
      teacher,
      date_from: dateFrom ?? undefined,
      date_to: dateTo ?? undefined,
    },
  });
}

export function getAvgPerWorkday({ teacher, dateFrom, dateTo } = {}) {
  return http.get("/teachers/teacher/avg-per-workday", {
    params: {
      teacher: teacher ?? undefined,
      date_from: dateFrom ?? undefined,
      date_to: dateTo ?? undefined,
    },
  });
}

// апішка для зручного пошуку викладача
export function suggestTeachers({ q, limit = 10 } = {}) {
  return http.get("/teachers/suggest", {
    params: {
      q: q ?? "",
      limit,
    },
  });
}
