import { defineStore } from 'pinia';

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    siteName: localStorage.getItem('siteName') || 'Trouble Ticket',
    timezone: localStorage.getItem('timezone') || 'Asia/Jakarta',
    language: localStorage.getItem('language') || 'id',
  }),
  actions: {
    setSiteName(name: string) {
      if (name.trim() === '') return;
      this.siteName = name;
      localStorage.setItem('siteName', name);
    },
    setTimezone(timezone: string) {
      this.timezone = timezone;
      localStorage.setItem('timezone', timezone);
    },
    setLanguage(language: string) {
      this.language = language;
      localStorage.setItem('language', language);
    },
  },
});