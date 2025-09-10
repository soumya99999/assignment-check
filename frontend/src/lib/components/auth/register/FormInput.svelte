<script lang="ts">
  export let label: string;
  export let type: string;
  export let id: string;
  export let value: string;
  export let required: boolean = false;
  export let placeholder: string = '';
</script>

<div>
  <label for={id} class="block text-sm font-medium text-gray-700 mb-2">{label}</label>
  <input
    {type}
    {id}
    {placeholder}
    bind:value
    {required}
    class="w-full rounded-xl px-4 py-3 text-sm outline-none border-none bg-[#f4f6f8]
           shadow-[inset_5px_5px_10px_#d1d1d1,inset_-5px_-5px_10px_#ffffff]
           focus:shadow-[inset_3px_3px_6px_#c1c1c1,inset_-3px_-3px_6px_#ffffff]"
  />
</div>
