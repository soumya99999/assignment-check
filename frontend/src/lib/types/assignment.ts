export interface Assignment {
  id: number;
  title: string;
  description: string;
  teacher: {
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    role: string;
  };
  classroom: number;
  question_file: string | null;
  correct_answer_file: string | null;
  total_marks: number;
  created_at: string;
  submitted_students_count: number;
}

export interface AssignmentFormData {
  title: string;
  description: string;
  classroom: number;
  question_file?: File;
  correct_answer_file?: File;
  total_marks: number;
}

export interface Submission {
  id: number;
  assignment: number;
  student: {
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    role: string;
    regdno: string;
  };
  submission_file: string;
  submission_date: string;
  score: number | null;
  plagiarism_report: string | null;
}
