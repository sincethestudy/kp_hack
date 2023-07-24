import { writable } from "svelte/store";

export const userPrompt = writable("");
export const systemPrompt = writable("");

// 4x4 grid
export const grid = writable([
  {
    completion: "",
    prompt: "",
  },
  {
    completion: "",
    prompt: "",
  },
  {
    completion: "",
    prompt: "",
  },
  {
    completion: "",
    prompt: "",
  },
]);
