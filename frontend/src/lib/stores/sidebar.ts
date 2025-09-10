import { writable } from 'svelte/store';

// Sidebar state store
export const isExpanded = writable(true); // true = expanded, false = collapsed
