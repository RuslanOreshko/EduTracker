import { defineStore } from "pinia";
import { http } from "../api/http";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    accessToken: null,
    isReady: false,
  }),

  getters: {
    isAuthenticated: (state) => Boolean(state.accessToken),
  },

  actions: {
    async loginWithGoogle(idToken) {
      const res = await http.post("/auth/google", { id_token: idToken });
      this.accessToken = res.data.access_token;
    },

    async refresh() {
      const res = await http.post("/auth/refresh");
      this.accessToken = res.data.access_token;
    },

    async logout() {
      try {
        await http.post("/auth/logout");
      } finally {
        this.accessToken = null;
      }
    },

    async init() {
      try {
        await this.refresh();
      } catch {
        this.accessToken = null;
      } finally {
        this.isReady = true;
      }
    },
  },
});
