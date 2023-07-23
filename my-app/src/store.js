import { writable } from "svelte/store";

export const userPrompt = writable("");

// 4x4 grid
export const grid = writable([
  {
    completion: "",
    prompt: "111111111111111111111111111",
  },
  {
    completion: "",
    prompt: "222222222222222222222222222",
  },
  {
    completion: "",
    prompt: "333333333333333333333333333",
  },
  {
    completion: "",
    prompt: "44444444444444",
  },
]);
