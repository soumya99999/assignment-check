import { writable } from "svelte/store";
import { goto as svelteGoto } from "$app/navigation";

export const isNavigating = writable(false);

export async function goto(url: string | URL, options?: { replaceState?: boolean }) {
  isNavigating.set(true);

  try {
    // Convert relative strings into absolute URLs
    const resolvedUrl =
      typeof url === "string"
        ? new URL(url, window.location.origin)
        : url;

    await svelteGoto(resolvedUrl, options);
  } finally {
    setTimeout(() => {
      isNavigating.set(false);
    }, 300);
  }
}
