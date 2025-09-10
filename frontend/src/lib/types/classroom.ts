export interface Classroom {
  id: number;
  name: string;
  description: string;
  teacher: {
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    role: string;
    regdno?: string;
  };
  code: string;
  created_at: string;
  students: Array<{
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    role: string;
    regdno?: string;
  }>;
  student_count: number;
  assignment_count: number;
}
