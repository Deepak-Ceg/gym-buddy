const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export { API_BASE };

export type UserProfile = {
  id: string;
  name: string;
  email: string;
  timezone: string;
  dietary_preferences: string[];
  goal: string;
  program_start_date: string;
};

export type DashboardResponse = {
  generated_for: string;
  current_user: UserProfile;
  buddy_user: UserProfile;
  buddy_pair: {
    id: string;
    member_ids: string[];
  };
  my_score: {
    user_id: string;
    total: number;
    breakdown: {
      steps_activity: number;
      workout_completion: number;
      diet_adherence: number;
      recovery_checkin: number;
      streak_bonus: number;
      penalties: number;
    };
  } | null;
  buddy_score: {
    user_id: string;
    total: number;
    breakdown: {
      steps_activity: number;
      workout_completion: number;
      diet_adherence: number;
      recovery_checkin: number;
      streak_bonus: number;
      penalties: number;
    };
  } | null;
  leaderboard: {
    entries: Array<{
      user_id: string;
      user_name: string;
      total_points: number;
      current_streak: number;
      penalties: number;
      rank: number;
      score_delta: number;
    }>;
  };
  my_checkin: {
    mood: string;
    soreness: string;
    notes: string;
    workout_completed: boolean;
  } | null;
  my_milestones: Array<{
    id: string;
    user_id: string;
    title: string;
    target_date: string;
    status: string;
    bonus_points: number;
  }>;
  buddy_milestones: Array<{
    id: string;
    user_id: string;
    title: string;
    target_date: string;
    status: string;
    bonus_points: number;
  }>;
  workout_plan: {
    title: string;
    focus: string;
    days: Array<{
      day: string;
      theme: string;
      duration_minutes: number;
      exercises: Array<{ name: string; sets: string; reps: string }>;
    }>;
  };
  meal_guidance: Array<{
    id: string;
    title: string;
    meal_type: string;
    items: string[];
    tags: string[];
    avoid: string[];
  }>;
  my_coach_insight: {
    summary: string;
    next_actions: string[];
  } | null;
  buddy_coach_insight: {
    summary: string;
    next_actions: string[];
  } | null;
};

export type LoginPayload = {
  email: string;
  password: string;
};

export type CheckInSubmission = {
  user_id: string;
  date: string;
  workout_completed: boolean;
  recovery_completed: boolean;
  mood: string;
  soreness: string;
  notes: string;
  voice_transcript?: string;
  diet: {
    sugar_free: boolean;
    low_fried_food: boolean;
    hydration_goal_met: boolean;
    protein_focus_met: boolean;
    fiber_focus_met: boolean;
  };
};

async function parseJson<T>(response: Response): Promise<T> {
  if (!response.ok) {
    throw new Error("Request failed");
  }
  return response.json() as Promise<T>;
}

export async function login(payload: LoginPayload) {
  const response = await fetch(`${API_BASE}/api/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    credentials: "include",
    body: JSON.stringify(payload)
  });
  return parseJson<{ user: UserProfile }>(response);
}

export async function logout() {
  const response = await fetch(`${API_BASE}/api/auth/logout`, {
    method: "POST",
    credentials: "include"
  });
  return parseJson<{ status: string }>(response);
}

export async function getMe() {
  const response = await fetch(`${API_BASE}/api/auth/me`, {
    credentials: "include",
    cache: "no-store"
  });
  if (response.status === 401) {
    return null;
  }
  return parseJson<{ user: UserProfile }>(response);
}

export async function getDashboard(): Promise<DashboardResponse> {
  const response = await fetch(`${API_BASE}/api/dashboard`, {
    credentials: "include",
    cache: "no-store"
  });
  return parseJson<DashboardResponse>(response);
}

export async function postCheckIn(payload: CheckInSubmission) {
  const response = await fetch(`${API_BASE}/api/checkins`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    credentials: "include",
    body: JSON.stringify(payload)
  });
  return parseJson(response);
}
