// Custom parameter matcher for user roles
// This ensures only valid roles ('student' or 'teacher') are accepted in routes

export function match(param: string): boolean {
  return param === 'student' || param === 'teacher';
}
