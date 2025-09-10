<script lang="ts">
  import SidebarLink from './SidebarLink.svelte';
  import SidebarToggle from './SidebarToggle.svelte';
  import SidebarHeader from './SidebarHeader.svelte';
  import { isExpanded } from '$lib/stores/sidebar';
  import { currentPath } from '$lib/stores/router';
  import { logout } from '$lib/stores/auth';
  import {
    faHouse,
    faClipboardList,
    faSchool,
    faChartPie,
    faArrowRightFromBracket
  } from '@fortawesome/free-solid-svg-icons';
</script>

<aside
  class={`h-screen flex flex-col justify-between bg-gray-50 border-r border-gray-200 transition-all duration-300 ${
    $isExpanded ? 'w-64' : 'w-20'
  }`}
>
  <!-- Header -->
  <SidebarHeader />

  <!-- Navigation -->
  <nav class="flex-1 px-1 space-y-2">
  <SidebarLink
    link={{ label: 'Home', href: '/', icon: faHouse, color: 'green' }}
    currentPath={currentPath}
  />
  <SidebarLink
    link={{ label: 'Assignments', href: '/assignments', icon: faClipboardList, color: 'yellow' }}
    currentPath={currentPath}
  />
  <SidebarLink
    link={{ label: 'Classrooms', href: '/teacher/classrooms', icon: faSchool, color: 'purple' }}
    currentPath={currentPath}
  />
  <SidebarLink
    link={{ label: 'Reports', href: '/reports', icon: faChartPie, color: 'blue' }}
    currentPath={currentPath}
  />
  <SidebarLink
    link={{ label: 'Logout', icon: faArrowRightFromBracket, color: 'red' }}
    currentPath={currentPath}
    onClick={logout}
  />
</nav>


  <!-- Toggle at bottom -->
  <div class="p-4">
    <SidebarToggle />
  </div>
</aside>
